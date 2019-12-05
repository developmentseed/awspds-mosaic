"""Test awspds_mosaic locally."""

import click
import base64

from socketserver import ThreadingMixIn

from urllib.parse import urlparse, parse_qsl
from http.server import HTTPServer, BaseHTTPRequestHandler

from awspds_mosaic.landsat.handlers.mosaic import app as app_mosaic
from awspds_mosaic.landsat.handlers.tiles import app as app_tiles
from awspds_mosaic.landsat.handlers.web import app

app.https = False
app_tiles.https = False
app_mosaic.https = False


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """MultiThread."""

    pass


class Handler(BaseHTTPRequestHandler):
    """Requests handler."""

    def do_GET(self):
        """Get requests."""
        q = urlparse(self.path)
        pathParameters = {}
        if q.path.startswith("/tiles/"):
            application = app_tiles
            resource = "/tiles/{proxy+}"
            pathParameters = {"proxy": q.path.replace("/tiles/", "")}
        elif q.path.startswith("/mosaic/"):
            application = app_mosaic
            resource = "/mosaic/{proxy+}"
            pathParameters = {"proxy": q.path.replace("/mosaic/", "")}
        else:
            resource = "/"
            application = app

        request = {
            "resource": resource,
            "pathParameters": pathParameters,
            "headers": dict(self.headers),
            "path": q.path,
            "queryStringParameters": dict(parse_qsl(q.query)),
            "httpMethod": self.command,
        }
        response = application(request, None)

        self.send_response(int(response["statusCode"]))
        for r in response["headers"]:
            self.send_header(r, response["headers"][r])
        self.end_headers()

        if response.get("isBase64Encoded"):
            response["body"] = base64.b64decode(response["body"])

        if isinstance(response["body"], str):
            self.wfile.write(bytes(response["body"], "utf-8"))
        else:
            self.wfile.write(response["body"])

    def do_POST(self):
        """POST requests."""
        body = self.rfile.read(int(dict(self.headers).get("Content-Length")))
        body = base64.b64encode(body).decode()

        q = urlparse(self.path)
        pathParameters = {}
        if q.path.startswith("/tiles/"):
            application = app_tiles
            resource = "/tiles/{proxy+}"
            pathParameters = {"proxy": q.path.replace("/tiles/", "")}
        elif q.path.startswith("/mosaic/"):
            application = app_mosaic
            resource = "/mosaic/{proxy+}"
            pathParameters = {"proxy": q.path.replace("/mosaic/", "")}
        else:
            resource = "/"
            application = app

        request = {
            "resource": resource,
            "pathParameters": pathParameters,
            "headers": dict(self.headers),
            "path": q.path,
            "queryStringParameters": dict(parse_qsl(q.query)),
            "body": body,
            "httpMethod": self.command,
            "isBase64Encoded": True,
        }

        response = application(request, None)

        self.send_response(int(response["statusCode"]))
        for r in response["headers"]:
            self.send_header(r, response["headers"][r])
        self.end_headers()
        if isinstance(response["body"], str):
            self.wfile.write(bytes(response["body"], "utf-8"))
        else:
            self.wfile.write(response["body"])


@click.command(short_help="Local Server")
@click.option("--port", type=int, default=8000, help="port")
def run(port):
    """Launch server."""
    server_address = ("", port)
    httpd = ThreadingSimpleServer(server_address, Handler)
    click.echo(f"Starting local server at http://127.0.0.1:{port}", err=True)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
