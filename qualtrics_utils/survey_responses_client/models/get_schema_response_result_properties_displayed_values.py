from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_schema_response_result_properties_displayed_values_type import (
    GetSchemaResponseResultPropertiesDisplayedValuesType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_schema_response_result_properties_displayed_values_additional_properties import (
        GetSchemaResponseResultPropertiesDisplayedValuesAdditionalProperties,
    )


T = TypeVar("T", bound="GetSchemaResponseResultPropertiesDisplayedValues")


@_attrs_define
class GetSchemaResponseResultPropertiesDisplayedValues:
    """
    Attributes:
        description (Union[Unset, str]):
        type (Union[Unset, GetSchemaResponseResultPropertiesDisplayedValuesType]):
        additional_properties (Union[Unset, GetSchemaResponseResultPropertiesDisplayedValuesAdditionalProperties]):
    """

    description: Union[Unset, str] = UNSET
    type: Union[Unset, GetSchemaResponseResultPropertiesDisplayedValuesType] = UNSET
    additional_properties: Union[
        Unset, "GetSchemaResponseResultPropertiesDisplayedValuesAdditionalProperties"
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        additional_properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.additional_properties, Unset):
            additional_properties = self.additional_properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if additional_properties is not UNSET:
            field_dict["additionalProperties"] = additional_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_schema_response_result_properties_displayed_values_additional_properties import (
            GetSchemaResponseResultPropertiesDisplayedValuesAdditionalProperties,
        )

        d = src_dict.copy()
        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, GetSchemaResponseResultPropertiesDisplayedValuesType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetSchemaResponseResultPropertiesDisplayedValuesType(_type)

        _additional_properties = d.pop("additionalProperties", UNSET)
        additional_properties: Union[
            Unset, GetSchemaResponseResultPropertiesDisplayedValuesAdditionalProperties
        ]
        if isinstance(_additional_properties, Unset):
            additional_properties = UNSET
        else:
            additional_properties = GetSchemaResponseResultPropertiesDisplayedValuesAdditionalProperties.from_dict(
                _additional_properties
            )

        get_schema_response_result_properties_displayed_values = cls(
            description=description,
            type=type,
            additional_properties=additional_properties,
        )

        get_schema_response_result_properties_displayed_values.additional_properties = d
        return get_schema_response_result_properties_displayed_values

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
