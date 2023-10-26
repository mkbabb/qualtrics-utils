from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd
import sqlalchemy
from googleapiutils2 import Sheets, SheetsValueRange
from loguru import logger
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base

from qualtrics_utils.misc import ExportedFile, T
from qualtrics_utils.survey import Surveys
from qualtrics_utils.utils import (
    create_mysql_engine,
    delete_sheet_if_exists,
    drop_if_exists,
    parse_file_id,
)

Base = declarative_base()


def pd_dkindto_sqlalchemy(dtype: np.dtype):
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
    """Generate a SQLAlchemy table schema from a Pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame from which to generate the schema.
        table_name (str): The name of the table.
        index_as_pk (bool, optional): Whether to use the index as the primary key. Defaults to False.
        auto_increment (bool, optional): Whether to use autoincrement for the primary key. Defaults to True.
    """
    metadata = MetaData()
    columns: list[Column] = [
        Column(name, pd_dkindto_sqlalchemy(dtype)) for name, dtype in df.dtypes.items()
    ]
    columns = [
        Column(name, pd_dkindto_sqlalchemy(dtype), primary_key=index_as_pk)
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


def format_status_name(survey_id: str, table_name: str | None):
    t_table_name = table_name if table_name is not None else survey_id
    return f"{t_table_name}_status"


def format_responses_name(survey_id: str, table_name: str | None):
    return table_name if table_name is not None else f"{survey_id}_responses"


def format_status_row(exported_file: ExportedFile[T]):
    return dict(
        file_id=exported_file.file_id,
        timestamp=exported_file.timestamp.isoformat(),
        last_response_id=exported_file.last_response_id,
        continuation_token=exported_file.continuation_token,
    )


def setup_sql(
    table_name: str | None, conn: sqlalchemy.Connection, restart: bool = False
):
    def inner(exported_file: ExportedFile[pd.DataFrame]):
        survey_id = exported_file.survey_id
        df = exported_file.data

        responses_table_name = format_responses_name(
            survey_id=survey_id, table_name=table_name
        )
        status_table_name = format_status_name(
            survey_id=survey_id, table_name=table_name
        )

        if restart:
            drop_if_exists(table_name=responses_table_name, conn=conn)
            drop_if_exists(table_name=status_table_name, conn=conn)

        responses_table = generate_sql_schema(
            df=df, table_name=responses_table_name, index_as_pk=True
        )
        responses_table.create(conn)

        status_table = get_status_table(table_name=status_table_name)
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
        df = exported_file.data

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=True,
            index_label=df.index.name,
        )
        conn.commit()

    return inner


def setup_sheets(
    sheet_name: str | None,
    sheet_url: str,
    sheets: Sheets,
    restart: bool = False,
):
    def inner(
        exported_file: ExportedFile[pd.DataFrame],
    ):
        survey_id = exported_file.survey_id

        responses_sheet_name = format_responses_name(
            survey_id=survey_id, table_name=sheet_name
        )
        status_sheet_name = format_status_name(
            survey_id=survey_id, table_name=sheet_name
        )

        if restart:
            delete_sheet_if_exists(
                sheet_name=responses_sheet_name, spreadsheet_id=sheet_url, sheets=sheets
            )
            delete_sheet_if_exists(
                sheet_name=status_sheet_name, spreadsheet_id=sheet_url, sheets=sheets
            )

        sheets.add(sheet_url, names=[responses_sheet_name, status_sheet_name])

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
    status_writer: Callable[[ExportedFile[T]], None],
    responses_writer: Callable[[ExportedFile[pd.DataFrame]], None],
    setup_func: Callable[[ExportedFile[pd.DataFrame]], None],
    responses_post_processing_func: ResponsePostProcessingFunc = responses_post_processing_func_default,
    **kwargs: Any,
):
    survey_id = parse_file_id(survey_id)

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
    exported_file = surveys.get_responses_df(
        survey_id=survey_id,
        last_response_id=last_response_id,
        continuation_token=continuation_token,
        **kwargs,
    )
    exported_file.data = responses_post_processing_func(exported_file.data)

    setup_func(exported_file)

    responses_writer(exported_file)

    status_writer(exported_file)


