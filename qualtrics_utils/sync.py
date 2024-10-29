from __future__ import annotations

import pathlib
import uuid
from argparse import ArgumentParser
from enum import Enum
from typing import Any, Callable

import pandas as pd
import sqlalchemy
import tomllib
from googleapiutils2 import Sheets, SheetsValueRange, get_oauth2_creds  # type: ignore
from loguru import logger
from sqlalchemy import Column, DateTime, Integer, MetaData, Table, Text, func
from sqlalchemy.orm import declarative_base

from qualtrics_utils.codebook.generate import generate_codebook
from qualtrics_utils.misc import ExportedFile, T
from qualtrics_utils.survey import Surveys
from qualtrics_utils.utils import (
    coalesce_multiselect,
    create_mysql_engine,
    generate_sql_schema,
    parse_file_id,
    rename_columns,
)


class SyncType(Enum):
    SHEETS = "sheets"
    MYSQL = "mysql"


Base = declarative_base()


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


def format_name(survey_id: str, table_name: str | None, suffix: str):
    return table_name if table_name is not None else f"{survey_id}_{suffix}"


def format_status_name(survey_id: str, table_name: str | None):
    return format_name(survey_id=survey_id, table_name=table_name, suffix="status")


def format_responses_name(survey_id: str, table_name: str | None):
    return format_name(survey_id=survey_id, table_name=table_name, suffix="responses")


def format_status_row(exported_file: ExportedFile[T]):
    return dict(
        file_id=exported_file.file_id,
        timestamp=exported_file.timestamp.isoformat(),
        last_response_id=exported_file.last_response_id,
        continuation_token=exported_file.continuation_token,
    )


def setup_sql(
    responses_table_name: str | None,
    status_table_name: str | None,
    conn: sqlalchemy.Connection,
    restart: bool = False,
):
    def inner(exported_file: ExportedFile[pd.DataFrame]):
        survey_id = exported_file.survey_id
        df = exported_file.data

        metadata = MetaData()

        t_responses_table_name = format_responses_name(
            survey_id=survey_id, table_name=responses_table_name
        )
        t_status_table_name = format_status_name(
            survey_id=survey_id, table_name=status_table_name
        )

        responses_table = sqlalchemy.Table(t_responses_table_name, metadata)
        status_table = sqlalchemy.Table(t_status_table_name, metadata)

        if restart:
            responses_table.drop(conn, checkfirst=True)
            status_table.drop(conn, checkfirst=True)

        if not conn.dialect.has_table(conn, t_responses_table_name):
            responses_table = generate_sql_schema(
                df=df, table_name=t_responses_table_name, index_as_pk=True
            )
            responses_table.create(conn)

        if not conn.dialect.has_table(conn, t_status_table_name):
            status_table = get_status_table(table_name=t_status_table_name)
            status_table.create(conn)

        conn.commit()

    return inner


def get_last_status_sql(table_name: str | None, conn: sqlalchemy.Connection):
    def inner(survey_id: str):
        metadata = MetaData()

        status_table_name = format_status_name(
            survey_id=survey_id, table_name=table_name
        )

        status_table = Table(status_table_name, metadata, autoload_with=conn)

        query = status_table.select().order_by(status_table.c.id.desc()).limit(1)

        if (row := conn.execute(query).fetchone()) is not None:
            return row._asdict()

    return inner


def write_status_sql(
    table_name: str | None,
    conn: sqlalchemy.Connection,
):
    def inner(
        exported_file: ExportedFile[T],
    ):
        survey_id = exported_file.survey_id
        metadata = MetaData()

        status_table_name = format_status_name(
            survey_id=survey_id, table_name=table_name
        )
        status_table = Table(status_table_name, metadata, autoload_with=conn)

        conn.execute(
            status_table.insert().values(
                **format_status_row(exported_file),
            )
        )
        conn.commit()

    return inner


