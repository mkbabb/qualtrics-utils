import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.export_creation_request_format import ExportCreationRequestFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportCreationRequest")


@_attrs_define
class ExportCreationRequest:
    """
    Attributes:
        format_ (ExportCreationRequestFormat): The format of the export file. This can be one of: `csv`, `tsv`, `json`,
            `ndjson`, `spss`, or `xml` Default: ExportCreationRequestFormat.CSV. Example: csv.
        breakout_sets (Union[Unset, bool]): If true, split multi-value fields into columns. Default: True. Example:
            true.
        compress (Union[Unset, bool]): Compress the final export file as a ZIP file. Exporting without compression is
            only recommended for small exports. Large exports may encounter issues when downloading the large files. It is
            possible in the future that if an export size is too large uncompressed, this flag will be ignored and it will
            be compressed anyway. Default: True. Example: true.
        end_date (Union[Unset, datetime.datetime]): Only export responses recorded before the specified date unless
            `sortByLastModifiedDate` is true. In which case only export responses created or modified before the date. See
            <a href="https://api.qualtrics.com/api-reference/docs/Instructions/dates-and-times.md">Dates and Times</a> for
            more information on the date and time format. The end date is exclusive. Default:
            isoparse('2100-01-01T01:00:00Z'). Example: 2040-02-01T01:50:00Z.
        export_responses_in_progress (Union[Unset, bool]): Only export responses not yet complete. Note that
            `sortByLastModifiedDate` doesn't have any impact when this is set to `true`. Default: True. Example: false.
        filter_id (Union[Unset, str]): If you provide a `filterId`, the export will only return responses matching the
            corresponding filter. For more information on filters and how to create them, see <a
            href="https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/filtering-
            responses/">Filtering Responses</a> at Qualtrics Support, or read the <a
            href="https://api.qualtrics.com/instructions/YXBpOjYwOTI5-surveys-response-import-export-api#export-using-a-
            filter">response import/export API overview section on using filters</a>. Example:
            9b67fbb7-ef89-430d-8ddf-f17f44de9254.
        format_decimal_as_comma (Union[Unset, bool]): If `true`, use a comma as a decimal separator instead of a period.
            Default: True. Example: false.
        include_display_order (Union[Unset, bool]): If `true`, include display order information in your export. This is
            useful for surveys with randomization. Note that if used alongside the `embeddedDataIds`, `questionIds`, or
            `surveyMetadataIds` parameters, this will only apply to the display order information for questions. Flow and
            block display order information will always be included. Default: True. Example: false.
        limit (Union[Unset, int]): Maximum number of responses to export. Example: 50.
        multiselect_seen_unanswered_recode (Union[Unset, int]): Recode seen-but-unanswered choices for multi-select
            questions with this value. If not set, this will be the `seenUnansweredRecode` value. Example: 99.
        newline_replacement (Union[Unset, str]): If set, replace newline characters in survey responses with this value.
            Note: this parameter is only relevant for CSV and TSV.
        seen_unanswered_recode (Union[Unset, int]): Recode seen-but-unanswered questions with this value. Example: 0.
        start_date (Union[Unset, datetime.datetime]): Only export responses recorded after the specified date unless
            `sortByLastModifiedDate` is true. In which case only export responses created or modified after the date. See <a
            href="https://api.qualtrics.com/api-reference/docs/Instructions/dates-and-times.md">Dates and Times</a> for more
            information on the date and time format. The start date is inclusive. Default: isoparse('1970-01-01T01:00:00Z').
            Example: 2018-01-01T01:50:00Z.
        time_zone (Union[Unset, str]): Timezone used to determine response date values. Data is recorded in UTC, and
            translates that value to your local time. This can be useful for local survey deadlines. See <a
            href="https://api.qualtrics.com/api-reference/docs/Instructions/dates-and-times.md">Dates and Times</a> for more
            information on time zone format. If this parameter is not provided, dates will be exported in UTC/GMT. Default:
            'UTC'. Example: America/Chicago.
        use_labels (Union[Unset, bool]): Instead of exporting the recode (numeric) value for the answer choice, export
            the text of the answer choice. For more information on recode values, see <a
            href="https://www.qualtrics.com/support/survey-platform/survey-module/question-options/recode-values/">Recode
            Values</a> on the Qualtrics Support Page. Default: True. Example: false.
        embedded_data_ids (Union[Unset, List[str]]): If provided, only export embedded data fields from the provided
            list of Embedded Data IDs. For more information see <a href="https://www.qualtrics.com/support/survey-
            platform/survey-module/survey-flow/standard-elements/embedded-data/">Embedded Data</a>
        question_ids (Union[Unset, List[str]]): If provided, only export answers from the provided list of Question IDs
        survey_metadata_ids (Union[Unset, List[str]]): If provided, only export metadata fields from the provided list
            of Metadata IDs. This will remove metadata included in export by default. The list of those fields is below:
            </dt><dd>
                <dl>
                    <dt><b>startDate</b></dt><dd>Start Date</dd>
                    <dt><b>endDate</b></dt><dd>End Date</dd>
                    <dt><b>status</b></dt><dd>Survey Response type (info found <a
            href="https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-
            data/understanding-your-dataset/#RespondentInformation">here</a>)</dd>
                    <dt><b>ipAddress</b></dt><dd>IP Address</dd>
                    <dt><b>progress</b></dt><dd>Progress (percentage)</dd>
                    <dt><b>duration</b></dt><dd>Duration (in seconds)</dd>
                    <dt><b>finished</b></dt><dd>boolean for whether or not the survey is complete</dd>
                    <dt><b>recordedDate</b></dt><dd>Recorded Date</dd>
                    <dt><b>_recordId</b></dt><dd>Response ID</dd>
                    <dt><b>locationLatitude</b></dt><dd>Latitude</dd>
                    <dt><b>locationLongitude</b></dt><dd>Longitude</dd>
                    <dt><b>recipientLastName</b></dt><dd>Recipient Last Name</dd>
            .       <dt><b>recipientFirstName</b></dt><dd>Recipient First Name</dd>
            .       <dt><b>recipientEmail</b></dt><dd>Recipient Email</dd>
            .       <dt><b>externalReference</b></dt><dd>External Reference</dd>
            .       <dt><b>distributionChannel</b></dt><dd>Distribution Channel</dd>
            </dl>
        continuation_token (Union[Unset, str]): Provide the continuation token returned from a previous export in order
            to get new responses recorded (or updated, if `sortByLastModifiedDate` is set to `true`) since that export. Note
            that a token is only returned if either `allowContinuation` or `continuationToken` is set. Continuation tokens
            expire after a week. If you provide a continuation token, it implies `allowContinuation` and you must not
            include the `allowContinuation` field. Example:
            UQhcCBAIGwgGCFkIEBscGhIcHxkZHxwGCEQIEBwYGxoaGhoaGgYITwgQGxwaExgcGhkYE1c.
        allow_continuation (Union[Unset, bool]): Set this to `true` to request a continuation token when this export has
            finished. Note, when this is set to true, you cannot include a filter. Default: True. Example: false.
        include_label_columns (Union[Unset, bool]): For columns that have answer labels, export two columns: one that
            uses recode values and one that uses labels. The label column has an `IsLabelsColumn` field in the 3rd header
            row. Note that this cannot be used with `useLabels`. Use this setting if you wish to export both column labels
            and numeric values in the same export. Default: True. Example: false.
        sort_by_last_modified_date (Union[Unset, bool]): Sort responses by modified date, which represents the date when
            a response was last updated or the creation time if the response hasn't changed since it was recorded. Note,
            when this is set to `true`, `startDate` and/or `endDate`, if provided, will be used to filter responses based on
            the modified date instead of the creation time alone. This parameter cannot be used together with the `filterId`
            parameter. Also, the modified date will be automatically included under an additional `LastModifiedDate` column
            in the export. `sortByLastModifiedDate` can be used in conjunction with `continuationToken` to periodically get
            all the new and modified responses since the last export and is the recommended way of handling that use case.
            Default: True. Example: false.
    """

    format_: ExportCreationRequestFormat = ExportCreationRequestFormat.CSV
    breakout_sets: Union[Unset, bool] = True
    compress: Union[Unset, bool] = True
    end_date: Union[Unset, datetime.datetime] = isoparse("2100-01-01T01:00:00Z")
    export_responses_in_progress: Union[Unset, bool] = True
    filter_id: Union[Unset, str] = UNSET
    format_decimal_as_comma: Union[Unset, bool] = True
    include_display_order: Union[Unset, bool] = True
    limit: Union[Unset, int] = UNSET
    multiselect_seen_unanswered_recode: Union[Unset, int] = UNSET
    newline_replacement: Union[Unset, str] = UNSET
    seen_unanswered_recode: Union[Unset, int] = UNSET
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T01:00:00Z")
    time_zone: Union[Unset, str] = "UTC"
    use_labels: Union[Unset, bool] = True
    embedded_data_ids: Union[Unset, List[str]] = UNSET
    question_ids: Union[Unset, List[str]] = UNSET
    survey_metadata_ids: Union[Unset, List[str]] = UNSET
    continuation_token: Union[Unset, str] = UNSET
    allow_continuation: Union[Unset, bool] = True
    include_label_columns: Union[Unset, bool] = True
    sort_by_last_modified_date: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        format_ = self.format_.value

        breakout_sets = self.breakout_sets
        compress = self.compress
        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        export_responses_in_progress = self.export_responses_in_progress
        filter_id = self.filter_id
        format_decimal_as_comma = self.format_decimal_as_comma
        include_display_order = self.include_display_order
        limit = self.limit
        multiselect_seen_unanswered_recode = self.multiselect_seen_unanswered_recode
        newline_replacement = self.newline_replacement
        seen_unanswered_recode = self.seen_unanswered_recode
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        time_zone = self.time_zone
        use_labels = self.use_labels
        embedded_data_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.embedded_data_ids, Unset):
            embedded_data_ids = self.embedded_data_ids

        question_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.question_ids, Unset):
            question_ids = self.question_ids

        survey_metadata_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.survey_metadata_ids, Unset):
            survey_metadata_ids = self.survey_metadata_ids

        continuation_token = self.continuation_token
        allow_continuation = self.allow_continuation
        include_label_columns = self.include_label_columns
        sort_by_last_modified_date = self.sort_by_last_modified_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "format": format_,
            }
        )
        if breakout_sets is not UNSET:
            field_dict["breakoutSets"] = breakout_sets
        if compress is not UNSET:
            field_dict["compress"] = compress
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if export_responses_in_progress is not UNSET:
            field_dict["exportResponsesInProgress"] = export_responses_in_progress
        if filter_id is not UNSET:
            field_dict["filterId"] = filter_id
        if format_decimal_as_comma is not UNSET:
            field_dict["formatDecimalAsComma"] = format_decimal_as_comma
        if include_display_order is not UNSET:
            field_dict["includeDisplayOrder"] = include_display_order
        if limit is not UNSET:
            field_dict["limit"] = limit
        if multiselect_seen_unanswered_recode is not UNSET:
            field_dict[
                "multiselectSeenUnansweredRecode"
            ] = multiselect_seen_unanswered_recode
        if newline_replacement is not UNSET:
            field_dict["newlineReplacement"] = newline_replacement
        if seen_unanswered_recode is not UNSET:
            field_dict["seenUnansweredRecode"] = seen_unanswered_recode
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if use_labels is not UNSET:
            field_dict["useLabels"] = use_labels
        if embedded_data_ids is not UNSET:
            field_dict["embeddedDataIds"] = embedded_data_ids
        if question_ids is not UNSET:
            field_dict["questionIds"] = question_ids
        if survey_metadata_ids is not UNSET:
            field_dict["surveyMetadataIds"] = survey_metadata_ids
        if continuation_token is not UNSET:
            field_dict["continuationToken"] = continuation_token
        if allow_continuation is not UNSET:
            field_dict["allowContinuation"] = allow_continuation
        if include_label_columns is not UNSET:
            field_dict["includeLabelColumns"] = include_label_columns
        if sort_by_last_modified_date is not UNSET:
            field_dict["sortByLastModifiedDate"] = sort_by_last_modified_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        format_ = ExportCreationRequestFormat(d.pop("format"))

        breakout_sets = d.pop("breakoutSets", UNSET)

        compress = d.pop("compress", UNSET)

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        export_responses_in_progress = d.pop("exportResponsesInProgress", UNSET)

        filter_id = d.pop("filterId", UNSET)

        format_decimal_as_comma = d.pop("formatDecimalAsComma", UNSET)

        include_display_order = d.pop("includeDisplayOrder", UNSET)

        limit = d.pop("limit", UNSET)

        multiselect_seen_unanswered_recode = d.pop(
            "multiselectSeenUnansweredRecode", UNSET
        )

        newline_replacement = d.pop("newlineReplacement", UNSET)

        seen_unanswered_recode = d.pop("seenUnansweredRecode", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        time_zone = d.pop("timeZone", UNSET)

        use_labels = d.pop("useLabels", UNSET)

        embedded_data_ids = cast(List[str], d.pop("embeddedDataIds", UNSET))

        question_ids = cast(List[str], d.pop("questionIds", UNSET))

        survey_metadata_ids = cast(List[str], d.pop("surveyMetadataIds", UNSET))

        continuation_token = d.pop("continuationToken", UNSET)

        allow_continuation = d.pop("allowContinuation", UNSET)

        include_label_columns = d.pop("includeLabelColumns", UNSET)

        sort_by_last_modified_date = d.pop("sortByLastModifiedDate", UNSET)

        export_creation_request = cls(
            format_=format_,
            breakout_sets=breakout_sets,
            compress=compress,
            end_date=end_date,
            export_responses_in_progress=export_responses_in_progress,
            filter_id=filter_id,
            format_decimal_as_comma=format_decimal_as_comma,
            include_display_order=include_display_order,
            limit=limit,
            multiselect_seen_unanswered_recode=multiselect_seen_unanswered_recode,
            newline_replacement=newline_replacement,
            seen_unanswered_recode=seen_unanswered_recode,
            start_date=start_date,
            time_zone=time_zone,
            use_labels=use_labels,
            embedded_data_ids=embedded_data_ids,
            question_ids=question_ids,
            survey_metadata_ids=survey_metadata_ids,
            continuation_token=continuation_token,
            allow_continuation=allow_continuation,
            include_label_columns=include_label_columns,
            sort_by_last_modified_date=sort_by_last_modified_date,
        )

        export_creation_request.additional_properties = d
        return export_creation_request

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
