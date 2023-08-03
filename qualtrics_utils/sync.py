from typing import Callable

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
    Base = declarative_base()

    class SurveyStatus(Base):  # type: ignore
        __tablename__ = table_name

        id = Column(Integer, primary_key=True, autoincrement=True)
        timestamp = Column(DateTime, server_default=func.now())
        continuationToken = Column(Text)
        fileId = Column(Text)

    return SurveyStatus()


format_status_name = lambda surveyId: f"{surveyId}_status"


def format_status_row(exported_file: ExportedFile[T]):
    return dict(
        continuationToken=exported_file.continuationToken, fileId=exported_file.fileId
    )


def write_status_sql(
    exported_file: ExportedFile[T],
    conn: sqlalchemy.Connection,
    create_table: bool = True,
):
    """Create a table to store the status of a survey's responses.

    Args:
        exported_file (ExportedFile[T]): The responses to create a status table for.
        conn (sqlalchemy.Connection): The connection to the MySQL database.
    """
    table_name = format_status_name(exported_file.surveyId)

    if create_table and not conn.dialect.has_table(conn, table_name):
        table = get_status_table(exported_file.surveyId)
        table.create(conn)

    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=conn)

    conn.execute(
        table.insert().values(
            **format_status_row(exported_file),
        )
    )


def get_last_continuation_token_sql(
    survey_id: str, conn: sqlalchemy.Connection
) -> str | None:
    table_name = format_status_name(survey_id)

    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=conn)

    query = table.select().order_by(table.c.id.desc()).limit(1)

    result = conn.execute(query).fetchone()
    if result is None:
        return None

    return result["continuationToken"]  # type: ignore


def write_responses_sql(
    exported_file: ExportedFile[pd.DataFrame],
    table_name: str,
    conn: sqlalchemy.Connection,
    create_table: bool = True,
):
    """Sync a survey's responses to a MySQL database.

    Args:
        exported_file (ExportedFile[pd.DataFrame]): The responses to sync.
        table_name (str): The name of the table to sync the responses to.
        conn (sqlalchemy.Connection): The connection to the MySQL database.
        create_table (bool, optional): Whether to create the table if it does not exist. Defaults to True.
    """
    if create_table and not conn.dialect.has_table(conn, table_name):
        schema = generate_sql_schema(exported_file.data, table_name)
        schema.create(conn)

    responses_df = exported_file.data

    responses_df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=True,
        index_label="ResponseId",
    )


def sync_responses_sql(
    survey_id: str,
    table_name: str,
    surveys: Surveys,
    conn: sqlalchemy.Connection,
    create_table: bool = True,
    post_processing_func: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
    *args,
    **kwargs,
):
    continuationToken = get_last_continuation_token_sql(survey_id=survey_id, conn=conn)

    exported_file = surveys.get_responses_df(
        surveyId=survey_id, continuationToken=continuationToken, *args, **kwargs
    )

    if exported_file is None:
        return

    exported_file.data = post_processing_func(exported_file.data)

    write_responses_sql(
        exported_file=exported_file,
        table_name=table_name,
        conn=conn,
        create_table=create_table,
    )

    write_status_sql(
        exported_file=exported_file,
        conn=conn,
        create_table=create_table,
    )


def get_last_continuation_token_sheets(
    survey_id: str, sheet_url: str, sheets: Sheets
) -> str | None:
    sheet_name = format_status_name(survey_id)

    sheets.add(sheet_url, names=sheet_name)

    sheet = SheetsValueRange(
        sheets=sheets, spreadsheet_id=sheet_url, sheet_name=sheet_name
    )

    last_status = sheet[-1, ...].to_frame()
    if last_status is None:
        return None

    return last_status.iloc[0]["continuationToken"]


def write_status_sheets(
    exported_file: ExportedFile[T],
    sheet_url: str,
    sheets: Sheets,
):
    sheet_name = format_status_name(exported_file.surveyId)

    row = format_status_row(exported_file)
    return sheets.append(
        spreadsheet_id=sheet_url,
        range_name=sheet_name,
        values=[row],
    )


def write_responses_sheets(
    exported_file: ExportedFile[pd.DataFrame],
    sheet_name: str,
    sheet_url: str,
    sheets: Sheets,
):
    responses_df = exported_file.data

    values = sheets.from_frame(responses_df.reset_index(drop=False), as_dict=True)

    if len(values) == 0:
        return

    sheets.append(
        spreadsheet_id=sheet_url,
        range_name=sheet_name,
        values=values,
    )

    sheets.resize_columns(
        spreadsheet_id=sheet_url,
        sheet_name=sheet_name,
        width=None,
    )


def sync_responses_sheets(
    survey_id: str,
    sheet_name: str,
    sheet_url: str,
    surveys: Surveys,
    sheets: Sheets,
    post_processing_func: Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
    *args,
    **kwargs,
):
    continuationToken = get_last_continuation_token_sheets(
        survey_id=survey_id, sheet_url=sheet_url, sheets=sheets
    )

    exported_file = surveys.get_responses_df(
        surveyId=survey_id, continuationToken=continuationToken, *args, **kwargs
    )

    if exported_file is None:
        return

    exported_file.data = post_processing_func(exported_file.data)

    write_responses_sheets(
        exported_file=exported_file,
        sheet_name=sheet_name,
        sheet_url=sheet_url,
        sheets=sheets,
    )

    write_status_sheets(
        exported_file=exported_file,
        sheet_url=sheet_url,
        sheets=sheets,
    )
