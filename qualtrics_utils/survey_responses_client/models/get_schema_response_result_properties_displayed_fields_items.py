from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_schema_response_result_properties_displayed_fields_items_type import (
    GetSchemaResponseResultPropertiesDisplayedFieldsItemsType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSchemaResponseResultPropertiesDisplayedFieldsItems")


@_attrs_define
class GetSchemaResponseResultPropertiesDisplayedFieldsItems:
    """
    Attributes:
        type (Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsItemsType]):
    """

    type: Union[
        Unset, GetSchemaResponseResultPropertiesDisplayedFieldsItemsType
    ] = UNSET
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
        type: Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsItemsType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetSchemaResponseResultPropertiesDisplayedFieldsItemsType(_type)

        get_schema_response_result_properties_displayed_fields_items = cls(
            type=type,
        )

        get_schema_response_result_properties_displayed_fields_items.additional_properties = (
            d
        )
        return get_schema_response_result_properties_displayed_fields_items

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
