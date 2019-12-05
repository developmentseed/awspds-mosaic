"""awspds_mosaic.utils: utility functions."""

from typing import Dict, BinaryIO, Tuple

import os
import zlib
import json
import functools
import itertools
from urllib.parse import urlparse

import requests
from boto3.session import Session as boto3_session

import numpy

import mercantile
from rio_tiler.utils import linear_rescale
from rio_color.utils import scale_dtype, to_math_type
from rio_color.operations import parse_operations


def _decompress_gz(gzip_buffer: BinaryIO) -> str:
    return zlib.decompress(gzip_buffer, zlib.MAX_WBITS | 16).decode()


def _compress_gz_json(data: str) -> BinaryIO:
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)

    return (
        gzip_compress.compress(json.dumps(data).encode("utf-8")) + gzip_compress.flush()
    )


def _aws_put_data(key: str, bucket: str, body: BinaryIO, options: Dict = {}) -> str:
    session = boto3_session()
    s3 = session.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=body, **options)
    return key


def _aws_get_data(key: str, bucket: str) -> BinaryIO:
    session = boto3_session()
    s3 = session.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def post_process_tile(
    tile: numpy.ndarray,
    mask: numpy.ndarray,
    rescale: str = None,
    color_formula: str = None,
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Tile data post processing."""
    if rescale:
        rescale_arr = (tuple(map(float, rescale.split(","))),) * tile.shape[0]
        for bdx in range(tile.shape[0]):
            tile[bdx] = numpy.where(
                mask,
                linear_rescale(
                    tile[bdx], in_range=rescale_arr[bdx], out_range=[0, 255]
                ),
                0,
            )
        tile = tile.astype(numpy.uint8)

    if color_formula:
        if issubclass(tile.dtype.type, numpy.floating):
            tile = tile.astype(numpy.int16)

        # make sure one last time we don't have
        # negative value before applying color formula
        tile[tile < 0] = 0
        for ops in parse_operations(color_formula):
            tile = scale_dtype(ops(to_math_type(tile)), numpy.uint8)

    return tile


def bbox_to_geojson(bbox: Tuple) -> Dict:
    """Return bbox geojson feature."""
    return {
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [bbox[0], bbox[3]],
                    [bbox[0], bbox[1]],
                    [bbox[2], bbox[1]],
                    [bbox[2], bbox[3]],
                    [bbox[0], bbox[3]],
                ]
            ],
        },
        "properties": {},
        "type": "Feature",
    }


def get_mosaic_content(url: str) -> Dict:
    """Get Mosaic document."""
    url_info = urlparse(url)

    if url_info.scheme == "s3":
        bucket = url_info.netloc
        key = url_info.path.strip("/")
        body = _aws_get_data(key, bucket)

    elif url_info.scheme in ["http", "https"]:
        # use requests
        body = requests.get(url)
        body = body.content

    else:
        with open(url, "rb") as f:
            body = f.read()

    if url.endswith(".gz"):
        body = _decompress_gz(body)

    if isinstance(body, dict):
        return body
    else:
        return json.loads(body)


@functools.lru_cache(maxsize=512)
def fetch_mosaic_definition(url: str) -> Dict:
    """Get Mosaic definition info."""
    return get_mosaic_content(url)


def get_assets(url: str, x: int, y: int, z: int) -> Tuple[str]:
    """Get assets."""
    mosaic_def = fetch_mosaic_definition(url)
    min_zoom = mosaic_def["minzoom"]
    max_zoom = mosaic_def["maxzoom"]
    if z > max_zoom or z < min_zoom:
        return []  # return empty asset

    mercator_tile = mercantile.Tile(x=x, y=y, z=z)
    quadkey_zoom = mosaic_def.get("quadkey_zoom", min_zoom)  # 0.0.2

    # get parent
    if mercator_tile.z > quadkey_zoom:
        depth = mercator_tile.z - quadkey_zoom
        for i in range(depth):
            mercator_tile = mercantile.parent(mercator_tile)
        quadkey = [mercantile.quadkey(*mercator_tile)]

    # get child
    elif mercator_tile.z < quadkey_zoom:
        depth = quadkey_zoom - mercator_tile.z
        mercator_tiles = [mercator_tile]
        for i in range(depth):
            mercator_tiles = sum([mercantile.children(t) for t in mercator_tiles], [])

        mercator_tiles = list(filter(lambda t: t.z == quadkey_zoom, mercator_tiles))
        quadkey = [mercantile.quadkey(*tile) for tile in mercator_tiles]
    else:
        quadkey = [mercantile.quadkey(*mercator_tile)]

    assets = list(
        itertools.chain.from_iterable(
            [mosaic_def["tiles"].get(qk, []) for qk in quadkey]
        )
    )

    # check if we have a mosaic in the url (.json/.gz)
    return list(
        itertools.chain.from_iterable(
            [
                get_assets(asset, x, y, z)
                if os.path.splitext(asset)[1] in [".json", ".gz"]
                else [asset]
                for asset in assets
            ]
        )
    )
