import pathlib

import typer
from bokeh.server.server import Server
from bokeh.util.browser import view
from tornado.ioloop import IOLoop
from typer.core import TyperGroup
from wasabi import msg

from bulk.cli.download import app as download_app
from bulk.cli.image import bulk_images
from bulk.cli.text import bulk_text
from bulk.cli.util import app as util_app
from radicli import Radicli, Arg

cli = Radicli(help="Bulk: Tools for bulk labelling.")

# app.add_typer(download_app, name="download")
# app.add_typer(util_app, name="util")


@cli.command(
    "text",
    path=Arg(help="path to .csv/.jsonl file"),
    keywords=Arg("--keywords", help="comma seperated string of terms to highlight"),
    port=Arg("--port", help="port number"),
    download=Arg("--download", help="save button turns into download button"),
)
def text(
    path: pathlib.Path,
    keywords: str = None,
    port: int = 5006,
    download: bool = False,
):
    """Bulk labelling interface for text."""
    if not path.exists():
        msg.fail(f"Path {str(path)} does not exist.", exits=True, spaced=True)
    if keywords:
        keywords = keywords.split(",")
    server = Server(
        {"/": bulk_text(path, keywords=keywords, download=download)},
        io_loop=IOLoop(),
        port=port,
    )
    server.start()
    host = f"http://localhost:{port}/"
    msg.good(f"About to serve `bulk` over at {host}.", spaced=True)
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


@cli.command(
    "image",
    path=Arg(help="path to .csv/.jsonl file"),
    port=Arg("--port", help="port number"),
    download=Arg("--download", help="save button turns into download button"),
)
def image(
    path: pathlib.Path,
    port: int = 5006,
    download: bool = False,
):
    """Bulk labelling interface for images."""
    if not path.exists():
        msg.fail(f"Path {str(path)} does not exist.", exits=True, spaced=True)
    server = Server(
        {"/": bulk_images(path, download=download)}, io_loop=IOLoop(), port=port
    )
    server.start()
    host = f"http://localhost:{port}/"
    msg.good(f"About to serve `bulk` over at {host}.", spaced=True)
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


if __name__ == "__main__":
    cli.run()
