import pathlib

import pytest


@pytest.fixture
def codebook_path() -> pathlib.Path:
    return pathlib.Path("data/NC_ODEL_DE_Survey-Spring_2023.qsf")
