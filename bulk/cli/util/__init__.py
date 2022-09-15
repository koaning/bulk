import pathlib 
from typing import List

import typer
import pandas as pd
from bulk.cli.util.download import app as download_app

app = typer.Typer(
    name="util",
    add_completion=False,
    help="Extra utilities.",
    no_args_is_help=True,
)
app.add_typer(download_app, name="download")


@app.command("concat")
def concat(paths: List[pathlib.Path] = typer.Argument(..., help="Paths to .csv files", exists=True),
           out: pathlib.Path = typer.Option(..., help="Name of output csv."),
           shuffle: bool = typer.Option(False, help="Keywords to highlight", is_flag=True)):
    """Concatenates csv files into single file."""
    df = pd.concat([pd.read_csv(f) for f in paths])
    if shuffle:
        df = df.sample(frac=1)
    df.drop_duplicates().to_csv(out, index=False)
