from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportStatusResponseResult")


@_attrs_define
class ExportStatusResponseResult:
    """
    Attributes:
        percent_complete (float): Indicates current completion of the export, in a percentage.
        status (RequestStatus): Indicates the status of the asynchronous operation.
        file_id (Union[Unset, str]):  Example: 1dc4c492-fbb6-4713-a7ba-bae9b988a965-def.
        continuation_token (Union[Unset, str]): The next continuation token needed to get all responses recorded since
            this export and not included in this export.
    """

    percent_complete: float
    status: RequestStatus
    file_id: Union[Unset, str] = UNSET
    continuation_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        percent_complete = self.percent_complete
        status = self.status.value

        file_id = self.file_id
        continuation_token = self.continuation_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "percentComplete": percent_complete,
                "status": status,
            }
        )
        if file_id is not UNSET:
            field_dict["fileId"] = file_id
        if continuation_token is not UNSET:
            field_dict["continuationToken"] = continuation_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        percent_complete = d.pop("percentComplete")

        status = RequestStatus(d.pop("status"))

        file_id = d.pop("fileId", UNSET)

        continuation_token = d.pop("continuationToken", UNSET)

        export_status_response_result = cls(
            percent_complete=percent_complete,
            status=status,
            file_id=file_id,
            continuation_token=continuation_token,
        )

        export_status_response_result.additional_properties = d
        return export_status_response_result

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
