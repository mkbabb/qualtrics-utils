from __future__ import annotations

import re
import urllib.parse
from functools import cache
from typing import *

import pandas as pd
import sqlalchemy
from attr import asdict
from googleapiutils2 import Sheets
from loguru import logger

from qualtrics_utils.misc import T
from qualtrics_utils.surveys_response_import_export_api_client.types import UNSET

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


def get_url_params(url: str) -> dict[str, List[str]]:
    """Get the components of the given URL."""
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)


def get_id_from_url(
    url: str, adjacent_options: list[str], query_param_options: list[str]
) -> str:
    """
    Extracts the ID from the URL provided.

    This function supports URLs of the form:
    - '.../x/{id}/...' for x in adjacent_options
    - With a query parameter named 'x': '...?x={x}...' for x in query_param_options

    We prioritize the adjacent_options over the query_param_options, and short circuit therein if we find a match.

    Args:
        url (str): The URL string from which to extract the ID.
    """
    url_obj = urllib.parse.urlparse(url)
    path = url_obj.path
    paths = path.split("/")

    get_adjacent = (
        lambda x: paths[t_ix]
        if x in paths and (t_ix := paths.index(x) + 1) < len(paths)
        else None
    )

    for i in adjacent_options:
        if (id := get_adjacent(i)) is not None:
            return id

    params = get_url_params(url)
    for i in query_param_options:
        if (ids := params.get(i)) is not None:
            return ids[0]

    raise ValueError(f"Could not parse file URL of {url}")


ADJACENT_OPTIONS = ["form", "survey-builder"]
QUERY_PARAM_OPTIONS = ["surveyId", "id"]


@cache
def parse_file_id(
    file_id: str,
    adjacent_options: list[str] = ADJACENT_OPTIONS,
    query_param_options: list[str] = QUERY_PARAM_OPTIONS,
) -> str:
    """
    Parse the given file_id which could be an ID string, URL string or a dictionary object.

    This function supports the following formats:
    - Direct ID string: '123456789'
    - URL formats supported by 'get_id_from_url' function.
    - Dictionary object with 'id' or 'surveyId' as keys.

    Args:
        file_id (str): The ID string or URL or dictionary from which to extract the ID.
    """

    def parse(file_id: str) -> str:
        if "http" in file_id:
            return get_id_from_url(
                file_id,
                adjacent_options=adjacent_options,
                query_param_options=query_param_options,
            )
        else:
            return file_id

    def obj_to_id(file: str) -> str:
        if isinstance(file, str):
            return file
        elif isinstance(file, dict):
            for i in query_param_options:
                if (id := file.get(i)) is not None:
                    return id

        return None

    if (id := obj_to_id(file_id)) is not None:
        return parse(id)
    else:
        return file_id


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
    """Coalesce a multi-select column into a single column.

    For example, if we have a multi-select question with the following options:
        - Option 1
        - Option 2
        - Option 3

    These will be typically split into individual columns, with each cell potentially being a non-null value.
    In many case, a multi-select question will have one response, and the rest will be null.

    This function will coalesce all the non-null values into a single column.
    If multiple values are present, then the values will be handled as follows:
        - If use_multiple is True, then the value will be set to "Multiple"
        - If use_multiple is False, then then value will be the concatenation of the values, separated by the `delimiter`.

    Args:
        - df (pd.DataFrame): The DataFrame to coalesce.
        - codebook (list[dict[str, Any]]): The codebook for the survey.
        - delimiter (str): The delimiter to use when joining multiple values.
        - use_multiple (bool): Whether to use the "Multiple" string when multiple values are present.
    """

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


def delete_sheet_if_exists(sheet_name: str, spreadsheet_id: str, sheets: Sheets):
    try:
        if sheets.has(name=sheet_name, spreadsheet_id=spreadsheet_id):
            sheets.delete(name=sheet_name, spreadsheet_id=spreadsheet_id)
    except Exception as e:
        logger.error(f"Error deleting sheet {sheet_name} from {spreadsheet_id}: {e}")
        pass

    return
