from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.meta_with_error import MetaWithError


T = TypeVar("T", bound="SurveyNotFoundResponse")


@_attrs_define
class SurveyNotFoundResponse:
    """
    Attributes:
        meta (MetaWithError):
    """

    meta: "MetaWithError"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.meta_with_error import MetaWithError

        d = src_dict.copy()
        meta = MetaWithError.from_dict(d.pop("meta"))

        survey_not_found_response = cls(
            meta=meta,
        )

        survey_not_found_response.additional_properties = d
        return survey_not_found_response

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