def write_responses_sql(
    table_name: str | None,
    conn: sqlalchemy.Connection,
):
    def inner(
        exported_file: ExportedFile[pd.DataFrame],
    ):
        survey_id = exported_file.survey_id
        df = exported_file.data

        metadata = MetaData()

        respones_table_name = format_responses_name(
            survey_id=survey_id, table_name=table_name
        )

        responses_table = Table(respones_table_name, metadata, autoload_with=conn)

        existing_columns = [col.name for col in responses_table.columns]
        df.drop(
            columns=[col for col in df.columns if col not in existing_columns],
            inplace=True,
        )

        df.to_sql(
            respones_table_name,
            conn,
            if_exists="append",
            index=True,
            index_label=df.index.name,
        )

        conn.commit()

    return inner


def setup_sheets(
    responses_sheet_name: str | None,
    status_sheet_name: str | None,
    sheet_url: str,
    sheets: Sheets,
    restart: bool = False,
):
    def inner(
        exported_file: ExportedFile[pd.DataFrame],
    ):
        survey_id = exported_file.survey_id

        t_responses_sheet_name = format_responses_name(
            survey_id=survey_id, table_name=responses_sheet_name
        )
        t_status_sheet_name = format_status_name(
            survey_id=survey_id, table_name=status_sheet_name
        )

        tmp_sheet_name = str(uuid.uuid4())

        if restart:
            sheets.add(sheet_url, names=tmp_sheet_name)

            sheets.delete(
                sheet_url,
                names=[t_responses_sheet_name, t_status_sheet_name],
                ignore_not_existing=True,
            )

        sheets.add(
            sheet_url,
            names=[t_responses_sheet_name, t_status_sheet_name],
            ignore_existing=True,
        )
        sheets.delete(sheet_url, names=tmp_sheet_name, ignore_not_existing=True)

    return inner


def get_last_status_sheets(
    sheet_name: str | None,
    sheet_url: str,
    sheets: Sheets,
):
    def inner(
        survey_id: str,
    ):
        status_sheet_name = format_status_name(
            survey_id=survey_id, table_name=sheet_name
        )

        status_sheet = SheetsValueRange(
            sheets=sheets, spreadsheet_id=sheet_url, sheet_name=status_sheet_name
        )

        last_status = status_sheet[..., ...].to_frame()
        if last_status is None or last_status.empty:
            return None

        return last_status.iloc[-1].to_dict()

    return inner


def write_status_sheets(
    sheet_name: str | None,
    sheet_url: str,
    sheets: Sheets,
):
    def inner(exported_file: ExportedFile[T]):
        survey_id = exported_file.survey_id
        status_sheet_name = format_status_name(
            survey_id=survey_id, table_name=sheet_name
        )

        row = format_status_row(exported_file)
        return sheets.append(
            spreadsheet_id=sheet_url,
            range_name=status_sheet_name,
            values=[row],
        )

    return inner


def write_responses_sheets(
    sheet_name: str | None,
    sheet_url: str,
    sheets: Sheets,
):
    def inner(exported_file: ExportedFile[pd.DataFrame]):
        df = exported_file.data
        survey_id = exported_file.survey_id

        responses_sheet_name = format_responses_name(
            survey_id=survey_id, table_name=sheet_name
        )

        values = sheets.from_frame(df.reset_index(drop=False), as_dict=True)

        if len(values) == 0:
            return

        sheets.append(
            spreadsheet_id=sheet_url,
            range_name=responses_sheet_name,
            values=values,
        )

    return inner


ResponsePostProcessingFunc = Callable[[pd.DataFrame], pd.DataFrame]

responses_post_processing_func_default: ResponsePostProcessingFunc = lambda x: x


