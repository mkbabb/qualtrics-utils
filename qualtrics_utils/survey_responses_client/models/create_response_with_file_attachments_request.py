import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.create_response_request import CreateResponseRequest
    from ..models.create_response_with_file_attachments_request_file_mapping import (
        CreateResponseWithFileAttachmentsRequestFileMapping,
    )


T = TypeVar("T", bound="CreateResponseWithFileAttachmentsRequest")


@_attrs_define
class CreateResponseWithFileAttachmentsRequest:
    """
    Attributes:
        response (CreateResponseRequest):
        file_mapping (CreateResponseWithFileAttachmentsRequestFileMapping):
        file1 (Union[Unset, File]):
        file2 (Union[Unset, File]):
        file3 (Union[Unset, File]):
        file4 (Union[Unset, File]):
        file5 (Union[Unset, File]):
    """

    response: "CreateResponseRequest"
    file_mapping: "CreateResponseWithFileAttachmentsRequestFileMapping"
    file1: Union[Unset, File] = UNSET
    file2: Union[Unset, File] = UNSET
    file3: Union[Unset, File] = UNSET
    file4: Union[Unset, File] = UNSET
    file5: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        response = self.response.to_dict()

        file_mapping = self.file_mapping.to_dict()

        file1: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file1, Unset):
            file1 = self.file1.to_tuple()

        file2: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file2, Unset):
            file2 = self.file2.to_tuple()

        file3: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file3, Unset):
            file3 = self.file3.to_tuple()

        file4: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file4, Unset):
            file4 = self.file4.to_tuple()

        file5: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file5, Unset):
            file5 = self.file5.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "response": response,
                "fileMapping": file_mapping,
            }
        )
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

    def to_multipart(self) -> Dict[str, Any]:
        response = (
            None,
            json.dumps(self.response.to_dict()).encode(),
            "application/json",
        )

        file_mapping = (
            None,
            json.dumps(self.file_mapping.to_dict()).encode(),
            "application/json",
        )

        file1: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file1, Unset):
            file1 = self.file1.to_tuple()

        file2: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file2, Unset):
            file2 = self.file2.to_tuple()

        file3: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file3, Unset):
            file3 = self.file3.to_tuple()

        file4: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file4, Unset):
            file4 = self.file4.to_tuple()

        file5: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file5, Unset):
            file5 = self.file5.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                key: (None, str(value).encode(), "text/plain")
                for key, value in self.additional_properties.items()
            }
        )
        field_dict.update(
            {
                "response": response,
                "fileMapping": file_mapping,
            }
        )
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
        from ..models.create_response_request import CreateResponseRequest
        from ..models.create_response_with_file_attachments_request_file_mapping import (
            CreateResponseWithFileAttachmentsRequestFileMapping,
        )

        d = src_dict.copy()
        response = CreateResponseRequest.from_dict(d.pop("response"))

        file_mapping = CreateResponseWithFileAttachmentsRequestFileMapping.from_dict(
            d.pop("fileMapping")
        )

        _file1 = d.pop("file1", UNSET)
        file1: Union[Unset, File]
        if isinstance(_file1, Unset):
            file1 = UNSET
        else:
            file1 = File(payload=BytesIO(_file1))

        _file2 = d.pop("file2", UNSET)
        file2: Union[Unset, File]
        if isinstance(_file2, Unset):
            file2 = UNSET
        else:
            file2 = File(payload=BytesIO(_file2))

        _file3 = d.pop("file3", UNSET)
        file3: Union[Unset, File]
        if isinstance(_file3, Unset):
            file3 = UNSET
        else:
            file3 = File(payload=BytesIO(_file3))

        _file4 = d.pop("file4", UNSET)
        file4: Union[Unset, File]
        if isinstance(_file4, Unset):
            file4 = UNSET
        else:
            file4 = File(payload=BytesIO(_file4))

        _file5 = d.pop("file5", UNSET)
        file5: Union[Unset, File]
        if isinstance(_file5, Unset):
            file5 = UNSET
        else:
            file5 = File(payload=BytesIO(_file5))

        create_response_with_file_attachments_request = cls(
            response=response,
            file_mapping=file_mapping,
            file1=file1,
            file2=file2,
            file3=file3,
            file4=file4,
            file5=file5,
        )

        create_response_with_file_attachments_request.additional_properties = d
        return create_response_with_file_attachments_request

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
