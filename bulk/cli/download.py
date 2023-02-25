import pathlib
import tarfile
import urllib.request

from wasabi import msg


def _download_and_untar(url, src, dst):
    urllib.request.urlretrieve(url, str(src))
    with tarfile.open(str(src), "r:gz") as tar:
        tar.extractall(str(dst))
    src.unlink()


def download_twemoji(force: bool = False):
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
        msg.good("The twemoji dataset already exists", spaced=True, exits=1)
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/twemoji")

    # Download and untar
    url = "https://github.com/koaning/bulk-datasets/raw/main/twemoji.tar.gz"
    _download_and_untar(url=url, src=src, dst=dst)


def download_pets(force: bool = False):
    """
    Download images of pets.

    This dataset contains photos of 39 breeds of pets.

    The dataset is a subset of the original Oxford repository, here:
    https://www.robots.ox.ac.uk/~vgg/data/pets/

    Once downloaded, you'll find these images in the `downloads` folder of the current dir.
    """
    src = pathlib.Path("downloads/pets/pets.tgz")
    if not force and src.parent.exists():
        msg.good("The pets dataset already exists", spaced=True, exits=1)
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/pets")

    # Download and untar
    url = "https://github.com/koaning/bulk-datasets/raw/main/pets.tar.gz"
    _download_and_untar(url=url, src=src, dst=dst)


def download_fruits(force: bool = False):
    """
    Download images of fruit.

    The dataset contains pictures of 360 degree fruits images

    It is a small subset of a dataset that was originally found as part of a Kaggle dataset, found here:
    https://www.kaggle.com/datasets/moltean/fruits

    Once downloaded, you'll find these images in the `downloads` folder of the current dir.
    """
    src = pathlib.Path("downloads/fruits/fruits.tgz")
    if not force and src.parent.exists():
        msg.good("The fruits dataset already exists", spaced=True, exits=1)
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/fruits")

    # Download and untar
    url = "https://github.com/koaning/bulk-datasets/raw/main/fruits.tar.gz"
    _download_and_untar(url=url, src=src, dst=dst)