def _sync(
    survey_id: str,
    surveys: Surveys,
    status_reader: Callable[[str], dict | None],
    status_writer: Callable[[ExportedFile[pd.DataFrame]], None],
    responses_writer: Callable[[ExportedFile[pd.DataFrame]], None],
    setup_func: Callable[[ExportedFile[pd.DataFrame]], None],
    responses_post_processing_func: ResponsePostProcessingFunc = responses_post_processing_func_default,
    **kwargs: Any,
):
    survey_id = parse_file_id(survey_id)
    logger.info(f"Syncing survey {survey_id}...")

    last_status = None
    try:
        last_status = status_reader(
            survey_id,
        )
    except Exception as e:
        logger.warning(f"Failed to read last status: {e}")

    last_response_id = (
        last_status["last_response_id"] if last_status is not None else None
    )
    # Only fallback to continuation token if last response ID is None.
    continuation_token = (
        last_status["continuation_token"]
        if last_status is not None and last_response_id is None
        else None
    )

    logger.info(
        f"Last response ID: {last_response_id} and continuation token: {continuation_token}"
    )

    exported_file = surveys.get_responses_df(
        survey_id=survey_id,
        last_response_id=last_response_id,
        continuation_token=continuation_token,
        **kwargs,
    )
    exported_file.data = responses_post_processing_func(exported_file.data)

    logger.info(f"Setting up tables...")
    setup_func(exported_file)

    logger.info(f"Writing responses...")
    responses_writer(exported_file)

    logger.info(f"Writing status...")
    status_writer(exported_file)


def sync_sql(
    survey_id: str,
    surveys: Surveys,
    conn: sqlalchemy.Connection,
    responses_table_name: str | None = None,
    status_table_name: str | None = None,
    restart: bool = False,
    response_post_processing_func: "ResponsePostProcessingFunc" = responses_post_processing_func_default,
    **kwargs: Any,
) -> None:
    survey_id = parse_file_id(survey_id)

    """
    Syncs survey responses and status from a given survey source to a SQL database.

    This requires two tables to be present in the target database:
        - A table to store the survey responses.
        - A table to store the last status of the survey.

    These will be automatically created if they do not exist:
        - If a table name is provided, the responses table will be named as such, and the status table will be named as {table_name}_status.
        - If a table name is not provided, the responses table will be named as {survey_id}_responses and the status table will be named as {survey_id}_status.

    The process is as thus:
        1. The last status of the survey is retrieved from the target.
            1a. If the survey has never been synced, the last status is None.
            1b. If the last status is found, then the last response ID and continuation token are retrieved.
        2. The survey responses are retrieved from the survey source, starting from the last response ID if possible, and the continuation token if possible.
        3. The retrieved survey responses are post-processed using the response_post_processing_func function.
        4. The post-processed survey responses are written to the target.
        5. The last status is written to the target.
    """
    _sync(
        survey_id=survey_id,
        surveys=surveys,
        status_reader=get_last_status_sql(table_name=status_table_name, conn=conn),
        status_writer=write_status_sql(table_name=status_table_name, conn=conn),
        responses_writer=write_responses_sql(
            table_name=responses_table_name, conn=conn
        ),
        setup_func=setup_sql(
            responses_table_name=responses_table_name,
            status_table_name=status_table_name,
            conn=conn,
            restart=restart,
        ),
        responses_post_processing_func=response_post_processing_func,
        **kwargs,
    )


def sync_sheets(
    survey_id: str,
    surveys: Surveys,
    sheets: Sheets,
    sheet_url: str,
    responses_sheet_name: str | None = None,
    status_sheet_name: str | None = None,
    restart: bool = False,
    response_post_processing_func: "ResponsePostProcessingFunc" = responses_post_processing_func_default,
    **kwargs: Any,
) -> None:
    """Syncs survey responses and status from a given survey source to a Google Sheet.

    This requires two tables to be present in the target database:
        - A table to store the survey responses.
        - A table to store the last status of the survey.

    These will be automatically created if they do not exist:
        - If a table name is provided, the responses table will be named as such, and the status table will be named as {table_name}_status.
        - If a table name is not provided, the responses table will be named as {survey_id}_responses and the status table will be named as {survey_id}_status.

    The process is as thus:
        1. The last status of the survey is retrieved from the target.
            1a. If the survey has never been synced, the last status is None.
            1b. If the last status is found, then the last response ID and continuation token are retrieved.
        2. The survey responses are retrieved from the survey source, starting from the last response ID if possible, and the continuation token if possible.
        3. The retrieved survey responses are post-processed using the response_post_processing_func function.
        4. The post-processed survey responses are written to the target.
        5. The last status is written to the target."""
    _sync(
        survey_id=survey_id,
        surveys=surveys,
        status_reader=get_last_status_sheets(
            sheet_name=status_sheet_name, sheet_url=sheet_url, sheets=sheets
        ),
        status_writer=write_status_sheets(
            sheet_name=status_sheet_name, sheet_url=sheet_url, sheets=sheets
        ),
        responses_writer=write_responses_sheets(
            sheet_name=responses_sheet_name, sheet_url=sheet_url, sheets=sheets
        ),
        setup_func=setup_sheets(
            responses_sheet_name=responses_sheet_name,
            status_sheet_name=status_sheet_name,
            sheet_url=sheet_url,
            sheets=sheets,
            restart=restart,
        ),
        responses_post_processing_func=response_post_processing_func,
        **kwargs,
    )


