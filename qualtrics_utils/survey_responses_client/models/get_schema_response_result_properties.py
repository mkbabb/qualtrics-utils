from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_schema_response_result_properties_displayed_fields import (
        GetSchemaResponseResultPropertiesDisplayedFields,
    )
    from ..models.get_schema_response_result_properties_displayed_values import (
        GetSchemaResponseResultPropertiesDisplayedValues,
    )
    from ..models.get_schema_response_result_properties_labels import (
        GetSchemaResponseResultPropertiesLabels,
    )
    from ..models.get_schema_response_result_properties_response_id import (
        GetSchemaResponseResultPropertiesResponseId,
    )
    from ..models.get_schema_response_result_properties_values import (
        GetSchemaResponseResultPropertiesValues,
    )


T = TypeVar("T", bound="GetSchemaResponseResultProperties")


@_attrs_define
class GetSchemaResponseResultProperties:
    """
    Attributes:
        displayed_fields (Union[Unset, GetSchemaResponseResultPropertiesDisplayedFields]):
        displayed_values (Union[Unset, GetSchemaResponseResultPropertiesDisplayedValues]):
        labels (Union[Unset, GetSchemaResponseResultPropertiesLabels]):
        response_id (Union[Unset, GetSchemaResponseResultPropertiesResponseId]):
        values (Union[Unset, GetSchemaResponseResultPropertiesValues]):
    """

    displayed_fields: Union[
        Unset, "GetSchemaResponseResultPropertiesDisplayedFields"
    ] = UNSET
    displayed_values: Union[
        Unset, "GetSchemaResponseResultPropertiesDisplayedValues"
    ] = UNSET
    labels: Union[Unset, "GetSchemaResponseResultPropertiesLabels"] = UNSET
    response_id: Union[Unset, "GetSchemaResponseResultPropertiesResponseId"] = UNSET
    values: Union[Unset, "GetSchemaResponseResultPropertiesValues"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        displayed_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.displayed_fields, Unset):
            displayed_fields = self.displayed_fields.to_dict()

        displayed_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.displayed_values, Unset):
            displayed_values = self.displayed_values.to_dict()

        labels: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        response_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.response_id, Unset):
            response_id = self.response_id.to_dict()

        values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if displayed_fields is not UNSET:
            field_dict["displayedFields"] = displayed_fields
        if displayed_values is not UNSET:
            field_dict["displayedValues"] = displayed_values
        if labels is not UNSET:
            field_dict["labels"] = labels
        if response_id is not UNSET:
            field_dict["responseId"] = response_id
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_schema_response_result_properties_displayed_fields import (
            GetSchemaResponseResultPropertiesDisplayedFields,
        )
        from ..models.get_schema_response_result_properties_displayed_values import (
            GetSchemaResponseResultPropertiesDisplayedValues,
        )
        from ..models.get_schema_response_result_properties_labels import (
            GetSchemaResponseResultPropertiesLabels,
        )
        from ..models.get_schema_response_result_properties_response_id import (
            GetSchemaResponseResultPropertiesResponseId,
        )
        from ..models.get_schema_response_result_properties_values import (
            GetSchemaResponseResultPropertiesValues,
        )

        d = src_dict.copy()
        _displayed_fields = d.pop("displayedFields", UNSET)
        displayed_fields: Union[Unset, GetSchemaResponseResultPropertiesDisplayedFields]
        if isinstance(_displayed_fields, Unset):
            displayed_fields = UNSET
        else:
            displayed_fields = (
                GetSchemaResponseResultPropertiesDisplayedFields.from_dict(
                    _displayed_fields
                )
            )

        _displayed_values = d.pop("displayedValues", UNSET)
        displayed_values: Union[Unset, GetSchemaResponseResultPropertiesDisplayedValues]
        if isinstance(_displayed_values, Unset):
            displayed_values = UNSET
        else:
            displayed_values = (
                GetSchemaResponseResultPropertiesDisplayedValues.from_dict(
                    _displayed_values
                )
            )

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, GetSchemaResponseResultPropertiesLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = GetSchemaResponseResultPropertiesLabels.from_dict(_labels)

        _response_id = d.pop("responseId", UNSET)
        response_id: Union[Unset, GetSchemaResponseResultPropertiesResponseId]
        if isinstance(_response_id, Unset):
            response_id = UNSET
        else:
            response_id = GetSchemaResponseResultPropertiesResponseId.from_dict(
                _response_id
            )

        _values = d.pop("values", UNSET)
        values: Union[Unset, GetSchemaResponseResultPropertiesValues]
        if isinstance(_values, Unset):
            values = UNSET
        else:
            values = GetSchemaResponseResultPropertiesValues.from_dict(_values)

        get_schema_response_result_properties = cls(
            displayed_fields=displayed_fields,
            displayed_values=displayed_values,
            labels=labels,
            response_id=response_id,
            values=values,
        )

        get_schema_response_result_properties.additional_properties = d
        return get_schema_response_result_properties

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
