from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.schema_property_data_type import SchemaPropertyDataType
from ..models.schema_property_format import SchemaPropertyFormat
from ..models.schema_property_type import SchemaPropertyType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_property_items import SchemaPropertyItems
    from ..models.survey_answer import SurveyAnswer


T = TypeVar("T", bound="SchemaProperty")


@_attrs_define
class SchemaProperty:
    """Each entry represents a field in the `values` field of the JSON survey response

    Attributes:
        type (SchemaPropertyType):
        description (str):
        format_ (Union[Unset, SchemaPropertyFormat]):
        question_id (Union[Unset, str]): The ID of the question this field is associated with
        loop_number (Union[Unset, int]): For loop and merge questions, this field documents which loop number the field
            in the JSON instance represents
        export_tag (Union[Unset, str]): The export tag of this field
        question_export_tag (Union[Unset, str]): The export tag of the question this field is associated with
        data_type (Union[Unset, SchemaPropertyDataType]): The type of data this field represents
        one_of (Union[Unset, List['SurveyAnswer']]):
        items (Union[Unset, SchemaPropertyItems]):
    """

    type: SchemaPropertyType
    description: str
    format_: Union[Unset, SchemaPropertyFormat] = UNSET
    question_id: Union[Unset, str] = UNSET
    loop_number: Union[Unset, int] = UNSET
    export_tag: Union[Unset, str] = UNSET
    question_export_tag: Union[Unset, str] = UNSET
    data_type: Union[Unset, SchemaPropertyDataType] = UNSET
    one_of: Union[Unset, List["SurveyAnswer"]] = UNSET
    items: Union[Unset, "SchemaPropertyItems"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        description = self.description
        format_: Union[Unset, str] = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

        question_id = self.question_id
        loop_number = self.loop_number
        export_tag = self.export_tag
        question_export_tag = self.question_export_tag
        data_type: Union[Unset, str] = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = self.data_type.value

        one_of: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.one_of, Unset):
            one_of = []
            for one_of_item_data in self.one_of:
                one_of_item = one_of_item_data.to_dict()

                one_of.append(one_of_item)

        items: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "description": description,
            }
        )
        if format_ is not UNSET:
            field_dict["format"] = format_
        if question_id is not UNSET:
            field_dict["questionId"] = question_id
        if loop_number is not UNSET:
            field_dict["loopNumber"] = loop_number
        if export_tag is not UNSET:
            field_dict["exportTag"] = export_tag
        if question_export_tag is not UNSET:
            field_dict["questionExportTag"] = question_export_tag
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if one_of is not UNSET:
            field_dict["oneOf"] = one_of
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.schema_property_items import SchemaPropertyItems
        from ..models.survey_answer import SurveyAnswer

        d = src_dict.copy()
        type = SchemaPropertyType(d.pop("type"))

        description = d.pop("description")

        _format_ = d.pop("format", UNSET)
        format_: Union[Unset, SchemaPropertyFormat]
        if isinstance(_format_, Unset):
            format_ = UNSET
        else:
            format_ = SchemaPropertyFormat(_format_)

        question_id = d.pop("questionId", UNSET)

        loop_number = d.pop("loopNumber", UNSET)

        export_tag = d.pop("exportTag", UNSET)

        question_export_tag = d.pop("questionExportTag", UNSET)

        _data_type = d.pop("dataType", UNSET)
        data_type: Union[Unset, SchemaPropertyDataType]
        if isinstance(_data_type, Unset):
            data_type = UNSET
        else:
            data_type = SchemaPropertyDataType(_data_type)

        one_of = []
        _one_of = d.pop("oneOf", UNSET)
        for one_of_item_data in _one_of or []:
            one_of_item = SurveyAnswer.from_dict(one_of_item_data)

            one_of.append(one_of_item)

        _items = d.pop("items", UNSET)
        items: Union[Unset, SchemaPropertyItems]
        if isinstance(_items, Unset):
            items = UNSET
        else:
            items = SchemaPropertyItems.from_dict(_items)

        schema_property = cls(
            type=type,
            description=description,
            format_=format_,
            question_id=question_id,
            loop_number=loop_number,
            export_tag=export_tag,
            question_export_tag=question_export_tag,
            data_type=data_type,
            one_of=one_of,
            items=items,
        )

        schema_property.additional_properties = d
        return schema_property

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
