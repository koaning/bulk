import pytest
import pathlib

from bulk.__main__ import download_fruits, download_pets, download_twemoji

mapper = {"fruits": download_fruits, "pets": download_pets, "twemoji": download_twemoji}


@pytest.mark.ci
@pytest.mark.parametrize("dataset", ["fruits", "pets", "twemoji"])
def test_download(dataset):
    """These tests may fail locally, but should be green in CI."""
    downloader = mapper[dataset]
    downloader()
    assert pathlib.Path("downloads", dataset).exists()

    # The path exists now, so exit_code needs to be raised
    with pytest.raises(SystemExit):
        downloader()
