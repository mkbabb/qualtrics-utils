import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateResponseRequestValues")


@_attrs_define
class CreateResponseRequestValues:
    """`values` is a set of key-value pairs corresponding to question-answer pairs. There can also be key-value pairs
    representing meta data for the response such as `startDate` or `userLanguage`.

        Attributes:
            distribution_channel (Union[Unset, str]): The method by which the survey was distributed to respondents
            duration (Union[Unset, int]): How long it took for the respondent to finish the survey in seconds
            end_date (Union[Unset, datetime.datetime]): The point in time when the survey response was finished
            finished (Union[Unset, int]): If the respondent finished and submitted the survey, the value will be 1,
                otherwise it will be 0
            location_latitude (Union[Unset, str]): The approximate location of the respondent at the time the survey was
                taken
            location_longitude (Union[Unset, str]): The approximate location of the respondent at the time the survey was
                taken
            progress (Union[Unset, int]): How far the respondent has progressed through the survey as a percentage
            start_date (Union[Unset, datetime.datetime]): The point in time when the survey response was started
            user_language (Union[Unset, str]): The language of the respondent
    """

    distribution_channel: Union[Unset, str] = UNSET
    duration: Union[Unset, int] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    finished: Union[Unset, int] = UNSET
    location_latitude: Union[Unset, str] = UNSET
    location_longitude: Union[Unset, str] = UNSET
    progress: Union[Unset, int] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    user_language: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        distribution_channel = self.distribution_channel
        duration = self.duration
        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        finished = self.finished
        location_latitude = self.location_latitude
        location_longitude = self.location_longitude
        progress = self.progress
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        user_language = self.user_language

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if user_language is not UNSET:
            field_dict["userLanguage"] = user_language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        distribution_channel = d.pop("distributionChannel", UNSET)

        duration = d.pop("duration", UNSET)

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        finished = d.pop("finished", UNSET)

        location_latitude = d.pop("locationLatitude", UNSET)

        location_longitude = d.pop("locationLongitude", UNSET)

        progress = d.pop("progress", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        user_language = d.pop("userLanguage", UNSET)

        create_response_request_values = cls(
            distribution_channel=distribution_channel,
            duration=duration,
            end_date=end_date,
            finished=finished,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            progress=progress,
            start_date=start_date,
            user_language=user_language,
        )

        create_response_request_values.additional_properties = d
        return create_response_request_values

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
