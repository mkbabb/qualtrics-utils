from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.meta_error import MetaError


T = TypeVar("T", bound="Meta")


@_attrs_define
class Meta:
    """
    Attributes:
        request_id (str):
        http_status (str):
        notice (Union[Unset, str]):
        error (Union[Unset, MetaError]):
    """

    request_id: str
    http_status: str
    notice: Union[Unset, str] = UNSET
    error: Union[Unset, "MetaError"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_id = self.request_id
        http_status = self.http_status
        notice = self.notice
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestId": request_id,
                "httpStatus": http_status,
            }
        )
        if notice is not UNSET:
            field_dict["notice"] = notice
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.meta_error import MetaError

        d = src_dict.copy()
        request_id = d.pop("requestId")

        http_status = d.pop("httpStatus")

        notice = d.pop("notice", UNSET)

        _error = d.pop("error", UNSET)
        error: Union[Unset, MetaError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = MetaError.from_dict(_error)

        meta = cls(
            request_id=request_id,
            http_status=http_status,
            notice=notice,
            error=error,
        )

        meta.additional_properties = d
        return meta

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
