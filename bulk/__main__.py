import pathlib

import typer
from typer.core import TyperGroup
from bokeh.server.server import Server
from bokeh.util.browser import view
from tornado.ioloop import IOLoop

from bulk.cli.text import bulk_text
from bulk.cli.image import bulk_images
from bulk.cli.util import app as util_app
from bulk.cli.download import app as download_app


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
    path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True),
    keywords: str = typer.Option(None, help="Keywords to highlight"),
    port: int = typer.Option(5006, help="Port number"),
):
    """Bulk Labelling for Text"""
    if keywords:
        keywords = keywords.split(",")
    server = Server(
        {"/": bulk_text(path, keywords=keywords)}, io_loop=IOLoop(), port=port
    )
    server.start()
    host = f"http://localhost:{port}/"
    print(f"About to serve `bulk` over at {host}.")
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


@app.command("image")
def image(
    path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True),
    port: int = typer.Option(5006, help="Port number"),
):
    """Bulk Labelling for Images"""
    server = Server({"/": bulk_images(path)}, io_loop=IOLoop(), port=port)
    server.start()
    host = f"http://localhost:{port}/"
    print(f"About to serve `bulk` over at {host}.")
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


if __name__ == "__main__":
    app()
