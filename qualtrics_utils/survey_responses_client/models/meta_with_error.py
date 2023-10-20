from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error import Error


T = TypeVar("T", bound="MetaWithError")


@_attrs_define
class MetaWithError:
    """
    Attributes:
        http_status (str): HTTP status code
        request_id (str): An identifier for the incoming request.
        error (Error):
        notice (Union[Unset, str]):
    """

    http_status: str
    request_id: str
    error: "Error"
    notice: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        http_status = self.http_status
        request_id = self.request_id
        error = self.error.to_dict()

        notice = self.notice

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "httpStatus": http_status,
                "requestId": request_id,
                "error": error,
            }
        )
        if notice is not UNSET:
            field_dict["notice"] = notice

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error import Error

        d = src_dict.copy()
        http_status = d.pop("httpStatus")

        request_id = d.pop("requestId")

        error = Error.from_dict(d.pop("error"))

        notice = d.pop("notice", UNSET)

        meta_with_error = cls(
            http_status=http_status,
            request_id=request_id,
            error=error,
            notice=notice,
        )

        meta_with_error.additional_properties = d
        return meta_with_error

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
