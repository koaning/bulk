import pathlib
import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import List

import pandas as pd
import typer
from wasabi import msg

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


@app.command("info")
def info():
    """Prints information useful for debugging."""
    versions = {}
    pkgs = ["bokeh", "embetter", "pandas"]
    for pkg in pkgs:
        try:
            versions[pkg] = version(pkg)
        except PackageNotFoundError as e:
            pass
    msg.divider(f"Info for bulk v{version('bulk')}")
    msg.info(f"OS & Python", spaced=True)
    print(f"Location={str(Path(__file__).parent.parent)}")
    print(f"Platform={platform.platform()}")
    print(f"Python={platform.python_version()}")
    msg.info(f"Dependencies", spaced=True)
    packge_info = "\n".join([f"{pkg}={version(pkg)}" for pkg in ["bokeh", "embetter"]])
    print(packge_info)
    print(" ")
