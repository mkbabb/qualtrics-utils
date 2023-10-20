from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_property_items_properties_x import (
        SchemaPropertyItemsPropertiesX,
    )
    from ..models.schema_property_items_properties_y import (
        SchemaPropertyItemsPropertiesY,
    )


T = TypeVar("T", bound="SchemaPropertyItemsProperties")


@_attrs_define
class SchemaPropertyItemsProperties:
    """
    Attributes:
        x (Union[Unset, SchemaPropertyItemsPropertiesX]):
        y (Union[Unset, SchemaPropertyItemsPropertiesY]):
    """

    x: Union[Unset, "SchemaPropertyItemsPropertiesX"] = UNSET
    y: Union[Unset, "SchemaPropertyItemsPropertiesY"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        x: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.x, Unset):
            x = self.x.to_dict()

        y: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.y, Unset):
            y = self.y.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.schema_property_items_properties_x import (
            SchemaPropertyItemsPropertiesX,
        )
        from ..models.schema_property_items_properties_y import (
            SchemaPropertyItemsPropertiesY,
        )

        d = src_dict.copy()
        _x = d.pop("x", UNSET)
        x: Union[Unset, SchemaPropertyItemsPropertiesX]
        if isinstance(_x, Unset):
            x = UNSET
        else:
            x = SchemaPropertyItemsPropertiesX.from_dict(_x)

        _y = d.pop("y", UNSET)
        y: Union[Unset, SchemaPropertyItemsPropertiesY]
        if isinstance(_y, Unset):
            y = UNSET
        else:
            y = SchemaPropertyItemsPropertiesY.from_dict(_y)

        schema_property_items_properties = cls(
            x=x,
            y=y,
        )

        schema_property_items_properties.additional_properties = d
        return schema_property_items_properties

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
