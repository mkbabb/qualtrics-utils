from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.schema_property_items_properties_y_type import (
    SchemaPropertyItemsPropertiesYType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaPropertyItemsPropertiesY")


@_attrs_define
class SchemaPropertyItemsPropertiesY:
    """
    Attributes:
        type (Union[Unset, SchemaPropertyItemsPropertiesYType]):
    """

    type: Union[Unset, SchemaPropertyItemsPropertiesYType] = UNSET
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
        type: Union[Unset, SchemaPropertyItemsPropertiesYType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = SchemaPropertyItemsPropertiesYType(_type)

        schema_property_items_properties_y = cls(
            type=type,
        )

        schema_property_items_properties_y.additional_properties = d
        return schema_property_items_properties_y

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
