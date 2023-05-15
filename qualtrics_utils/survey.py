import urllib.parse
import zipfile
from dataclasses import dataclass
from io import BytesIO
from typing import *
from zipfile import ZipFile

import pandas as pd
import requests

HEADERS = {"X-API-TOKEN": "", "Content-Type": "application/json"}

VERSION = "v3"

BASE_URL: Callable[
    [str], str
] = lambda x: f"https://yul1.qualtrics.com/API/{x}/surveys/"

T = TypeVar("T")


@dataclass
class ExportedFile(Generic[T]):
    fileId: str
    continuationToken: str
    data: T


class Surveys:
    def __init__(self, api_token: str, version: str = VERSION):
        self.headers = HEADERS
        self.headers["X-API-TOKEN"] = api_token

        self.version = version
        self.base_url = BASE_URL(version)

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
        surveyId: str,
        format: str = "csv",
        continuationToken: Optional[str] = None,
    ) -> dict[str, Any] | None:
        response_export_url = self._make_api_url(
            "{surveyId}/export-responses", surveyId=surveyId
        )

        payload = {
            "format": format,  # format of the exported file
            "useLabels": True,  # use labels instead of numerical values
            "breakoutSets": True,  # include breakout sets
            "seenUnansweredRecode": -1,  # recode seen but unanswered questions as -1
            "multiselectSeenUnansweredRecode": -1,  # recode multiselect seen but unanswered questions as -1
            "allowContinuation": True,  # allow continuation of export via continuationToken
        }
        if continuationToken:
            payload["continuationToken"] = continuationToken

        r = requests.post(
            response_export_url,
            json=payload,
            headers=HEADERS,
        )

        if r.status_code != 200:
            return None
        else:
            return r.json() # type: ignore

    def _response_export_progress(
        self, surveyId: str, exportProgressId: str
    ) -> dict[str, Any] | None:
        progress_url = self._make_api_url(
            "{surveyId}/export-responses/{exportProgressId}",
            surveyId=surveyId,
            exportProgressId=exportProgressId,
        )

        while True:
            r = requests.get(progress_url, headers=HEADERS)
            data: dict[str, Any] = r.json()

            match data["result"]["status"]:
                case "complete":
                    return data
                case "failed":
                    return None
                case "inProgress":
                    continue

    def _response_export_file(self, surveyId: str, fileId: str) -> bytes:
        get_response_file_url = self._make_api_url(
            "{surveyId}/export-responses/{fileId}/file",
            surveyId=surveyId,
            fileId=fileId,
        )

        r = requests.get(get_response_file_url, headers=HEADERS)

        return r.content

    def get_responses(
        self,
        surveyId: str,
        format: str = "csv",
        continuationToken: Optional[str] = None,
    ) -> ExportedFile[bytes] | None:
        """Get responses from a survey by surveyId.
        Outputs a file-like object, primarily containing bytes data in the format specified.

        If a continuationToken is provided, the export will continue from where it left off.

        Args:
            surveyId (str): The surveyId of the survey to get responses from.
            format (str, optional): The format of the response data. Defaults to "csv".
            continuationToken (Optional[str], optional): The continuation token for the response export. Defaults to None.
        """
        export = self._response_export(
            surveyId=surveyId, format=format, continuationToken=continuationToken
        )

        if export is None:
            return None

        progressId = export["result"]["progressId"]
        export_progress = self._response_export_progress(
            surveyId=surveyId, exportProgressId=progressId
        )
        if export_progress is None:
            return None

        fileId = export_progress["result"]["fileId"]
        file = self._response_export_file(surveyId=surveyId, fileId=fileId)

        return ExportedFile(
            fileId=fileId,
            continuationToken=export_progress["result"]["continuationToken"],
            data=file,
        )

    def get_response(self, surveyId: str, responseId: str) -> dict[str, Any] | None:
        """Get a single response from a survey by surveyId and responseId.

        Args:
            surveyId (str): The surveyId of the survey to get the response from.
            responseId (str): The responseId of the response to get.
        """
        response_url = self._make_api_url(
            "{surveyId}/responses/{responseId}",
            surveyId=surveyId,
            responseId=responseId,
        )

        r = requests.get(response_url, headers=HEADERS)

        if r.status_code != 200:
            return None
        else:
            return r.json() # type: ignore

    def get_responses_df(
        self,
        surveyId: str,
        continuationToken: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> ExportedFile[pd.DataFrame] | None:
        """Get responses from a survey by surveyId.
        Outputs a pandas DataFrame, with the index set to the ResponseId.

        All blank values therein are replaced with pd.NA.,
        and all columns that are entirely pd.NA. are cast to object.

        If a continuationToken is provided, the export will continue from where it left off.

        Args:
            surveyId (str): The surveyId of the survey to get responses from.
            continuationToken (Optional[str], optional): The continuation token for the response export. Defaults to None.
            *args: Additional arguments to pass to pandas.read_csv.
            **kwargs: Additional keyword arguments to pass to pandas.read_csv.
        """

        raw_data = self.get_responses(
            surveyId=surveyId, continuationToken=continuationToken
        )
        if raw_data is None:
            return None

        with zipfile.ZipFile(BytesIO(raw_data.data)) as data:
            with data.open(data.filelist[0]) as f:
                new_df: pd.DataFrame = pd.read_csv(f, skiprows=[1, 2], *args, **kwargs)
                new_df.set_index("ResponseId", inplace=True)
                new_df = new_df.replace(r"^\s*$", pd.NA, regex=True)
                new_df = new_df.astype(
                    {
                        col: "object"
                        for col in new_df.columns
                        if new_df[col].isna().all()
                    }
                )

                return ExportedFile(
                    fileId=raw_data.fileId,
                    continuationToken=raw_data.continuationToken,
                    data=new_df,
                )

    def get_survey_schema(self, surveyId: str) -> dict[str, Any] | None:
        """Get the schema of a survey by surveyId.

        Args:
            surveyId (str): The surveyId of the survey to get the schema from.
        """
        schema_url = self._make_api_url("{surveyId}", surveyId=surveyId)
        r = requests.get(schema_url, headers=HEADERS)

        if r.status_code != 200:
            return None
        else:
            return r.json() # type: ignore


# import numpy as np
# from sqlalchemy import (
#     Boolean,
#     Column,
#     DateTime,
#     Float,
#     Integer,
#     MetaData,
#     String,
#     Table,
#     Text,
# )


# def pd_dtype_to_sqlalchemy(dtype: np.dtype):
#     if np.issubdtype(dtype, np.integer):
#         return Integer
#     elif np.issubdtype(dtype, np.floating):
#         return Float
#     elif np.issubdtype(dtype, np.datetime64):
#         return DateTime
#     elif (
#         np.issubdtype(dtype, np.dtype("O"))
#         or np.issubdtype(dtype, np.dtype("S"))
#         or np.issubdtype(dtype, np.dtype("U"))
#     ):
#         return Text
#     elif np.issubdtype(dtype, np.bool_):
#         return Boolean
#     else:
#         raise ValueError(f"Unsupported dtype: {dtype}")


# def generate_mysql_schema(
#     df: pd.DataFrame,
#     table_name: str,
#     index_as_pk: bool = False,
#     auto_increment: bool = True,
# ):
#     metadata = MetaData()
#     columns = [
#         Column(name, pd_dtype_to_sqlalchemy(dtype)) for name, dtype in df.dtypes.items()
#     ]
#     columns = [
#         Column(name, pd_dtype_to_sqlalchemy(dtype), primary_key=index_as_pk)
#         for name, dtype in df.index.to_frame().dtypes.items()
#     ] + columns

#     if auto_increment:
#         columns.insert(0, Column("id", Integer, primary_key=True, autoincrement=True))

#     table = Table(table_name, metadata, *columns)
#     return table
