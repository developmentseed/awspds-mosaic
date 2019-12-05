"""awspds-mosaic.landsat.handlers.web: web pages."""

from typing import Tuple

import os
from awspds_mosaic.landsat.templates import landsatlive, timeserie

from lambda_proxy.proxy import API

app = API(name="awspds-mosaic-landsat-web", add_docs=False)


@app.route("/", methods=["GET"], cors=True, tag=["landing page"])
@app.route("/index.html", methods=["GET"], cors=True, tag=["landing page"])
def _landsatlive() -> Tuple[str, str, str]:
    """
    Handle / requests.

    Returns
    -------
    status : str
        Status of the request (e.g. OK, NOK).
    MIME type : str
        response body MIME type (e.g. application/json).
    body : str
        String encoded html

    """
    return (
        "OK",
        "text/html",
        landsatlive(app.host, os.environ.get("MAPBOX_ACCESS_TOKEN", "")),
    )


@app.route("/timeserie.html", methods=["GET"], cors=True, tag=["landing page"])
def _timeserie() -> Tuple[str, str, str]:
    """
    Handle / requests.

    Returns
    -------
    status : str
        Status of the request (e.g. OK, NOK).
    MIME type : str
        response body MIME type (e.g. application/json).
    body : str
        String encoded html

    """
    return (
        "OK",
        "text/html",
        timeserie(app.host, os.environ.get("MAPBOX_ACCESS_TOKEN", "")),
    )


@app.route("/favicon.ico", methods=["GET"], cors=True, tag=["other"])
def favicon() -> Tuple[str, str, str]:
    """Favicon."""
    return ("EMPTY", "text/plain", "")
