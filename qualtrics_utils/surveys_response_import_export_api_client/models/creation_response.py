from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.creation_response_result import CreationResponseResult
    from ..models.meta import Meta


T = TypeVar("T", bound="CreationResponse")


@_attrs_define
class CreationResponse:
    """
    Attributes:
        result (CreationResponseResult):
        meta (Meta):
    """

    result: "CreationResponseResult"
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
        from ..models.creation_response_result import CreationResponseResult
        from ..models.meta import Meta

        d = src_dict.copy()
        result = CreationResponseResult.from_dict(d.pop("result"))

        meta = Meta.from_dict(d.pop("meta"))

        creation_response = cls(
            result=result,
            meta=meta,
        )

        creation_response.additional_properties = d
        return creation_response

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
