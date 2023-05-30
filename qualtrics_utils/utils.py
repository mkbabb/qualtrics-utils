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


def rename_columns(df: pd.DataFrame, codebook: list[dict[str, Any]]) -> pd.DataFrame:
    renaming_map = {}
    for question in codebook:
        root_q_num = question["question_number"]
        sub_questions = question.get("questions")

        if root_q_num in df.columns:
            renaming_map[root_q_num] = f"{root_q_num} - {question['question_string']}"

        if sub_questions is not None and len(sub_questions) >= 1:
            for sub_question in sub_questions:
                q_num = sub_question["question_number"]
                if not q_num in df.columns:
                    continue

                renaming_map[
                    q_num
                ] = f"{root_q_num} - {sub_question['question_string']}"

    df.rename(columns=renaming_map, inplace=True, errors="ignore")
    return df


def coalesce_multiselect(
    df: pd.DataFrame,
    codebook: list[dict[str, Any]],
    delimiter: str = ", ",
    use_other: bool = True,
) -> pd.DataFrame:
    def join(x: pd.Series) -> str:
        l = x.dropna().tolist()

        if use_other and len(l) > 1:
            return "Other"
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
