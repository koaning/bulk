import shutil
import pathlib
import tarfile
import urllib.request
import typer


app = typer.Typer(
    name="download",
    add_completion=False,
    help="Download datasets.",
    no_args_is_help=True,
)


@app.command("twemoji")
def twemoji(force: bool = typer.Option(False, help="Force the download", is_flag=True)):
    """
    Download images of twemoji.

    This dataset reprents a snapshot of the emoji that Twitter uses.
    It can originally be found here: https://github.com/twitter/twemoji

    More information can be found on their documentation:
    https://twemoji.twitter.com/

    Once downloaded, you'll find these images in the `downloads` folder of the current dir.
    """
    src = pathlib.Path("downloads/twemoji/twemoji.tgz")
    if not force and src.parent.exists():
        print("The twemoji dataset already exists")
        raise typer.Exit(1)
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/twemoji")

    # Download and untar
    url = "https://github.com/koaning/bulk-datasets/raw/main/twemoji.tar.gz"
    urllib.request.urlretrieve(url, str(src))
    with tarfile.open(str(src), "r:gz") as tar:
        tar.extractall(str(dst))
    src.unlink()


@app.command("pets")
def pets(force: bool = typer.Option(False, help="Force the download", is_flag=True)):
    """
    Download images of pets.

    This dataset contains photos of 39 breeds of pets.

    The dataset is a subset of the original Oxford repository, here:
    https://www.robots.ox.ac.uk/~vgg/data/pets/

    Once downloaded, you'll find these images in the `downloads` folder of the current dir.
    """
    src = pathlib.Path("downloads/pets/pets.tgz")
    if not force and src.parent.exists():
        print("The pets dataset already exists")
        raise typer.Exit(1)
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/pets")

    # Download and untar
    url = "https://github.com/koaning/bulk-datasets/raw/main/pets.tar.gz"
    urllib.request.urlretrieve(url, str(src))
    with tarfile.open(str(src), "r:gz") as tar:
        tar.extractall(str(dst))
    src.unlink()


@app.command("fruits")
def fruits(force: bool = typer.Option(False, help="Force the download", is_flag=True)):
    """
    Download images of fruit.

    The dataset contains pictures of 360 degree fruits images

    It is a small subset of a dataset that was originally found as part of a Kaggle dataset, found here:
    https://www.kaggle.com/datasets/moltean/fruits

    Once downloaded, you'll find these images in the `downloads` folder of the current dir.
    """
    src = pathlib.Path("downloads/fruits/fruits.tgz")
    if not force and src.parent.exists():
        print("The fruits dataset already exists")
        raise typer.Exit(1)
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/fruits")

    # Download and untar
    url = "https://github.com/koaning/bulk-datasets/raw/main/fruits.tar.gz"
    urllib.request.urlretrieve(url, str(src))
    with tarfile.open(str(src), "r:gz") as tar:
        tar.extractall(str(dst))
    src.unlink()
