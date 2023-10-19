import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="GetFiltersListResponseResultElementsItem")


@_attrs_define
class GetFiltersListResponseResultElementsItem:
    """
    Attributes:
        filter_name (str): The name of the filter.
        creation_date (datetime.datetime): The date and time the filter was created.
        filter_id (str): The ID of the filter.
    """

    filter_name: str
    creation_date: datetime.datetime
    filter_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_name = self.filter_name
        creation_date = self.creation_date.isoformat()

        filter_id = self.filter_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filterName": filter_name,
                "creationDate": creation_date,
                "filterId": filter_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_name = d.pop("filterName")

        creation_date = isoparse(d.pop("creationDate"))

        filter_id = d.pop("filterId")

        get_filters_list_response_result_elements_item = cls(
            filter_name=filter_name,
            creation_date=creation_date,
            filter_id=filter_id,
        )

        get_filters_list_response_result_elements_item.additional_properties = d
        return get_filters_list_response_result_elements_item

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
