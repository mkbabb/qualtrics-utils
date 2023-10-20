from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_schema_response_result_properties_labels_additional_properties import (
    GetSchemaResponseResultPropertiesLabelsAdditionalProperties,
)
from ..models.get_schema_response_result_properties_labels_type import (
    GetSchemaResponseResultPropertiesLabelsType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSchemaResponseResultPropertiesLabels")


@_attrs_define
class GetSchemaResponseResultPropertiesLabels:
    """
    Attributes:
        description (Union[Unset, str]):
        type (Union[Unset, GetSchemaResponseResultPropertiesLabelsType]):
        additional_properties (Union[Unset, GetSchemaResponseResultPropertiesLabelsAdditionalProperties]):
    """

    description: Union[Unset, str] = UNSET
    type: Union[Unset, GetSchemaResponseResultPropertiesLabelsType] = UNSET
    additional_properties: Union[
        Unset, GetSchemaResponseResultPropertiesLabelsAdditionalProperties
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        additional_properties: Union[Unset, int] = UNSET
        if not isinstance(self.additional_properties, Unset):
            additional_properties = self.additional_properties.value

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
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, GetSchemaResponseResultPropertiesLabelsType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetSchemaResponseResultPropertiesLabelsType(_type)

        _additional_properties = d.pop("additionalProperties", UNSET)
        additional_properties: Union[
            Unset, GetSchemaResponseResultPropertiesLabelsAdditionalProperties
        ]
        if isinstance(_additional_properties, Unset):
            additional_properties = UNSET
        else:
            additional_properties = (
                GetSchemaResponseResultPropertiesLabelsAdditionalProperties(
                    _additional_properties
                )
            )

        get_schema_response_result_properties_labels = cls(
            description=description,
            type=type,
            additional_properties=additional_properties,
        )

        get_schema_response_result_properties_labels.additional_properties = d
        return get_schema_response_result_properties_labels

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
