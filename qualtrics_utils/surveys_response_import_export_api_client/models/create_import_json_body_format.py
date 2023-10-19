from enum import Enum


class CreateImportJsonBodyFormat(str, Enum):
    CSV = "csv"
    TSV = "tsv"

    def __str__(self) -> str:
        return str(self.value)
