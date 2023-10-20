from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_schema_response_result_schema import GetSchemaResponseResultSchema
from ..models.get_schema_response_result_type import GetSchemaResponseResultType

if TYPE_CHECKING:
    from ..models.get_schema_response_result_properties import (
        GetSchemaResponseResultProperties,
    )


T = TypeVar("T", bound="GetSchemaResponseResult")


@_attrs_define
class GetSchemaResponseResult:
    """
    Attributes:
        schema (GetSchemaResponseResultSchema):
        id (str):
        title (str):
        description (str):
        type (GetSchemaResponseResultType):
        required (List[str]):
        properties (GetSchemaResponseResultProperties):
    """

    schema: GetSchemaResponseResultSchema
    id: str
    title: str
    description: str
    type: GetSchemaResponseResultType
    required: List[str]
    properties: "GetSchemaResponseResultProperties"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema = self.schema.value

        id = self.id
        title = self.title
        description = self.description
        type = self.type.value

        required = self.required

        properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "$schema": schema,
                "$id": id,
                "title": title,
                "description": description,
                "type": type,
                "required": required,
                "properties": properties,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_schema_response_result_properties import (
            GetSchemaResponseResultProperties,
        )

        d = src_dict.copy()
        schema = GetSchemaResponseResultSchema(d.pop("$schema"))

        id = d.pop("$id")

        title = d.pop("title")

        description = d.pop("description")

        type = GetSchemaResponseResultType(d.pop("type"))

        required = cast(List[str], d.pop("required"))

        properties = GetSchemaResponseResultProperties.from_dict(d.pop("properties"))

        get_schema_response_result = cls(
            schema=schema,
            id=id,
            title=title,
            description=description,
            type=type,
            required=required,
            properties=properties,
        )

        get_schema_response_result.additional_properties = d
        return get_schema_response_result

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
