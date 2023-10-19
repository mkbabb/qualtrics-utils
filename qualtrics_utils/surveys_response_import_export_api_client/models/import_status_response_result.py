from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.request_status import RequestStatus

T = TypeVar("T", bound="ImportStatusResponseResult")


@_attrs_define
class ImportStatusResponseResult:
    """
    Attributes:
        percent_complete (float):
        status (RequestStatus): Indicates the status of the asynchronous operation.
    """

    percent_complete: float
    status: RequestStatus
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        percent_complete = self.percent_complete
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "percentComplete": percent_complete,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        percent_complete = d.pop("percentComplete")

        status = RequestStatus(d.pop("status"))

        import_status_response_result = cls(
            percent_complete=percent_complete,
            status=status,
        )

        import_status_response_result.additional_properties = d
        return import_status_response_result

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
