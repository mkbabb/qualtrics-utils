import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RetrieveResponseResponseResultValues")


@_attrs_define
class RetrieveResponseResponseResultValues:
    """`values` is a set of key-value pairs corresponding to question-answer pairs. There can also be key-value pairs
    representing meta data for the response such as `startDate` or `userLanguage`.

        Attributes:
            end_date (datetime.datetime): The point in time when the survey response was finished
            finished (int): If the respondent finished and submitted the survey, the value will be 1, otherwise it will be 0
            recorded_date (datetime.datetime): The point in time when the survey response was recorded
            start_date (datetime.datetime): The point in time when the survey response was started
            status (int): The type of response
            distribution_channel (Union[Unset, str]): The method by which the survey was distributed to respondents
            duration (Union[Unset, int]): How long it took for the respondent to finish the survey in seconds
            location_latitude (Union[Unset, str]): The approximate location of the respondent at the time the survey was
                taken
            location_longitude (Union[Unset, str]): The approximate location of the respondent at the time the survey was
                taken
            progress (Union[Unset, int]): How far the respondent has progressed through the survey as a percentage
            user_language (Union[Unset, str]): The language of the respondent
    """

    end_date: datetime.datetime
    finished: int
    recorded_date: datetime.datetime
    start_date: datetime.datetime
    status: int
    distribution_channel: Union[Unset, str] = UNSET
    duration: Union[Unset, int] = UNSET
    location_latitude: Union[Unset, str] = UNSET
    location_longitude: Union[Unset, str] = UNSET
    progress: Union[Unset, int] = UNSET
    user_language: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        end_date = self.end_date.isoformat()

        finished = self.finished
        recorded_date = self.recorded_date.isoformat()

        start_date = self.start_date.isoformat()

        status = self.status
        distribution_channel = self.distribution_channel
        duration = self.duration
        location_latitude = self.location_latitude
        location_longitude = self.location_longitude
        progress = self.progress
        user_language = self.user_language

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endDate": end_date,
                "finished": finished,
                "recordedDate": recorded_date,
                "startDate": start_date,
                "status": status,
            }
        )
        if distribution_channel is not UNSET:
            field_dict["distributionChannel"] = distribution_channel
        if duration is not UNSET:
            field_dict["duration"] = duration
        if location_latitude is not UNSET:
            field_dict["locationLatitude"] = location_latitude
        if location_longitude is not UNSET:
            field_dict["locationLongitude"] = location_longitude
        if progress is not UNSET:
            field_dict["progress"] = progress
        if user_language is not UNSET:
            field_dict["userLanguage"] = user_language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        end_date = isoparse(d.pop("endDate"))

        finished = d.pop("finished")

        recorded_date = isoparse(d.pop("recordedDate"))

        start_date = isoparse(d.pop("startDate"))

        status = d.pop("status")

        distribution_channel = d.pop("distributionChannel", UNSET)

        duration = d.pop("duration", UNSET)

        location_latitude = d.pop("locationLatitude", UNSET)

        location_longitude = d.pop("locationLongitude", UNSET)

        progress = d.pop("progress", UNSET)

        user_language = d.pop("userLanguage", UNSET)

        retrieve_response_response_result_values = cls(
            end_date=end_date,
            finished=finished,
            recorded_date=recorded_date,
            start_date=start_date,
            status=status,
            distribution_channel=distribution_channel,
            duration=duration,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            progress=progress,
            user_language=user_language,
        )

        retrieve_response_response_result_values.additional_properties = d
        return retrieve_response_response_result_values

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
