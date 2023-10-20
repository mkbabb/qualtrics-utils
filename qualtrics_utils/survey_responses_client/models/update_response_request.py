from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_response_request_embedded_data import (
        UpdateResponseRequestEmbeddedData,
    )


T = TypeVar("T", bound="UpdateResponseRequest")


@_attrs_define
class UpdateResponseRequest:
    """
    Attributes:
        survey_id (str): The Survey ID
        embedded_data (UpdateResponseRequestEmbeddedData): `embeddedData` is a JSON object representing the embedded
            data fields to set.
        reset_recorded_date (Union[Unset, bool]): Sets the recorded date to the current time. If false, the recorded
            date will be incremented by one millisecond. Default: True.
    """

    survey_id: str
    embedded_data: "UpdateResponseRequestEmbeddedData"
    reset_recorded_date: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        survey_id = self.survey_id
        embedded_data = self.embedded_data.to_dict()

        reset_recorded_date = self.reset_recorded_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "surveyId": survey_id,
                "embeddedData": embedded_data,
            }
        )
        if reset_recorded_date is not UNSET:
            field_dict["resetRecordedDate"] = reset_recorded_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_response_request_embedded_data import (
            UpdateResponseRequestEmbeddedData,
        )

        d = src_dict.copy()
        survey_id = d.pop("surveyId")

        embedded_data = UpdateResponseRequestEmbeddedData.from_dict(
            d.pop("embeddedData")
        )

        reset_recorded_date = d.pop("resetRecordedDate", UNSET)

        update_response_request = cls(
            survey_id=survey_id,
            embedded_data=embedded_data,
            reset_recorded_date=reset_recorded_date,
        )

        update_response_request.additional_properties = d
        return update_response_request

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
