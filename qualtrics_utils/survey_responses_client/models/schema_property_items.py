from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_property_items_properties import SchemaPropertyItemsProperties
    from ..models.survey_answer import SurveyAnswer


T = TypeVar("T", bound="SchemaPropertyItems")


@_attrs_define
class SchemaPropertyItems:
    """
    Attributes:
        type (Union[Unset, str]):
        one_of (Union[Unset, List['SurveyAnswer']]):
        properties (Union[Unset, SchemaPropertyItemsProperties]):
    """

    type: Union[Unset, str] = UNSET
    one_of: Union[Unset, List["SurveyAnswer"]] = UNSET
    properties: Union[Unset, "SchemaPropertyItemsProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        one_of: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.one_of, Unset):
            one_of = []
            for one_of_item_data in self.one_of:
                one_of_item = one_of_item_data.to_dict()

                one_of.append(one_of_item)

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if one_of is not UNSET:
            field_dict["oneOf"] = one_of
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.schema_property_items_properties import (
            SchemaPropertyItemsProperties,
        )
        from ..models.survey_answer import SurveyAnswer

        d = src_dict.copy()
        type = d.pop("type", UNSET)

        one_of = []
        _one_of = d.pop("oneOf", UNSET)
        for one_of_item_data in _one_of or []:
            one_of_item = SurveyAnswer.from_dict(one_of_item_data)

            one_of.append(one_of_item)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, SchemaPropertyItemsProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = SchemaPropertyItemsProperties.from_dict(_properties)

        schema_property_items = cls(
            type=type,
            one_of=one_of,
            properties=properties,
        )

        schema_property_items.additional_properties = d
        return schema_property_items

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
