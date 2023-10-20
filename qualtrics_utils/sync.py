from enum import Enum
from typing import Any, Callable

import numpy as np
import pandas as pd
import sqlalchemy
from googleapiutils2 import Sheets, SheetsValueRange
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base

from qualtrics_utils.misc import ExportedFile, T
from qualtrics_utils.survey import Surveys

Base = declarative_base()


class SyncType(Enum):
    SQL = "sql"
    SHEETS = "sheets"


def pd_dtype_to_sqlalchemy(dtype: np.dtype):
    if np.issubdtype(dtype, np.integer):
        return Integer
    elif np.issubdtype(dtype, np.floating):
        return Float
    elif np.issubdtype(dtype, np.datetime64):
        return DateTime
    elif (
        np.issubdtype(dtype, np.dtype("O"))
        or np.issubdtype(dtype, np.dtype("S"))
        or np.issubdtype(dtype, np.dtype("U"))
    ):
        return Text
    elif np.issubdtype(dtype, np.bool_):
        return Boolean
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")


def generate_sql_schema(
    df: pd.DataFrame,
    table_name: str,
    index_as_pk: bool = False,
    auto_increment: bool = True,
):
    metadata = MetaData()
    columns: list[Column] = [
        Column(name, pd_dtype_to_sqlalchemy(dtype)) for name, dtype in df.dtypes.items()
    ]
    columns = [
        Column(name, pd_dtype_to_sqlalchemy(dtype), primary_key=index_as_pk)
        for name, dtype in df.index.to_frame().dtypes.items()
    ] + columns

    if auto_increment:
        columns.insert(0, Column("id", Integer, primary_key=True, autoincrement=True))

    table = Table(table_name, metadata, *columns)
    return table


def get_status_table(table_name: str):
    return Table(
        table_name,
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("timestamp", DateTime, server_default=func.now()),
        Column("last_response_id", Text),
        Column("continuation_token", Text),
        Column("file_id", Text),
    )


format_status_name = lambda survey_id: f"{survey_id}_status"


def format_status_row(exported_file: ExportedFile[T]):
    return dict(
        file_id=exported_file.file_id,
        timestamp=exported_file.timestamp.isoformat(),
        last_response_id=exported_file.last_response_id,
        continuation_token=exported_file.continuation_token,
    )


def write_status_sql(
    conn: sqlalchemy.Connection,
):
    def inner(
        exported_file: ExportedFile[T],
    ):
        table_name = format_status_name(exported_file.survey_id)

        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=conn)

        conn.execute(
            table.insert().values(
                **format_status_row(exported_file),
            )
        )
        conn.commit()

    return inner


def get_last_status_sql(conn: sqlalchemy.Connection):
    def inner(survey_id: str):
        table_name = format_status_name(survey_id)

        table = None
        if not conn.dialect.has_table(conn, table_name):
            table = get_status_table(table_name=table_name)
            table.create(conn)
        else:
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=conn)

        query = table.select().order_by(table.c.id.desc()).limit(1)

        if (row := conn.execute(query).fetchone()) is not None:
            return row._asdict()

    return inner


def write_responses_sql(
    table_name: str,
    conn: sqlalchemy.Connection,
):
    def inner(
        exported_file: ExportedFile[pd.DataFrame],
    ):
        if not conn.dialect.has_table(conn, table_name):
            table = generate_sql_schema(exported_file.data, table_name)
            table.create(conn)

        responses_df = exported_file.data
        responses_df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=True,
            index_label="ResponseId",
        )
        conn.commit()

    return inner


def get_last_status_sheets(sheet_url: str, sheets: Sheets):
    def inner(
        survey_id: str,
    ):
        sheet_name = format_status_name(survey_id)

        sheets.add(sheet_url, names=sheet_name)

        sheet = SheetsValueRange(
            sheets=sheets, spreadsheet_id=sheet_url, sheet_name=sheet_name
        )

        last_status = sheet[..., ...].to_frame()
        if last_status is None or last_status.empty:
            return None

        return last_status.iloc[-1].to_dict()

    return inner


def write_status_sheets(
    sheet_url: str,
    sheets: Sheets,
):
    def inner(exported_file: ExportedFile[T]):
        sheet_name = format_status_name(exported_file.survey_id)

        row = format_status_row(exported_file)
        return sheets.append(
            spreadsheet_id=sheet_url,
            range_name=sheet_name,
            values=[row],
        )

    return inner


def write_responses_sheets(
    sheet_name: str,
    sheet_url: str,
    sheets: Sheets,
):
    def inner(exported_file: ExportedFile[pd.DataFrame]):
        responses_df = exported_file.data

        values = sheets.from_frame(responses_df.reset_index(drop=False), as_dict=True)

        if len(values) == 0:
            return

        sheets.append(
            spreadsheet_id=sheet_url,
            range_name=sheet_name,
            values=values,
        )

    return inner


