from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.meta import Meta
    from ..models.retrieve_response_response_not_yet_available_result import (
        RetrieveResponseResponseNotYetAvailableResult,
    )


T = TypeVar("T", bound="RetrieveResponseResponseNotYetAvailable")


@_attrs_define
class RetrieveResponseResponseNotYetAvailable:
    """
    Attributes:
        result (RetrieveResponseResponseNotYetAvailableResult):
        meta (Meta):
    """

    result: "RetrieveResponseResponseNotYetAvailableResult"
    meta: "Meta"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = self.result.to_dict()

        meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.meta import Meta
        from ..models.retrieve_response_response_not_yet_available_result import (
            RetrieveResponseResponseNotYetAvailableResult,
        )

        d = src_dict.copy()
        result = RetrieveResponseResponseNotYetAvailableResult.from_dict(
            d.pop("result")
        )

        meta = Meta.from_dict(d.pop("meta"))

        retrieve_response_response_not_yet_available = cls(
            result=result,
            meta=meta,
        )

        retrieve_response_response_not_yet_available.additional_properties = d
        return retrieve_response_response_not_yet_available

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
