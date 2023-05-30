import re
from typing import *

import pandas as pd


def normalize_whitespace(s: str) -> str:
    RE_WHITESPACE = re.compile("\s+")
    s = re.sub(RE_WHITESPACE, " ", s)
    return s.strip()


def quote_value(value: str, quote: str = "`") -> str:
    if re.match(re.compile(quote + "(.*)" + quote), value) is not None:
        return value
    else:
        return f"{quote}{value}{quote}"


def coalesce_multiselect(
    df: pd.DataFrame, codebook: list[dict[str, Any]], delimiter: str = ","
) -> pd.DataFrame:
    for question in codebook:
        if question["question_type"] == "MC":
            root_question = question["question_number"]
            sub_questions = question.get("questions", [])
            if len(sub_questions) <= 1:
                continue

            sub_question_numbers = [
                sub_question["question_number"] for sub_question in sub_questions
            ]
            sub_question_columns = [
                col for col in df.columns if col in sub_question_numbers
            ]
            df[root_question] = df[sub_question_columns].apply(
                lambda x: delimiter.join(x.dropna().astype(str)), axis=1
            )
            df.drop(sub_question_columns, axis=1, inplace=True)

    return df
