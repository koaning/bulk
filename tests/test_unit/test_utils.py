import pandas as pd
import pytest

from bulk._bokeh_utils import get_color_mapping, read_file, determine_keyword, read_file

MAX_DISCRETE_CLASSES = 10


def _int_to_alpha(x: int) -> str:
    # returns int mapped to char: 0: a, 1: b, 2: c
    return chr(x + 97)


def _create_dummy_df() -> pd.DataFrame:
    df = pd.DataFrame()
    df["color"] = [_int_to_alpha(i) for i in range(MAX_DISCRETE_CLASSES)]
    return df


def test_get_color_mapping_raises_error_on_too_many_classes():
    df = _create_dummy_df()
    additional_class = pd.DataFrame.from_records(
        [{"color": _int_to_alpha(MAX_DISCRETE_CLASSES + 1)}]
    )
    df = pd.concat([df, additional_class], axis=0, ignore_index=True)
    with pytest.raises(ValueError):
        get_color_mapping(df)


def test_get_color_mapping_doesnt_raise_error():
    df = _create_dummy_df()
    try:
        get_color_mapping(df)
    except ValueError as e:
        assert False, f"get_color_mapping raised a ValueError: {e}"


def test_exit_bad_file():
    with pytest.raises(SystemExit):
        read_file("foobar.yaml")


def test_determine_keyword():
    assert determine_keyword("this is a sentence", ["this"]) == "this"
    assert determine_keyword("this is a sentence", ["that"]) == "none"


def test_pluck_orig_cols():
    _, _, orig_cols = read_file("tests/data/text.csv")
    assert set(orig_cols) == set(["text", "x", "y"])


def test_throw_sys_exit_no_text_with_keywords():
    with pytest.raises(SystemExit):
        read_file("tests/data/vision.csv", keywords=["foobar"])
