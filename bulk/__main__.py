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


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()


app = typer.Typer(
    name="bulk",
    add_completion=False,
    help="Tools for bulk labelling.",
    no_args_is_help=True,
    cls=NaturalOrderGroup,
)
app.add_typer(download_app, name="download")
app.add_typer(util_app, name="util")


@app.command("text")
def text(
    # fmt: off
    path: pathlib.Path = typer.Argument(..., help="Path to .csv/.jsonl file"),
    keywords: str = typer.Option(None, help="Keywords to highlight"),
    port: int = typer.Option(5006, help="Port number"),
    download: bool = typer.Option(False, help="Save button turns into download button", is_flag=True),
    # fmt: on
):
    """Bulk Labelling for Text"""
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


@app.command("image")
def image(
    # fmt: off
    path: pathlib.Path = typer.Argument(..., help="Path to .csv/.jsonl file", exists=True),
    port: int = typer.Option(5006, help="Port number"),
    download: bool = typer.Option(False, help="Save button turns into download button", is_flag=True),
    # fmt: on
):
    """Bulk Labelling for Images"""
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
    app()
