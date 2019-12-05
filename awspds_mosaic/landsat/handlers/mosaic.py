"""awspds_mosaic.handlers.mosaics: create mosaics."""

from typing import Any, Tuple

import os
import json
import urllib

import mercantile

from awspds_mosaic.utils import _compress_gz_json, _aws_put_data, get_mosaic_content
from awspds_mosaic.landsat.stac import stac_to_mosaicJSON

from loguru import logger

from lambda_proxy.proxy import API
from lambda_proxy_cache.proxy import get_hash

app = API(name="awspds-mosaic-landsat-mosaic", debug=True)


@app.route("/create", methods=["POST"], cors=True, tag=["mosaic"])
def create(
    body: str,
    minzoom: int = 7,
    maxzoom: int = 12,
    optimized_selection: bool = False,
    maximum_items_per_tile: int = 20,
    stac_collection_limit: int = 500,
    seasons: str = None,
    tile_format: str = "png",
    tile_scale: int = 1,
    **kwargs: Any,
) -> Tuple[str, str, str]:
    """Handle /create requests."""
    body = json.loads(body)
    logger.debug(body)

    minzoom = int(minzoom) if isinstance(minzoom, str) else minzoom
    maxzoom = int(maxzoom) if isinstance(maxzoom, str) else maxzoom
    if isinstance(optimized_selection, str):
        optimized_selection = (
            False if optimized_selection in ["False", "false"] else True
        )

    if seasons:
        seasons = seasons.split(",")
    else:
        seasons = ["spring", "summer", "autumn", "winter"]

    maximum_items_per_tile = (
        int(maximum_items_per_tile)
        if isinstance(maximum_items_per_tile, str)
        else maximum_items_per_tile
    )
    stac_collection_limit = (
        int(stac_collection_limit)
        if isinstance(stac_collection_limit, str)
        else stac_collection_limit
    )

    mosaicid = get_hash(
        body=body,
        minzoom=minzoom,
        maxzoom=maxzoom,
        optimized_selection=optimized_selection,
        maximum_items_per_tile=maximum_items_per_tile,
        stac_collection_limit=stac_collection_limit,
        seasons=seasons,
    )

    logger.debug(f"Mosaic id: {mosaicid}")
    try:
        bucket = os.environ["MOSAIC_DEF_BUCKET"]
        url = f"s3://{bucket}/mosaics/{mosaicid}.json.gz"
        mosaic_definition = get_mosaic_content(url)
    except Exception:
        body["query"].update({"eo:platform": {"eq": "landsat-8"}})

        mosaic_definition = stac_to_mosaicJSON(
            body,
            minzoom=minzoom,
            maxzoom=maxzoom,
            optimized_selection=optimized_selection,
            maximum_items_per_tile=maximum_items_per_tile,
            stac_collection_limit=stac_collection_limit,
            seasons=seasons,
        )

        key = f"mosaics/{mosaicid}.json.gz"
        bucket = os.environ["MOSAIC_DEF_BUCKET"]
        _aws_put_data(key, bucket, _compress_gz_json(mosaic_definition))

    qs = urllib.parse.urlencode(list(kwargs.items()))
    tile_url = f"{app.host}/tiles/{mosaicid}/{{z}}/{{x}}/{{y}}@{tile_scale}x.{tile_format}?{qs}"

    meta = {
        "bounds": mosaic_definition["bounds"],
        "center": mosaic_definition["center"],
        "maxzoom": mosaic_definition["maxzoom"],
        "minzoom": mosaic_definition["minzoom"],
        "name": mosaicid,
        "tilejson": "2.1.0",
        "tiles": [tile_url],
    }

    return ("OK", "application/json", json.dumps(meta))


@app.route(
    "/<regex([0-9A-Fa-f]{56}):mosaicid>.json",
    methods=["GET"],
    cors=True,
    tag=["mosaic"],
)
def info(mosaicid: str) -> Tuple[str, str, str]:
    """Handle /create requests."""
    bucket = os.environ["MOSAIC_DEF_BUCKET"]
    url = f"s3://{bucket}/mosaics/{mosaicid}.json.gz"
    mosaic_definition = get_mosaic_content(url)
    return ("OK", "application/json", json.dumps(mosaic_definition))


@app.route(
    "/<regex([0-9A-Fa-f]{56}):mosaicid>/geojson",
    methods=["GET"],
    cors=True,
    payload_compression_method="gzip",
    binary_b64encode=True,
    tag=["metadata"],
)
def _get_geojson(mosaicid: str = None, url: str = None) -> Tuple[str, str, str]:
    """
    Handle /geojson requests.

    Attributes
    ----------
    url : str, required
        Mosaic definition url.

    Returns
    -------
    status : str
        Status of the request (e.g. OK, NOK).
    MIME type : str
        response body MIME type (e.g. application/json).
    body : str
        String encoded JSON metata

    """
    bucket = os.environ["MOSAIC_DEF_BUCKET"]
    url = f"s3://{bucket}/mosaics/{mosaicid}.json.gz"
    mosaic_definition = get_mosaic_content(url)

    geojson = {
        "type": "FeatureCollection",
        "features": [
            mercantile.feature(
                mercantile.quadkey_to_tile(qk), props=dict(quadkey=qk, files=files)
            )
            for qk, files in mosaic_definition["tiles"].items()
        ],
    }

    return ("OK", "application/json", json.dumps(geojson))


@app.route("/favicon.ico", methods=["GET"], cors=True, tag=["other"])
def favicon() -> Tuple[str, str, str]:
    """Favicon."""
    return ("EMPTY", "text/plain", "")
