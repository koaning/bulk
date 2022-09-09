import pathlib 
from typing import List

import typer
import pandas as pd

from ._download import download_tinyplanet


app = typer.Typer(
    name="util",
    add_completion=False,
    help="Utilities for data.",
    no_args_is_help=True,
)


@app.command("concat")
def concat(paths: List[pathlib.Path] = typer.Argument(..., help="Paths to .csv files", exists=True),
           out: pathlib.Path = typer.Option(..., help="Name of output csv."),
           shuffle: bool = typer.Option(False, help="Keywords to highlight", is_flag=True)):
    """Concatenates csv files into single file."""
    df = pd.concat([pd.read_csv(f) for f in paths])
    if shuffle:
        df = df.sample(frac=1)
    df.drop_duplicates().to_csv(out, index=False)


@app.command("download")
def concat(name: str = typer.Argument(..., help="Name of dataset to download. Can be `tinyplanet` or `clinc`."),
           force: bool = typer.Option(False, help="Force the download", is_flag=True)):
    """Downloads files to play with."""
    allowed = ["tinyplanet", "clinc"]
    if name not in allowed:
        raise typer.Exit(f"Dataset name must be either {'/'.join(['tinyplanet', 'clinc'])}.")
    if name == "tinyplanet":
        download_tinyplanet(force=force)
