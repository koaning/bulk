import pathlib 

import typer 
from tornado.ioloop import IOLoop
from bokeh.util.browser import view
from bokeh.server.server import Server

from bulk.text import bulk_text


app = typer.Typer(
    name="bulk",
    add_completion=False,
    help="Tools for bulk labelling.",
    no_args_is_help=True,
)

@app.command("version")
def version():
    print("0.1.0")

@app.command("text")
def text(path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True)):
    """Bulk Labelling for Text"""
    server = Server({"/": bulk_text(path)}, io_loop=IOLoop())
    server.start()
    
    server.io_loop.add_callback(view, "http://localhost:5006/")
    server.io_loop.start()

if __name__ == '__main__':
    app()