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


@app.command("tinyplanet")
def concat(force: bool = typer.Option(False, help="Force the download", is_flag=True)):
    """Download the tiny planet dataset."""
    src = pathlib.Path("downloads/tinyplanet/tinyplanet.tgz")
    if not force and src.exists():
        print("The tinyplanet dataset already exists")
        return 1
    src.parent.mkdir(exist_ok=True, parents=True)
    dst = pathlib.Path("downloads/tinyplanet")
    urllib.request.urlretrieve("https://s3.amazonaws.com/fast-ai-sample/planet_tiny.tgz", str(src))
    with tarfile.open(str(src), 'r:gz') as tar:
        tar.extractall(str(dst))