def sync(
    config: dict[str, Any],
    type: SyncType,
    responses_table_name: str | None,
    status_table_name: str | None,
    verbose: bool,
    restart: bool,
):
    qualtrics_config = config["qualtrics"]

    if "api_token" not in qualtrics_config:
        raise ValueError("API token is not provided in the config file.")

    qualtrics_api_token = qualtrics_config["api_token"]
    codebook_path = (
        pathlib.Path(qualtrics_config["codebook_path"])
        if "codebook_path" in qualtrics_config
        else None
    )

    surveys = Surveys(api_token=qualtrics_api_token)

    if "survey_id" not in qualtrics_config:
        raise ValueError("Survey ID is not provided in the config file.")

    survey_id = qualtrics_config["survey_id"]

    survey_args = (
        qualtrics_config["survey_args"] if "survey_args" in qualtrics_config else {}
    )

    logger.info(f"Type: {type}")
    logger.info(f"Restart: {restart}")
    logger.info(f"Responses table name: {responses_table_name}")
    logger.info(f"Status table name: {status_table_name}")
    logger.info(f"Verbose: {verbose}")

    def post_processing_func(df: pd.DataFrame):
        if codebook_path is None:
            return df

        codebook = generate_codebook(codebook_path)
        tmp = coalesce_multiselect(df, codebook=codebook)
        tmp = rename_columns(tmp, codebook=codebook, verbose=verbose)

        return tmp

    if type == SyncType.SHEETS:
        responses_url = config["google"]["urls"]["responses"]

        creds = get_oauth2_creds(config["google"]["credentials_path"])
        sheets = Sheets(creds=creds)

        sync_sheets(
            survey_id=survey_id,
            surveys=surveys,
            response_post_processing_func=post_processing_func,
            responses_sheet_name=responses_table_name,
            status_sheet_name=status_table_name,
            sheet_url=responses_url,
            sheets=sheets,
            restart=restart,
            **survey_args,
        )
    elif type == SyncType.MYSQL:
        engine = create_mysql_engine(
            **config["mysql"],
        )

        with engine.connect() as conn:
            sync_sql(
                survey_id=survey_id,
                surveys=surveys,
                response_post_processing_func=post_processing_func,
                conn=conn,
                responses_table_name=responses_table_name,
                status_table_name=status_table_name,
                restart=restart,
                **survey_args,
            )


def main():
    parser = ArgumentParser(
        description="""Sync Qualtrics survey responses to a target."""
    )
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        required=False,
        default=pathlib.Path("auth/config.toml"),
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--restart", action="store_true")
    parser.add_argument("--responses-table-name", required=False)
    parser.add_argument("--status-table-name", required=False)
    parser.add_argument(
        "--type",
        choices=[t for t in SyncType.__members__.values()],
        required=True,
        type=SyncType,
    )
    args = parser.parse_args()

    config = tomllib.loads(args.config.read_text())

    sync(
        config=config,
        type=args.type,
        responses_table_name=args.responses_table_name,
        status_table_name=args.status_table_name,
        verbose=args.verbose,
        restart=args.restart,
    )


if __name__ == "__main__":
    main()
