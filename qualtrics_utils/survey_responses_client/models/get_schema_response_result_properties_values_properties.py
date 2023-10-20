from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_property import SchemaProperty


T = TypeVar("T", bound="GetSchemaResponseResultPropertiesValuesProperties")


@_attrs_define
class GetSchemaResponseResultPropertiesValuesProperties:
    """
    Attributes:
        distribution_channel (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the
            JSON survey response
        duration (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON survey
            response
        end_date (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON survey
            response
        finished (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON survey
            response
        location_latitude (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the
            JSON survey response
        location_longitude (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the
            JSON survey response
        progress (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON survey
            response
        recorded_date (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON
            survey response
        start_date (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON
            survey response
        status (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON survey
            response
        user_language (Union[Unset, SchemaProperty]): Each entry represents a field in the `values` field of the JSON
            survey response
    """

    distribution_channel: Union[Unset, "SchemaProperty"] = UNSET
    duration: Union[Unset, "SchemaProperty"] = UNSET
    end_date: Union[Unset, "SchemaProperty"] = UNSET
    finished: Union[Unset, "SchemaProperty"] = UNSET
    location_latitude: Union[Unset, "SchemaProperty"] = UNSET
    location_longitude: Union[Unset, "SchemaProperty"] = UNSET
    progress: Union[Unset, "SchemaProperty"] = UNSET
    recorded_date: Union[Unset, "SchemaProperty"] = UNSET
    start_date: Union[Unset, "SchemaProperty"] = UNSET
    status: Union[Unset, "SchemaProperty"] = UNSET
    user_language: Union[Unset, "SchemaProperty"] = UNSET
    additional_properties: Dict[str, "SchemaProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        distribution_channel: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.distribution_channel, Unset):
            distribution_channel = self.distribution_channel.to_dict()

        duration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.duration, Unset):
            duration = self.duration.to_dict()

        end_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.to_dict()

        finished: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.finished, Unset):
            finished = self.finished.to_dict()

        location_latitude: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location_latitude, Unset):
            location_latitude = self.location_latitude.to_dict()

        location_longitude: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location_longitude, Unset):
            location_longitude = self.location_longitude.to_dict()

        progress: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()

        recorded_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recorded_date, Unset):
            recorded_date = self.recorded_date.to_dict()

        start_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.to_dict()

        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        user_language: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_language, Unset):
            user_language = self.user_language.to_dict()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})
        if distribution_channel is not UNSET:
            field_dict["distributionChannel"] = distribution_channel
        if duration is not UNSET:
            field_dict["duration"] = duration
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if finished is not UNSET:
            field_dict["finished"] = finished
        if location_latitude is not UNSET:
            field_dict["locationLatitude"] = location_latitude
        if location_longitude is not UNSET:
            field_dict["locationLongitude"] = location_longitude
        if progress is not UNSET:
            field_dict["progress"] = progress
        if recorded_date is not UNSET:
            field_dict["recordedDate"] = recorded_date
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if status is not UNSET:
            field_dict["status"] = status
        if user_language is not UNSET:
            field_dict["userLanguage"] = user_language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.schema_property import SchemaProperty

        d = src_dict.copy()
        _distribution_channel = d.pop("distributionChannel", UNSET)
        distribution_channel: Union[Unset, SchemaProperty]
        if isinstance(_distribution_channel, Unset):
            distribution_channel = UNSET
        else:
            distribution_channel = SchemaProperty.from_dict(_distribution_channel)

        _duration = d.pop("duration", UNSET)
        duration: Union[Unset, SchemaProperty]
        if isinstance(_duration, Unset):
            duration = UNSET
        else:
            duration = SchemaProperty.from_dict(_duration)

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, SchemaProperty]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = SchemaProperty.from_dict(_end_date)

        _finished = d.pop("finished", UNSET)
        finished: Union[Unset, SchemaProperty]
        if isinstance(_finished, Unset):
            finished = UNSET
        else:
            finished = SchemaProperty.from_dict(_finished)

        _location_latitude = d.pop("locationLatitude", UNSET)
        location_latitude: Union[Unset, SchemaProperty]
        if isinstance(_location_latitude, Unset):
            location_latitude = UNSET
        else:
            location_latitude = SchemaProperty.from_dict(_location_latitude)

        _location_longitude = d.pop("locationLongitude", UNSET)
        location_longitude: Union[Unset, SchemaProperty]
        if isinstance(_location_longitude, Unset):
            location_longitude = UNSET
        else:
            location_longitude = SchemaProperty.from_dict(_location_longitude)

        _progress = d.pop("progress", UNSET)
        progress: Union[Unset, SchemaProperty]
        if isinstance(_progress, Unset):
            progress = UNSET
        else:
            progress = SchemaProperty.from_dict(_progress)

        _recorded_date = d.pop("recordedDate", UNSET)
        recorded_date: Union[Unset, SchemaProperty]
        if isinstance(_recorded_date, Unset):
            recorded_date = UNSET
        else:
            recorded_date = SchemaProperty.from_dict(_recorded_date)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, SchemaProperty]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = SchemaProperty.from_dict(_start_date)

        _status = d.pop("status", UNSET)
        status: Union[Unset, SchemaProperty]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SchemaProperty.from_dict(_status)

        _user_language = d.pop("userLanguage", UNSET)
        user_language: Union[Unset, SchemaProperty]
        if isinstance(_user_language, Unset):
            user_language = UNSET
        else:
            user_language = SchemaProperty.from_dict(_user_language)

        get_schema_response_result_properties_values_properties = cls(
            distribution_channel=distribution_channel,
            duration=duration,
            end_date=end_date,
            finished=finished,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            progress=progress,
            recorded_date=recorded_date,
            start_date=start_date,
            status=status,
            user_language=user_language,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = SchemaProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_schema_response_result_properties_values_properties.additional_properties = (
            additional_properties
        )
        return get_schema_response_result_properties_values_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "SchemaProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "SchemaProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
