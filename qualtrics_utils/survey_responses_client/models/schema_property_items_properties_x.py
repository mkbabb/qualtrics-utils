from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.schema_property_items_properties_x_type import (
    SchemaPropertyItemsPropertiesXType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaPropertyItemsPropertiesX")


@_attrs_define
class SchemaPropertyItemsPropertiesX:
    """
    Attributes:
        type (Union[Unset, SchemaPropertyItemsPropertiesXType]):
    """

    type: Union[Unset, SchemaPropertyItemsPropertiesXType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, SchemaPropertyItemsPropertiesXType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = SchemaPropertyItemsPropertiesXType(_type)

        schema_property_items_properties_x = cls(
            type=type,
        )

        schema_property_items_properties_x.additional_properties = d
        return schema_property_items_properties_x

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
