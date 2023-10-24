from __future__ import annotations

import re
from typing import *

import pandas as pd
import sqlalchemy
from attr import asdict

from qualtrics_utils.misc import T
from qualtrics_utils.surveys_response_import_export_api_client.types import UNSET

from googleapiutils2 import Sheets

RE_HTML_TAG = re.compile(r"<(.|\s)*?>")

RE_SPACE = re.compile(r"&nbsp;")

RE_WHITESPACE = re.compile("\s+")


def normalize_whitespace(s: str) -> str:
    s = re.sub(RE_WHITESPACE, " ", s)
    return s.strip()


def normalize_html_string(s: str) -> str:
    s = re.sub(RE_HTML_TAG, "", s)
    s = re.sub(RE_SPACE, " ", s)
    s = normalize_whitespace(s)
    return s


def quote_value(value: str, quote: str = "`") -> str:
    if re.match(re.compile(quote + "(.*)" + quote), value) is not None:
        return value
    else:
        return f"{quote}{value}{quote}"


def reset_request_defaults(request: T, set_items: dict[str, Any]) -> T:
    """Set all attributes of d to UNSET except for those in set_items
    This is useful for when you want all defaults to be UNSET, but you want to set some attributes to a value.

    Args:
        request (Any): Input request object from an OpenAPI client.
        set_items (dict[str, Any]): Dictionary of attributes that were explicitly set.
    """
    # request must have a to_dict() and from_dict() method
    if not hasattr(request, "to_dict") or not hasattr(request, "from_dict"):
        raise ValueError("request must have a to_dict() and from_dict() method")

    for k, v in asdict(request).items():  # type: ignore
        if k not in set_items and not isinstance(v, dict):
            setattr(request, k, UNSET)

    return request


def rename_columns(
    df: pd.DataFrame, codebook: list[dict[str, Any]], verbose: bool = True
) -> pd.DataFrame:
    renaming_map = {}
    for question in codebook:
        root_q_num = question["question_number"]
        sub_questions = question.get("questions")

        if root_q_num in df.columns:
            if verbose:
                renaming_map[
                    root_q_num
                ] = f"{root_q_num} - {question['question_string']}"
            else:
                renaming_map[root_q_num] = f"{root_q_num}"

        if sub_questions is not None and len(sub_questions) >= 1:
            for sub_question in sub_questions:
                q_num = sub_question["question_number"]
                if not q_num in df.columns:
                    continue

                if verbose:
                    renaming_map[
                        q_num
                    ] = f"{root_q_num} - {sub_question['question_string']}"
                else:
                    renaming_map[q_num] = f"{sub_question['question_number']}"

    df.rename(columns=renaming_map, inplace=True, errors="ignore")
    return df


def coalesce_multiselect(
    df: pd.DataFrame,
    codebook: list[dict[str, Any]],
    delimiter: str = ", ",
    use_multiple: bool = True,
) -> pd.DataFrame:
    def join(x: pd.Series) -> str:
        l = x.dropna().tolist()

        if use_multiple and len(l) > 1:
            return "Multiple"
        else:
            return delimiter.join(l)

    root_questions = {}

    for question in codebook:
        if question["question_type"] == "MC":
            root_q_num = question["question_number"]
            sub_questions = question.get("questions")

            if sub_questions is None or len(sub_questions) <= 1:
                continue

            sub_question_numbers = [
                sub_question["question_number"] for sub_question in sub_questions
            ]
            sub_question_columns = [
                col for col in df.columns if col in sub_question_numbers
            ]
            root_questions[root_q_num] = df[sub_question_columns].apply(
                lambda x: join(x), axis=1
            )
            df.drop(columns=sub_question_columns, inplace=True)

    for root_q_num, root_question_df in root_questions.items():
        df[root_q_num] = root_question_df

    return df


def create_mysql_engine(
    username: str, password: str, host: str, port: str, database: str, **kwargs: Any
) -> sqlalchemy.engine.Engine:
    engine_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    engine = sqlalchemy.create_engine(engine_str)
    return engine


def drop_if_exists(table_name: str, conn: sqlalchemy.Connection):
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(table_name, metadata)

    if conn.dialect.has_table(conn, table_name):
        table.drop(conn)


def delete_sheet_if_exists(sheet_name: str, sheets: Sheets):
    if sheets.has(name=sheet_name):
        sheets.delete(name=sheet_name)
