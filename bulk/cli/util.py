import itertools as it
import json
import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import List

import pandas as pd
from wasabi import msg


def concat(
    paths: List[Path] = typer.Argument(..., help="Paths to .csv files", exists=True),
    out: Path = typer.Option(..., help="Name of output csv."),
    shuffle: bool = typer.Option(False, help="Keywords to highlight", is_flag=True),
):
    """Concatenates csv files into single file."""
    df = pd.concat([pd.read_csv(f) for f in paths])
    if shuffle:
        df = df.sample(frac=1)
    df.drop_duplicates().to_csv(out, index=False)


def _fetch_phrases(stream, nlp, keep_det=False):
    for doc in nlp.pipe(stream):
        for chunk in doc.noun_chunks:
            if keep_det:
                yield {"text": chunk.text}
            else:
                yield {"text": " ".join([t.text for t in chunk if t.pos_ != "DET"])}


def extract_phrases(
    # fmt: off
    file_in: Path = typer.Argument(..., help="A .json file with texts"),
    file_out: Path = typer.Argument(..., help="Output file for phrases. Will print if not provided."),
    model: str = typer.Option(..., help="A spaCy model to load."),
    n: int = typer.Option(None, help="Only consider top `n` texts."),
    keep_det: bool = typer.Option(False, help="Keep the determinant in the phrase.", is_flag=True),
    # fmt: on
):
    """Turns a `.jsonl` with text into a `.jsonl` with extracted phrases.

    Note! spaCy needs to be installed with an available model
    """
    # fmt: off
    import spacy
    import srsly
    # fmt: on

    stream = (ex["text"] for ex in srsly.read_jsonl(file_in))
    if n:
        stream = it.islice(stream, n)
    nlp = spacy.load(model, disable=["ents"])
    stream = _fetch_phrases(stream, nlp, keep_det=keep_det)
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for ex in stream:
            print(json.dumps(ex))


if __name__ == "__main__":
    typer.run(extract_phrases)
