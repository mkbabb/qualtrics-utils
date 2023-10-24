from __future__ import annotations

import datetime
import urllib.parse
import zipfile
from io import BytesIO
from typing import IO, Any, Optional
from zipfile import ZipFile

import pandas as pd
import requests

from qualtrics_utils.misc import BASE_URL, HEADERS, VERSION, ExportedFile
from qualtrics_utils.surveys_response_import_export_api_client.api.response_exports import (
    create_export,
    get_export_file,
    get_export_progress,
)
from qualtrics_utils.surveys_response_import_export_api_client.client import (
    AuthenticatedClient,
)
from qualtrics_utils.surveys_response_import_export_api_client.models import (
    ExportCreationRequest,
    ExportCreationRequestFormat,
    RequestStatus,
)
from qualtrics_utils.surveys_response_import_export_api_client.types import UNSET
from qualtrics_utils.utils import parse_file_id, reset_request_defaults

# The first two rows of the CSV are Qualtrics metadata.
SKIP_ROWS = [1, 2]

# These columns are parsed as dates.
PARSE_DATES = ["StartDate", "EndDate"]


class Surveys:
    def __init__(self, api_token: str, version: str = VERSION):
        self.base_url = BASE_URL(version)

        self.headers = HEADERS.copy()
        self.headers["X-API-TOKEN"] = api_token

        self.version = version

        self.client = AuthenticatedClient(
            token=api_token,
            base_url=self.base_url,
            prefix="",
            auth_header_name="X-API-TOKEN",
        )

    @staticmethod
    def _get_zip(url: str) -> IO[bytes] | list[IO[bytes]]:
        r = requests.get(url)
        with BytesIO(r.content) as data, ZipFile(data) as zipfile:
            files = [zipfile.open(file_name) for file_name in zipfile.namelist()]
            return files.pop() if len(files) == 1 else files

    def _make_api_url(self, url: str, **kwargs: Any) -> str:
        return urllib.parse.urljoin(self.base_url, url.format(**kwargs))

    def _response_export(
        self,
        survey_id: str,
        format: ExportCreationRequestFormat = ExportCreationRequestFormat.CSV,
        use_labels: bool = True,
        end_date: datetime.datetime | None = None,
        start_date: datetime.datetime | None = None,
        export_responses_in_progress: bool = False,
        continuation_token: Optional[str] = None,
        **kwargs: Any,
    ):
        kwargs = dict(
            format_=format,
            use_labels=use_labels,
            breakout_sets=True,
            seen_unanswered_recode=-1,
            multiselect_seen_unanswered_recode=-1,
            allow_continuation=not export_responses_in_progress,
            sort_by_last_modified_date=False,
            include_label_columns=not use_labels,
            compress=True,
            export_responses_in_progress=export_responses_in_progress,
            end_date=end_date if end_date is not None else UNSET,
            start_date=start_date if start_date is not None else UNSET,
            continuation_token=continuation_token
            if continuation_token is not None
            else UNSET,
            **kwargs,
        )
        payload = ExportCreationRequest(**kwargs)
        # ! This is a HACK because the Qualtrics OpenAPI docs suck tremendously and the defaults are NOT correct.
        payload = reset_request_defaults(payload, kwargs)

        return create_export.sync(
            survey_id=survey_id,
            client=self.client,
            json_body=payload,
        )

    def _response_export_status(self, survey_id: str, export_progress_id: str):
        while True:
            r = get_export_progress.sync(
                survey_id=survey_id,
                export_progress_id=export_progress_id,
                client=self.client,
            )
            status = r.result.status  # type: ignore
            match status:
                case None | RequestStatus.FAILED:
                    raise Exception("Export failed", r)
                case RequestStatus.COMPLETE:
                    return r
                case RequestStatus.INPROGRESS:
                    continue

    def _response_export_file(self, survey_id: str, file_id: str) -> bytes:
        r = get_export_file.sync(
            survey_id=survey_id,
            file_id=file_id,
            client=self.client,
        )
        return r.payload.read()  # type: ignore

    def get_responses(
        self,
        survey_id: str,
        format: ExportCreationRequestFormat = ExportCreationRequestFormat.CSV,
        use_labels: bool = True,
        end_date: datetime.datetime | None = None,
        start_date: datetime.datetime | None = None,
        export_responses_in_progress: bool = False,
        continuation_token: Optional[str] = None,
        last_response_id: Optional[str] = None,
        **kwargs: Any,
    ) -> ExportedFile[bytes]:
        """Get responses from a survey by survey_id.
        Outputs a zipped file, in bytes, in the format specified by `format`.

        If a `last_response_id` is provided, the export will continue from the response after the last_response_id.
        If a `continuation_token` is provided, the export will continue from where it left off. The continuation_token **cannot** be older than 1 week.

        Args:
            survey_id (str): The survey_id of the survey to get responses from.
            format (str, optional): The format of the response data. Defaults to "csv".
            use_labels (bool, optional): Whether to use labels for the column names. Defaults to True.
            end_date (Optional[datetime.datetime], optional): The end date for the response export. Defaults to None.
            start_date (Optional[datetime.datetime], optional): The start date for the response export. Defaults to None.
            export_responses_in_progress (bool, optional): Whether to export responses that are in progress. Defaults to False.
            continuation_token (Optional[str], optional): The continuation token for the response export. Defaults to None.
            last_response_id (Optional[str], optional): The responseId of the last response to export. Defaults to None.
        """
        survey_id = parse_file_id(survey_id)

        start_date = (
            self._response_id_to_date(survey_id=survey_id, response_id=last_response_id)
            if start_date is None and last_response_id is not None
            else start_date
        )

        export = self._response_export(
            survey_id=survey_id,
            format=format,
            use_labels=use_labels,
            end_date=end_date,
            start_date=start_date,
            export_responses_in_progress=export_responses_in_progress,
            continuation_token=continuation_token,
            **kwargs,
        )

        progress_id = export.result.progress_id
        export_status = self._response_export_status(
            survey_id=survey_id, export_progress_id=progress_id
        )

        file_id = export_status.result.file_id
        file = self._response_export_file(survey_id=survey_id, file_id=file_id)

        return ExportedFile(
            survey_id=survey_id,
            file_id=file_id,
            last_response_id=None,
            continuation_token=export_status.result.continuation_token,
            data=file,
            timestamp=datetime.datetime.now(),
        )

    def get_response(self, survey_id: str, response_id: str) -> dict[str, Any]:
        """Get a single response from a survey by survey_id and response_id.

        Args:
            survey_id (str): The survey_id of the survey to get the response from.
            response_id (str): The response_id of the response to get.
        """
        survey_id = parse_file_id(survey_id)

        response_url = self._make_api_url(
            "surveys/{survey_id}/responses/{response_id}",
            survey_id=survey_id,
            response_id=response_id,
        )
        r = requests.get(response_url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def _response_id_to_date(
        self, survey_id: str, response_id: str
    ) -> datetime.datetime | None:
        response = self.get_response(survey_id=survey_id, response_id=response_id)

        return datetime.datetime.fromisoformat(
            response["result"]["values"]["startDate"]
        )

    def get_responses_df(
        self,
        survey_id: str,
        use_labels: bool = True,
        end_date: datetime.datetime | None = None,
        start_date: datetime.datetime | None = None,
        export_responses_in_progress: bool = False,
        continuation_token: Optional[str] = None,
        last_response_id: Optional[str] = None,
        filter_preview: bool = True,
        parse_dates: list[str] = PARSE_DATES,
        **kwargs: Any,
    ) -> ExportedFile[pd.DataFrame]:
        """Get responses from a survey by survey_id.
        Outputs a pandas DataFrame, with the index set to `ResponseId`.

        All blank values therein are replaced with pd.NA.,
        and all columns that are entirely pd.NA are cast to an object.

        If a last_response_id is provided, the export will continue from the response after the last_response_id.
        If a continuation_token is provided, the export will continue from where it left off. The continuation_token **cannot** be older than 1 week.

        Additional keyword arguments are passed to `get_responses`, see the ExportCreationRequest model for more details.

        Args:
            survey_id (str): The survey_id of the survey to get responses from.
            use_labels (bool, optional): Whether to use labels for the column names. Defaults to True.
            end_date (Optional[datetime.datetime], optional): The end date for the response export. Defaults to None.
            start_date (Optional[datetime.datetime], optional): The start date for the response export. Defaults to None.
            export_responses_in_progress (bool, optional): Whether to export responses that are in progress. Defaults to False.
            continuation_token (Optional[str], optional): The continuation token for the response export. Defaults to None.
            last_response_id (Optional[str], optional): The responseId of the last response to export. Defaults to None.
            filter_preview (bool, optional): Whether to filter out Survey Preview responses. Defaults to True.
            parse_dates (list[str], optional): List of columns to parse as dates. Defaults to ["StartDate", "EndDate"].
        """
        survey_id = parse_file_id(survey_id)

        raw_data = self.get_responses(
            survey_id=survey_id,
            use_labels=use_labels,
            end_date=end_date,
            start_date=start_date,
            export_responses_in_progress=export_responses_in_progress,
            continuation_token=continuation_token,
            last_response_id=last_response_id,
            **kwargs,
        )

        with zipfile.ZipFile(BytesIO(raw_data.data)) as data:
            with data.open(data.filelist[0]) as f:
                new_df_reader = pd.read_csv(
                    f,
                    skiprows=SKIP_ROWS,
                    parse_dates=parse_dates,
                    iterator=True,
                )
                new_df = pd.concat(new_df_reader, ignore_index=True)
                new_df.set_index("ResponseId", inplace=True)

                # If the last response is the same as the last response from the previous export, drop it.
                if not new_df.empty and new_df.index[0] == last_response_id:
                    new_df.drop(new_df.index[0], inplace=True)
                # Sort by StartDate
                new_df.sort_values("StartDate", inplace=True)
                # Replace all blank values with pd.NA
                new_df.replace([r"^\s*$", "-1", -1], pd.NA, regex=True, inplace=True)
                # Cast all columns that are entirely pd.NA to object (str)
                new_df = new_df.astype(
                    {
                        col: "object"
                        for col in new_df.columns
                        if new_df[col].isna().all()
                    }
                )
                # Filter out Survey Preview responses
                if filter_preview and "Status" in new_df.columns:
                    new_df = new_df[new_df["Status"] != "Survey Preview"]

                # Set the last_response_id to the last response in the DataFrame, or the last_response_id from the previous export.
                last_response_id = (
                    new_df.index[-1] if len(new_df) > 0 else last_response_id
                )

                return ExportedFile(
                    survey_id=raw_data.survey_id,
                    file_id=raw_data.file_id,
                    last_response_id=last_response_id,
                    continuation_token=raw_data.continuation_token,
                    data=new_df,
                    timestamp=datetime.datetime.now(),
                )

    def get_survey_schema(self, survey_id: str) -> dict[str, Any]:
        """Get the schema of a survey by survey_id.

        Args:
            survey_id (str): The survey_id of the survey to get the schema from.
        """
        survey_id = parse_file_id(survey_id)
        schema_url = self._make_api_url("{survey_id}", survey_id=survey_id)
        r = requests.get(schema_url, headers=HEADERS)
        r.raise_for_status()
        return r.json()