ResponsePostProcessingFunc = Callable[[pd.DataFrame], pd.DataFrame]

responses_post_processing_func_default: ResponsePostProcessingFunc = lambda x: x


def sync_internal(
    survey_id: str,
    surveys: Surveys,
    status_reader: Callable[[str], dict | None],
    status_writer: Callable[[ExportedFile[T]], None],
    responses_writer: Callable[[ExportedFile[pd.DataFrame]], None],
    responses_post_processing_func: ResponsePostProcessingFunc = responses_post_processing_func_default,
    *args: Any,
    **kwargs: Any,
):
    last_status = status_reader(
        survey_id,
    )
    last_response_id = (
        last_status["last_response_id"] if last_status is not None else None
    )
    # Only fallback to continuation token if last response ID is None.
    continuation_token = (
        last_status["continuation_token"]
        if last_status is not None and last_response_id is None
        else None
    )
    exported_file = surveys.get_responses_df(
        survey_id=survey_id,
        last_response_id=last_response_id,
        continuation_token=continuation_token,
        *args,
        **kwargs,
    )  # type: ignore
    exported_file.data = responses_post_processing_func(exported_file.data)

    responses_writer(exported_file)

    status_writer(exported_file)


def sync(
    survey_id: str,
    surveys: Surveys,
    sync_type: SyncType = SyncType.SQL,
    response_post_processing_func: ResponsePostProcessingFunc = responses_post_processing_func_default,
    *args: Any,
    **kwargs: Any,
):
    """Synchronizes survey responses and status from a given survey source to a target, which can be either a SQL database or Google Sheets.

    If the target is a SQL database, the following keyword arguments are required:
        - conn (sqlalchemy.Connection): A connection to the target database.
        - table_name (str): The name of the table where the survey responses will be stored.

    If the target is Google Sheets, the following keyword arguments are required:
        - sheets (Sheets): An instance of the Sheets class for Google Sheets interaction.
        - sheet_url (str): The URL of the spreadsheet where the survey responses will be stored.
        - sheet_name (str): The name of the sheet where the survey responses will be stored.

    For every target, the syncing process takes places as thus:
        1. The last status of the survey is retrieved from the target.
            1a. If the survey has never been synced, the last status is None.
            1b. If the last status is found, then the last response ID and continuation token are retrieved.
        2. The survey responses are retrieved from the survey source, starting from the last response ID if possible, and the continuation token if possible.
        3. The retrieved survey responses are post-processed using the response_post_processing_func function.
        4. The post-processed survey responses are written to the target.
        5. The last status is written to the target.

    This requires that the target has two "tables", one for the survey responses and one for the survey status.

    Args:
        - survey_id (str): The ID of the survey to be synchronized.
        - surveys (Surveys): An instance of the Surveys class for survey data interaction.
        - sync_type (SyncType, optional): The type of the target where the data will be synchronized. Defaults to SyncType.SQL.
        - response_post_processing_func (Callable, optional): A function to post-process the retrieved survey responses. Defaults to a no-op.
        - *args (Any): Additional positional arguments for internal methods.
        - **kwargs (Any): Additional keyword arguments for internal methods.
    """
    if sync_type == SyncType.SQL:
        conn, table_name = kwargs.pop("conn"), kwargs.pop("table_name")

        sync_internal(
            survey_id=survey_id,
            surveys=surveys,
            status_reader=get_last_status_sql(
                conn=conn,
            ),
            status_writer=write_status_sql(
                conn=conn,
            ),
            responses_writer=write_responses_sql(
                table_name=table_name,
                conn=conn,
            ),
            responses_post_processing_func=response_post_processing_func,
            *args,
            **kwargs,
        )  # type: ignore

    elif sync_type == SyncType.SHEETS:
        sheets, sheet_url, sheet_name = (
            kwargs.pop("sheets"),
            kwargs.pop("sheet_url"),
            kwargs.pop("sheet_name"),
        )
        sync_internal(
            survey_id=survey_id,
            surveys=surveys,
            status_reader=get_last_status_sheets(
                sheet_url=sheet_url,
                sheets=sheets,
            ),
            status_writer=write_status_sheets(
                sheet_url=sheet_url,
                sheets=sheets,
            ),
            responses_writer=write_responses_sheets(
                sheet_name=sheet_name,
                sheet_url=sheet_url,
                sheets=sheets,
            ),
            responses_post_processing_func=response_post_processing_func,
            *args,
            **kwargs,
        )  # type: ignore
