from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_schema_response_result_properties_values_type import (
    GetSchemaResponseResultPropertiesValuesType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_schema_response_result_properties_values_properties import (
        GetSchemaResponseResultPropertiesValuesProperties,
    )


T = TypeVar("T", bound="GetSchemaResponseResultPropertiesValues")


@_attrs_define
class GetSchemaResponseResultPropertiesValues:
    """
    Attributes:
        type (Union[Unset, GetSchemaResponseResultPropertiesValuesType]):
        description (Union[Unset, str]):
        properties (Union[Unset, GetSchemaResponseResultPropertiesValuesProperties]):
        required (Union[Unset, List[str]]): A list of fields that will always be on the survey response. This list is
            the same across all surveys.
    """

    type: Union[Unset, GetSchemaResponseResultPropertiesValuesType] = UNSET
    description: Union[Unset, str] = UNSET
    properties: Union[
        Unset, "GetSchemaResponseResultPropertiesValuesProperties"
    ] = UNSET
    required: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        description = self.description
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        required: Union[Unset, List[str]] = UNSET
        if not isinstance(self.required, Unset):
            required = self.required

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if properties is not UNSET:
            field_dict["properties"] = properties
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_schema_response_result_properties_values_properties import (
            GetSchemaResponseResultPropertiesValuesProperties,
        )

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, GetSchemaResponseResultPropertiesValuesType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetSchemaResponseResultPropertiesValuesType(_type)

        description = d.pop("description", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, GetSchemaResponseResultPropertiesValuesProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = GetSchemaResponseResultPropertiesValuesProperties.from_dict(
                _properties
            )

        required = cast(List[str], d.pop("required", UNSET))

        get_schema_response_result_properties_values = cls(
            type=type,
            description=description,
            properties=properties,
            required=required,
        )

        get_schema_response_result_properties_values.additional_properties = d
        return get_schema_response_result_properties_values

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
