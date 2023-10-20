from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.retrieve_response_response_result_displayed_values import (
        RetrieveResponseResponseResultDisplayedValues,
    )
    from ..models.retrieve_response_response_result_labels import (
        RetrieveResponseResponseResultLabels,
    )
    from ..models.retrieve_response_response_result_values import (
        RetrieveResponseResponseResultValues,
    )


T = TypeVar("T", bound="RetrieveResponseResponseResult")


@_attrs_define
class RetrieveResponseResponseResult:
    """
    Attributes:
        response_id (str): The unique ID for each response
        values (RetrieveResponseResponseResultValues): `values` is a set of key-value pairs corresponding to question-
            answer pairs. There can also be key-value pairs representing meta data for the response such as `startDate` or
            `userLanguage`.
        labels (RetrieveResponseResponseResultLabels): `labels` is a set of key-value pairs where each key corresponds
            to a key in the `values` object and the value is the label of the answer of that question.
        displayed_fields (Union[Unset, List[str]]): All the fields that were displayed during the taking of the survey
        displayed_values (Union[Unset, RetrieveResponseResponseResultDisplayedValues]): For every field, the values that
            were displayed during the taking of the survey
    """

    response_id: str
    values: "RetrieveResponseResponseResultValues"
    labels: "RetrieveResponseResponseResultLabels"
    displayed_fields: Union[Unset, List[str]] = UNSET
    displayed_values: Union[
        Unset, "RetrieveResponseResponseResultDisplayedValues"
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        response_id = self.response_id
        values = self.values.to_dict()

        labels = self.labels.to_dict()

        displayed_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.displayed_fields, Unset):
            displayed_fields = self.displayed_fields

        displayed_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.displayed_values, Unset):
            displayed_values = self.displayed_values.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "responseId": response_id,
                "values": values,
                "labels": labels,
            }
        )
        if displayed_fields is not UNSET:
            field_dict["displayedFields"] = displayed_fields
        if displayed_values is not UNSET:
            field_dict["displayedValues"] = displayed_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.retrieve_response_response_result_displayed_values import (
            RetrieveResponseResponseResultDisplayedValues,
        )
        from ..models.retrieve_response_response_result_labels import (
            RetrieveResponseResponseResultLabels,
        )
        from ..models.retrieve_response_response_result_values import (
            RetrieveResponseResponseResultValues,
        )

        d = src_dict.copy()
        response_id = d.pop("responseId")

        values = RetrieveResponseResponseResultValues.from_dict(d.pop("values"))

        labels = RetrieveResponseResponseResultLabels.from_dict(d.pop("labels"))

        displayed_fields = cast(List[str], d.pop("displayedFields", UNSET))

        _displayed_values = d.pop("displayedValues", UNSET)
        displayed_values: Union[Unset, RetrieveResponseResponseResultDisplayedValues]
        if isinstance(_displayed_values, Unset):
            displayed_values = UNSET
        else:
            displayed_values = RetrieveResponseResponseResultDisplayedValues.from_dict(
                _displayed_values
            )

        retrieve_response_response_result = cls(
            response_id=response_id,
            values=values,
            labels=labels,
            displayed_fields=displayed_fields,
            displayed_values=displayed_values,
        )

        retrieve_response_response_result.additional_properties = d
        return retrieve_response_response_result

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
