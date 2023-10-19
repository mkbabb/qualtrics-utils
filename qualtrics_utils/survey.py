from __future__ import annotations

import datetime
import urllib.parse
import zipfile
from http import HTTPStatus
from io import BytesIO
from typing import IO, Any, List, Optional, TypedDict
from zipfile import ZipFile

import pandas as pd
import requests

from qualtrics_utils.misc import BASE_URL, HEADERS, VERSION, ExportedFile
from qualtrics_utils.surveys_response_import_export_api_client.api.response_exports import (
    create_export,
    get_export_file,
    get_export_progress,
    get_filters_list,
)
from qualtrics_utils.surveys_response_import_export_api_client.client import (
    AuthenticatedClient,
)
from qualtrics_utils.surveys_response_import_export_api_client.models import (
    ExportCreationRequest,
    ExportCreationRequestFormat,
    ExportStatusResponse,
    ExportStatusResponseResult,
    RequestStatus,
)
from qualtrics_utils.surveys_response_import_export_api_client.types import UNSET

SKIP_ROWS = [1, 2]


class Surveys:
    def __init__(self, api_token: str, version: str = VERSION):
        self.base_url = BASE_URL(version)

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
        continuation_token: Optional[str] = None,
    ):
        payload = ExportCreationRequest(
            format_=format,
            use_labels=use_labels,
            breakout_sets=True,
            seen_unanswered_recode=-1,
            multiselect_seen_unanswered_recode=-1,
            allow_continuation=continuation_token is not None,
            sort_by_last_modified_date=True,
            time_zone=UNSET,
            include_label_columns=not use_labels,
        )
        if end_date is not None:
            payload.end_date = end_date
        if start_date is not None:
            payload.start_date = start_date
        if continuation_token is not None:
            payload.continuation_token = continuation_token

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
            if r is None:
                return None

            status = r["result"]["status"]

            match status:
                case None:
                    return None
                case RequestStatus.COMPLETE:
                    return r
                case RequestStatus.FAILED:
                    return None
                case RequestStatus.INPROGRESS:
                    continue

    def _response_export_file(self, survey_id: str, file_id: str) -> bytes | None:
        r = get_export_file.sync(
            survey_id=survey_id,
            file_id=file_id,
            client=self.client,
        )
        if r is None:
            return None

        return r["payload"].read()  # type: ignore

    def get_responses(
        self,
        survey_id: str,
        format: ExportCreationRequestFormat = ExportCreationRequestFormat.CSV,
        continuation_token: Optional[str] = None,
    ) -> ExportedFile[bytes] | None:
        """Get responses from a survey by survey_id.
        Outputs a file-like object, primarily containing bytes data in the format specified.

        If a continuation_token is provided, the export will continue from where it left off.

        Args:
            survey_id (str): The survey_id of the survey to get responses from.
            format (str, optional): The format of the response data. Defaults to "csv".
            continuation_token (Optional[str], optional): The continuation token for the response export. Defaults to None.
        """
        export = self._response_export(
            survey_id=survey_id, format=format, continuation_token=continuation_token
        )
        if export is None:
            return None

        progress_id = export.result.progress_id
        export_status = self._response_export_status(
            survey_id=survey_id, export_progress_id=progress_id
        )
        if export_status is None:
            return None

        file_id = export_status.result.file_id
        file = self._response_export_file(survey_id=survey_id, file_id=file_id)

        if file is None:
            return None

        return ExportedFile(
            survey_id=survey_id,
            file_id=file_id,
            continuation_token=export_status.result.continuation_token,
            data=file,
        )

    def get_response(self, survey_id: str, responseId: str) -> dict[str, Any] | None:
        """Get a single response from a survey by survey_id and responseId.

        Args:
            survey_id (str): The survey_id of the survey to get the response from.
            responseId (str): The responseId of the response to get.
        """
        response_url = self._make_api_url(
            "{survey_id}/responses/{responseId}",
            survey_id=survey_id,
            responseId=responseId,
        )

        r = requests.get(response_url, headers=HEADERS)

        if r.status_code != HTTPStatus.OK:
            return None
        else:
            return r.json()

    def get_responses_df(
        self,
        survey_id: str,
        continuation_token: Optional[str] = None,
        filter_preview: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> ExportedFile[pd.DataFrame] | None:
        """Get responses from a survey by survey_id.
        Outputs a pandas DataFrame, with the index set to the ResponseId.

        All blank values therein are replaced with pd.NA.,
        and all columns that are entirely pd.NA. are cast to object.

        If a continuation_token is provided, the export will continue from where it left off.

        Args:
            survey_id (str): The survey_id of the survey to get responses from.
            continuation_token (Optional[str], optional): The continuation token for the response export. Defaults to None.
            *args: Additional arguments to pass to pandas.read_csv.
            **kwargs: Additional keyword arguments to pass to pandas.read_csv.
        """

        raw_data = self.get_responses(
            survey_id=survey_id, continuation_token=continuation_token
        )
        if raw_data is None:
            return None

        with zipfile.ZipFile(BytesIO(raw_data.data)) as data:
            with data.open(data.filelist[0]) as f:
                new_df_reader = pd.read_csv(
                    f, skiprows=SKIP_ROWS, *args, **kwargs, iterator=True
                )
                new_df = pd.concat(new_df_reader, ignore_index=True)
                new_df.set_index("ResponseId", inplace=True)

                new_df.replace([r"^\s*$", "-1", -1], pd.NA, regex=True, inplace=True)

                new_df = new_df.astype(
                    {
                        col: "object"
                        for col in new_df.columns
                        if new_df[col].isna().all()
                    }
                )

                if filter_preview and "Status" in new_df.columns:
                    new_df = new_df[new_df["Status"] != "Survey Preview"]

                return ExportedFile(
                    survey_id=raw_data.survey_id,
                    file_id=raw_data.file_id,
                    continuation_token=raw_data.continuation_token,
                    data=new_df,
                )

    def get_survey_schema(self, survey_id: str) -> dict[str, Any] | None:
        """Get the schema of a survey by survey_id.

        Args:
            survey_id (str): The survey_id of the survey to get the schema from.
        """
        schema_url = self._make_api_url("{survey_id}", survey_id=survey_id)
        r = requests.get(schema_url, headers=HEADERS)

        if r.status_code != HTTPStatus.OK:
            return None
        else:
            return r.json()
