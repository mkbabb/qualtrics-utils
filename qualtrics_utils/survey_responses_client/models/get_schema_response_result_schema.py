from enum import Enum


class GetSchemaResponseResultSchema(str, Enum):
    HTTPSJSON_SCHEMA_ORGDRAFT2019_09SCHEMA = (
        "https://json-schema.org/draft/2019-09/schema"
    )

    def __str__(self) -> str:
        return str(self.value)
