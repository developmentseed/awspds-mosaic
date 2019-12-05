"""awspds_mosaic.mosaic: create mosaicJSON from a stac query."""

from typing import Dict, Tuple

import os
import json
import requests
import itertools
from datetime import datetime

import mercantile
from shapely.geometry import box, shape
from supermercado import burntiles

from awspds_mosaic.utils import bbox_to_geojson

from loguru import logger


def _get_season(date, lat=0):
    if lat > 0:
        season_names = {1: "winter", 2: "spring", 3: "summer", 4: "autumn"}
    else:
        season_names = {4: "winter", 3: "spring", 2: "summer", 1: "autumn"}

    month = datetime.strptime(date[0:10], "%Y-%m-%d").month

    # from https://stackoverflow.com/questions/44124436/python-datetime-to-season
    idx = (month % 12 + 3) // 3

    return season_names[idx]


def stac_to_mosaicJSON(
    query: Dict,
    minzoom: int = 7,
    maxzoom: int = 12,
    optimized_selection: bool = True,
    maximum_items_per_tile: int = 20,
    stac_collection_limit: int = 500,
    seasons: Tuple = ["spring", "summer", "autumn", "winter"],
    stac_url: str = os.environ.get("SATAPI_URL", "https://sat-api.developmentseed.org"),
) -> Dict:
    """
    Create a mosaicJSON from a stac request.

    Attributes
    ----------
    query : str
        sat-api query.
    minzoom : int, optional, (default: 7)
        Mosaic Min Zoom.
    maxzoom : int, optional (default: 12)
        Mosaic Max Zoom.
    optimized_selection : bool, optional (default: true)
        Limit one Path-Row scene per quadkey.
    maximum_items_per_tile : int, optional (default: 20)
        Limit number of scene per quadkey. Use 0 to use all items.
    stac_collection_limit : int, optional (default: None)
        Limits the number of items returned by sat-api
    stac_url : str, optional (default: from ENV)

    Returns
    -------
    out : dict
        MosaicJSON definition.

    """
    if stac_collection_limit:
        query.update(limit=stac_collection_limit)

    logger.debug(json.dumps(query))

    def fetch_sat_api(query):
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip",
            "Accept": "application/geo+json",
        }

        url = f"{stac_url}/stac/search"
        data = requests.post(url, headers=headers, json=query).json()
        error = data.get("message", "")
        if error:
            raise Exception(f"SAT-API failed and returned: {error}")

        meta = data.get("meta", {})
        if not meta.get("found"):
            return []

        logger.debug(json.dumps(meta))

        features = data["features"]
        if data["links"]:
            curr_page = int(meta["page"])
            query["page"] = curr_page + 1
            query["limit"] = meta["limit"]

            features = list(itertools.chain(features, fetch_sat_api(query)))

        return features

    features = fetch_sat_api(query)
    if not features:
        raise Exception(f"No asset found for query '{json.dumps(query)}'")

    logger.debug(f"Found: {len(features)} scenes")

    features = list(
        filter(
            lambda x: _get_season(
                x["properties"]["datetime"], max(x["bbox"][1], x["bbox"][3])
            )
            in seasons,
            features,
        )
    )

    if optimized_selection:
        dataset = []
        prs = []
        for item in features:
            pr = item["properties"]["eo:column"] + "-" + item["properties"]["eo:row"]
            if pr not in prs:
                prs.append(pr)
                dataset.append(item)
    else:
        dataset = features

    if query.get("bbox"):
        bounds = query["bbox"]
    else:
        bounds = burntiles.find_extrema(dataset)

    for i in range(len(dataset)):
        dataset[i]["geometry"] = shape(dataset[i]["geometry"])

    tiles = burntiles.burn([bbox_to_geojson(bounds)], minzoom)
    tiles = list(set(["{2}-{0}-{1}".format(*tile.tolist()) for tile in tiles]))

    logger.debug(f"Number tiles: {len(tiles)}")

    mosaic_definition = dict(
        mosaicjson="0.0.1",
        minzoom=minzoom,
        maxzoom=maxzoom,
        bounds=bounds,
        center=[(bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2, minzoom],
        tiles={},
    )

    for tile in tiles:
        z, x, y = list(map(int, tile.split("-")))
        tile = mercantile.Tile(x=x, y=y, z=z)
        quadkey = mercantile.quadkey(*tile)
        geometry = box(*mercantile.bounds(tile))
        intersect_dataset = list(
            filter(lambda x: geometry.intersects(x["geometry"]), dataset)
        )
        if len(intersect_dataset):
            # We limit the item per quadkey to 20
            if maximum_items_per_tile:
                intersect_dataset = intersect_dataset[0:maximum_items_per_tile]

            mosaic_definition["tiles"][quadkey] = [
                scene["properties"]["landsat:product_id"] for scene in intersect_dataset
            ]

    return mosaic_definition
