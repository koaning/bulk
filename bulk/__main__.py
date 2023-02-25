import itertools as it
import json
import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import List, Literal

from bokeh.server.server import Server
from bokeh.util.browser import view
from radicli import Arg, Radicli
from tornado.ioloop import IOLoop
from wasabi import msg

from bulk._bokeh_utils import read_file, save_file
from bulk.cli.download import download_fruits, download_pets, download_twemoji
from bulk.cli.image import bulk_images
from bulk.cli.text import bulk_text

cli = Radicli(help="Bulk: Tools for bulk labelling.")


@cli.command(
    "text",
    path=Arg(help="path to .csv/.jsonl file"),
    keywords=Arg("--keywords", help="comma seperated string of terms to highlight"),
    port=Arg("--port", help="port number"),
    download=Arg("--download", help="save button turns into download button"),
)
def text(
    path: Path,
    keywords: str = None,
    port: int = 5006,
    download: bool = False,
):
    """Bulk labelling interface for text."""
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


@cli.command(
    "image",
    path=Arg(help="path to .csv/.jsonl file"),
    port=Arg("--port", help="port number"),
    download=Arg("--download", help="save button turns into download button"),
)
def image(
    path: Path,
    port: int = 5006,
    download: bool = False,
):
    """Bulk labelling interface for images."""
    if not path.exists():
        msg.fail(f"Path {str(path)} does not exist.", exits=True, spaced=True)
    server = Server(
        {"/": bulk_images(path, download=download)},
        io_loop=IOLoop(),
        port=port,
    )
    server.start()
    host = f"http://localhost:{port}/"
    msg.good(f"About to serve `bulk` over at {host}.", spaced=True)
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


@cli.command(
    "download",
    dataset=Arg(help="Name of the dataset to download"),
    force=Arg("--force", help="Download even when local files seem present"),
)
def download(
    dataset: Literal["twemoji", "pets", "fruits"],
    force: bool = False,
):
    """Utility to download demo datasets."""
    lookup = {
        "twemoji": download_twemoji,
        "pets": download_pets,
        "fruits": download_fruits,
    }
    lookup[dataset](force=force)


@cli.subcommand("util", "info")
def info():
    """Prints version information for debugging."""
    versions = {}
    pkgs = ["bokeh", "embetter", "pandas", "spacy", "radicli", "tqdm"]
    for pkg in pkgs:
        try:
            versions[pkg] = version(pkg)
        except PackageNotFoundError:
            pass
    msg.divider(f"Info for bulk v{version('bulk')}")
    msg.info("OS & Python", spaced=True)
    print(f"Location={str(Path(__file__).parent.parent)}")
    print(f"Platform={platform.platform()}")
    print(f"Python={platform.python_version()}")
    msg.info("Dependencies", spaced=True)
    packge_info = "\n".join([f"{k}={v}" for k, v in versions.items()])
    print(packge_info)
    print(" ")


# fmt: off
@cli.subcommand("util", "to-phrases",
    file_in=Arg(help="A .jsonl file with texts"),
    file_out=Arg(help="Output file for phrases. Will print if not provided."),
    model=Arg("--model", help="spaCy model to load"),
    n=Arg("--n", help="Only consider top `n` texts."),
    keep_det=Arg("--keep-det", help="Keep the determinant in the phrase."),
)
# fmt: on
def extract_phrases(
    file_in: Path, file_out: Path, model: str, n: int = None, keep_det: bool = False
):
    """Turns a `.jsonl` with text into a `.jsonl` with phrases.

    Note! spaCy needs to be installed with an available model
    """
    # fmt: off
    import spacy
    import srsly
    import tqdm

    # fmt: on

    def _fetch_phrases(stream, nlp, keep_det=False):
        for doc in nlp.pipe(stream):
            for chunk in doc.noun_chunks:
                if keep_det:
                    yield {"text": chunk.text}
                else:
                    yield {"text": " ".join([t.text for t in chunk if t.pos_ != "DET"])}

    stream = (ex["text"] for ex in srsly.read_jsonl(file_in))
    stream_copy, stream = it.tee(stream)
    total = sum(1 for _ in stream_copy)
    stream = tqdm.tqdm(stream, total=total)
    if n:
        stream = it.islice(stream, n)
    nlp = spacy.load(model, disable=["ents"])
    stream = _fetch_phrases(stream, nlp, keep_det=keep_det)
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for ex in stream:
            print(json.dumps(ex))


@cli.subcommand(
    "util",
    "resize",
    file_in=Arg(help="A file with original image paths in it."),
    file_out=Arg(help="New file with replaced thumbnail image paths in it."),
    folder_out=Arg(help="Output folder for thumbnails."),
    size=Arg("--size", help="Image size"),
)
def resize(file_in: Path, file_out: Path, folder_out: Path, size: str = "200x200"):
    """Resize images into lightweight thumbnails."""
    from PIL import Image

    folder_out.mkdir(exist_ok=True, parents=True)
    size_tup = tuple(int(i) for i in size.split("x"))

    df, _, orig_cols = read_file(file_in)

    filepaths = []
    for row in df.itertuples():
        with Image.open(row.path) as im:
            file_name = row.path.split("/")[-1]
            file_name = file_name.split(".")[0]
            im.thumbnail(size_tup)
            filepath = folder_out / f"{file_name}_{size}.jpeg"
            im.save(filepath, format="JPEG")
            filepaths.append(str(filepath))

    df["path"] = filepaths
    save_file(df, df.index, file_out, orig_cols=orig_cols)


if __name__ == "__main__":
    cli.run()
