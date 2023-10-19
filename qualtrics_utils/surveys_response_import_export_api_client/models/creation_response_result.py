from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreationResponseResult")


@_attrs_define
class CreationResponseResult:
    """
    Attributes:
        progress_id (str): The ID of the asynchronous operation.
        percent_complete (float): Indicates current completion of the asynchronous operation, in a percentage.
        status (RequestStatus): Indicates the status of the asynchronous operation.
        continuation_token (Union[Unset, str]): The next continuation token needed to get all responses recorded since
            this export and not included in this export.
    """

    progress_id: str
    percent_complete: float
    status: RequestStatus
    continuation_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        progress_id = self.progress_id
        percent_complete = self.percent_complete
        status = self.status.value

        continuation_token = self.continuation_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "progressId": progress_id,
                "percentComplete": percent_complete,
                "status": status,
            }
        )
        if continuation_token is not UNSET:
            field_dict["continuationToken"] = continuation_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        progress_id = d.pop("progressId")

        percent_complete = d.pop("percentComplete")

        status = RequestStatus(d.pop("status"))

        continuation_token = d.pop("continuationToken", UNSET)

        creation_response_result = cls(
            progress_id=progress_id,
            percent_complete=percent_complete,
            status=status,
            continuation_token=continuation_token,
        )

        creation_response_result.additional_properties = d
        return creation_response_result

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
