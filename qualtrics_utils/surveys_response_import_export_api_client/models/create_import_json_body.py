from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_import_json_body_format import CreateImportJsonBodyFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImportJsonBody")


@_attrs_define
class CreateImportJsonBody:
    """
    Attributes:
        format_ (CreateImportJsonBodyFormat): Allowed values are CSV or TSV. See guide before for instructions on how to
            format CSV or TSV files. Default: CreateImportJsonBodyFormat.CSV.
        file_url (str): The URL of a CSV or TSV file containing the survey responses to import. Example:
            https://mydomain.com/importfile.csv.
        charset (Union[Unset, str]):  Default: 'UTF-8'.
    """

    file_url: str
    format_: CreateImportJsonBodyFormat = CreateImportJsonBodyFormat.CSV
    charset: Union[Unset, str] = "UTF-8"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        format_ = self.format_.value

        file_url = self.file_url
        charset = self.charset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "format": format_,
                "fileUrl": file_url,
            }
        )
        if charset is not UNSET:
            field_dict["charset"] = charset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        format_ = CreateImportJsonBodyFormat(d.pop("format"))

        file_url = d.pop("fileUrl")

        charset = d.pop("charset", UNSET)

        create_import_json_body = cls(
            format_=format_,
            file_url=file_url,
            charset=charset,
        )

        create_import_json_body.additional_properties = d
        return create_import_json_body

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
