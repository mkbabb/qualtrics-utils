from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateResponseWithFileAttachmentsRequestFileMapping")


@_attrs_define
class CreateResponseWithFileAttachmentsRequestFileMapping:
    """
    Attributes:
        file1 (Union[Unset, str]): The QuestionID of the file upload question to map file1 to Example: QID1.
        file2 (Union[Unset, str]): The QuestionID of the file upload question to map file2 to Example: QID2.
        file3 (Union[Unset, str]): The QuestionID of the file upload question to map file3 to Example: QID3.
        file4 (Union[Unset, str]): The QuestionID of the file upload question to map file4 to Example: QID4.
        file5 (Union[Unset, str]): The QuestionID of the file upload question to map file5 to Example: QID5.
    """

    file1: Union[Unset, str] = UNSET
    file2: Union[Unset, str] = UNSET
    file3: Union[Unset, str] = UNSET
    file4: Union[Unset, str] = UNSET
    file5: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file1 = self.file1
        file2 = self.file2
        file3 = self.file3
        file4 = self.file4
        file5 = self.file5

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file1 is not UNSET:
            field_dict["file1"] = file1
        if file2 is not UNSET:
            field_dict["file2"] = file2
        if file3 is not UNSET:
            field_dict["file3"] = file3
        if file4 is not UNSET:
            field_dict["file4"] = file4
        if file5 is not UNSET:
            field_dict["file5"] = file5

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file1 = d.pop("file1", UNSET)

        file2 = d.pop("file2", UNSET)

        file3 = d.pop("file3", UNSET)

        file4 = d.pop("file4", UNSET)

        file5 = d.pop("file5", UNSET)

        create_response_with_file_attachments_request_file_mapping = cls(
            file1=file1,
            file2=file2,
            file3=file3,
            file4=file4,
            file5=file5,
        )

        create_response_with_file_attachments_request_file_mapping.additional_properties = (
            d
        )
        return create_response_with_file_attachments_request_file_mapping

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
