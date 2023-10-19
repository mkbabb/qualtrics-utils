from enum import Enum


class ExportCreationRequestFormat(str, Enum):
    CSV = "csv"
    JSON = "json"
    NDJSON = "ndjson"
    SPSS = "spss"
    TSV = "tsv"
    XML = "xml"

    def __str__(self) -> str:
        return str(self.value)
