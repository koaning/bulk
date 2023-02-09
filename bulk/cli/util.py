import pathlib
from PIL import Image
from typing import List
import glob
import os

import pandas as pd
import typer

from bulk._bokeh_utils import read_file

app = typer.Typer(
    name="util",
    add_completion=False,
    help="Extra utilities.",
    no_args_is_help=True,
)


@app.command("concat")
def concat(
    paths: List[pathlib.Path] = typer.Argument(
        ..., help="Paths to .csv files", exists=True
    ),
    out: pathlib.Path = typer.Option(..., help="Name of output csv."),
    shuffle: bool = typer.Option(False, help="Keywords to highlight", is_flag=True),
):
    """Concatenates csv files into single file."""
    df = pd.concat([pd.read_csv(f) for f in paths])
    if shuffle:
        df = df.sample(frac=1)
    df.drop_duplicates().to_csv(out, index=False)

@app.command("resize")
def resize(
        path: pathlib.Path = typer.Argument(..., help="Path to .csv/.jsonl file", exists=True),
        thumbnail_paths: pathlib.Path = typer.Argument(..., help="Path to folder to store thumbnails.", exists=False)):
    """Resize the images into thumbnails."""

    os.system(f"mkdir {thumbnail_paths}")
    df, colormap, orig_cols = read_file(path, do_encoding = False)
    
    for row in df.itertuples():
        with Image.open(row.path) as im:
            file_name = row.path.split('/')[-1]
            file_name = file_name.split('.')[0] #remove extension
            im.thumbnail((200,200))
            im.save(f'{thumbnail_paths}/{file_name}_thumbnail.jpeg', format='JPEG')
    