def sync_sql(
    survey_id: str,
    surveys: Surveys,
    conn: sqlalchemy.Connection,
    table_name: str | None = None,
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
        status_reader=get_last_status_sql(table_name=table_name, conn=conn),
        status_writer=write_status_sql(table_name=table_name, conn=conn),
        responses_writer=write_responses_sql(table_name=table_name, conn=conn),
        setup_func=setup_sql(table_name=table_name, conn=conn, restart=restart),
        responses_post_processing_func=response_post_processing_func,
        **kwargs,
    )


def sync_sheets(
    survey_id: str,
    surveys: Surveys,
    sheets: Sheets,
    sheet_url: str,
    sheet_name: str | None = None,
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
            sheet_name=sheet_name, sheet_url=sheet_url, sheets=sheets
        ),
        status_writer=write_status_sheets(
            sheet_name=sheet_name, sheet_url=sheet_url, sheets=sheets
        ),
        responses_writer=write_responses_sheets(
            sheet_name=sheet_name, sheet_url=sheet_url, sheets=sheets
        ),
        setup_func=setup_sheets(
            sheet_name=sheet_name, sheet_url=sheet_url, sheets=sheets, restart=restart
        ),
        responses_post_processing_func=response_post_processing_func,
        **kwargs,
    )


def main():
    import pathlib
    import tomllib
    from argparse import ArgumentParser

    from googleapiutils2 import Sheets, get_oauth2_creds

    from qualtrics_utils import (
        Surveys,
        coalesce_multiselect,
        create_mysql_engine,
        generate_codebook,
        rename_columns,
    )

    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        required=False,
        default=pathlib.Path("auth/config.toml"),
        help="Path to the config file. See the config.example.toml for more information.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Synced column names will be the verbose names from the codebook (if provided)",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Restart the sync from the beginning of the survey.",
    )
    parser.add_argument(
        "--table-name",
        required=False,
        help="Base table name for the survey. If not provided, the survey ID will be used.",
    )
    parser.add_argument(
        "--kind",
        choices=["sheets", "sql"],
        required=True,
        help="The kind of sync to perform. Either 'sheets' or 'sql' (mysql only for now).",
    )

    args = parser.parse_args()

    config = tomllib.loads(args.config.read_text())

    qualtrics_api_token = config["qualtrics"]["api_token"]
    codebook_path = pathlib.Path(config["qualtrics"]["codebook_path"])

    surveys = Surveys(api_token=qualtrics_api_token)

    survey_id = config["qualtrics"]["survey_id"]

    kind = args.kind
    table_name = args.table_name
    verbose = args.verbose
    restart = args.restart

    survey_args = config["qualtrics"]["survey_args"]
    for k, v in survey_args.items():
        if isinstance(v, str) and "date" in k.lower():
            survey_args[k] = pd.to_datetime(v)

    def post_processing_func(df: pd.DataFrame):
        codebook = generate_codebook(codebook_path)
        tmp = coalesce_multiselect(df, codebook=codebook)
        tmp = rename_columns(tmp, codebook=codebook, verbose=verbose)

        return tmp

    if kind == "sheets":
        responses_url = config["google"]["urls"]["responses"]

        creds = get_oauth2_creds(config["google"]["credentials_path"])
        sheets = Sheets(creds=creds)

        sync_sheets(
            survey_id=survey_id,
            surveys=surveys,
            response_post_processing_func=post_processing_func,
            sheet_name=table_name,
            sheet_url=responses_url,
            sheets=sheets,
            restart=restart,
            **survey_args,
        )
    elif kind == "sql":
        engine = create_mysql_engine(
            **config["mysql"],
        )
        with engine.connect() as conn:
            sync_sql(
                survey_id=survey_id,
                surveys=surveys,
                response_post_processing_func=post_processing_func,
                conn=conn,
                table_name=table_name,
                restart=restart,
                **survey_args,
            )


if __name__ == "__main__":
    main()
