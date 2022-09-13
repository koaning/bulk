import shutil
import pathlib
import pandas as pd
import tarfile
import urllib.request
import typer


app = typer.Typer(
    name="download",
    add_completion=False,
    help="Download datasets.",
    no_args_is_help=True,
)


@app.command("tinyplanet")
def concat(force: bool = typer.Option(False, help="Force the download", is_flag=True)):
    """Download the tiny planet dataset."""
    src = pathlib.Path("downloads/tinyplanet/tinyplanet.tgz")
    if not force and src.parent.exists():
        print("The tinyplanet dataset already exists")
        return 1
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/tinyplanet")
    
    # Download and untar
    urllib.request.urlretrieve("https://s3.amazonaws.com/fast-ai-sample/planet_tiny.tgz", str(src))
    with tarfile.open(str(src), 'r:gz') as tar:
        tar.extractall(str(dst))
    src.unlink()

    # Move files into nice positions
    glob = pathlib.Path("downloads/tinyplanet/planet_tiny/train").glob("*.jpg")
    pathlib.Path("downloads/tinyplanet/images").mkdir(exist_ok=True, parents=True)
    for file in glob:
        file.rename(f"downloads/tinyplanet/images/{file.name}")

    # Move the labels file 
    (pd.read_csv("downloads/tinyplanet/planet_tiny/labels.csv")
      .assign(image=lambda d: d['image_name'].str.replace("train_", ""))
      .drop(columns=["image_name"])
      .to_csv("downloads/tinyplanet/labels.csv", index=False))

    shutil.rmtree("downloads/tinyplanet/planet_tiny")
