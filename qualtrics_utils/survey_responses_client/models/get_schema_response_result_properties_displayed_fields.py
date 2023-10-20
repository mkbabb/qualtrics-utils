from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_schema_response_result_properties_displayed_fields_type import (
    GetSchemaResponseResultPropertiesDisplayedFieldsType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_schema_response_result_properties_displayed_fields_items import (
        GetSchemaResponseResultPropertiesDisplayedFieldsItems,
    )


T = TypeVar("T", bound="GetSchemaResponseResultPropertiesDisplayedFields")


@_attrs_define
class GetSchemaResponseResultPropertiesDisplayedFields:
    """
    Attributes:
        description (Union[Unset, str]):
        type (Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsType]):
        items (Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsItems]):
    """

    description: Union[Unset, str] = UNSET
    type: Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsType] = UNSET
    items: Union[Unset, "GetSchemaResponseResultPropertiesDisplayedFieldsItems"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        items: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_schema_response_result_properties_displayed_fields_items import (
            GetSchemaResponseResultPropertiesDisplayedFieldsItems,
        )

        d = src_dict.copy()
        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetSchemaResponseResultPropertiesDisplayedFieldsType(_type)

        _items = d.pop("items", UNSET)
        items: Union[Unset, GetSchemaResponseResultPropertiesDisplayedFieldsItems]
        if isinstance(_items, Unset):
            items = UNSET
        else:
            items = GetSchemaResponseResultPropertiesDisplayedFieldsItems.from_dict(
                _items
            )

        get_schema_response_result_properties_displayed_fields = cls(
            description=description,
            type=type,
            items=items,
        )

        get_schema_response_result_properties_displayed_fields.additional_properties = d
        return get_schema_response_result_properties_displayed_fields

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
