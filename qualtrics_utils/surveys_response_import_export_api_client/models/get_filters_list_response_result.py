from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_filters_list_response_result_elements_item import (
        GetFiltersListResponseResultElementsItem,
    )


T = TypeVar("T", bound="GetFiltersListResponseResult")


@_attrs_define
class GetFiltersListResponseResult:
    """
    Attributes:
        elements (List['GetFiltersListResponseResultElementsItem']):
        next_page (Optional[str]):
    """

    elements: List["GetFiltersListResponseResultElementsItem"]
    next_page: Optional[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        elements = []
        for elements_item_data in self.elements:
            elements_item = elements_item_data.to_dict()

            elements.append(elements_item)

        next_page = self.next_page

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elements": elements,
                "nextPage": next_page,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_filters_list_response_result_elements_item import (
            GetFiltersListResponseResultElementsItem,
        )

        d = src_dict.copy()
        elements = []
        _elements = d.pop("elements")
        for elements_item_data in _elements:
            elements_item = GetFiltersListResponseResultElementsItem.from_dict(
                elements_item_data
            )

            elements.append(elements_item)

        next_page = d.pop("nextPage")

        get_filters_list_response_result = cls(
            elements=elements,
            next_page=next_page,
        )

        get_filters_list_response_result.additional_properties = d
        return get_filters_list_response_result

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
