import json
import pathlib

from qualtrics_utils.codebook.generate import generate_codebook


def test_generate_codebook(codebook_path: pathlib.Path) -> None:
    codebook = generate_codebook(codebook_path)

    assert len(codebook) == 1
