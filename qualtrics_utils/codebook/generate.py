import argparse
import json
import pathlib
import re
from typing import *

from qualtrics_utils.utils import normalize_html_string


def map_questions(survey_element: dict[str, Any]) -> Optional[dict[str, Any]]:
    PrimaryAttribute: str = survey_element["PrimaryAttribute"]
    Payload: dict[str, Any] = survey_element["Payload"]

    QuestionText: str = Payload["QuestionText"]
    DataExportTag: str = Payload["DataExportTag"]
    QuestionType: str = Payload["QuestionType"]
    QuestionDescription: str = Payload["QuestionDescription"]

    Choices: Optional[dict[str, Any]] = Payload.get("Choices")
    ChoiceOrder: Optional[list[str]] = Payload.get("ChoiceOrder")

    if Choices is not None and ChoiceOrder is not None:
        ChoiceOrder = [str(i) for i in ChoiceOrder]
        Choices = {key: Choices[key] for key in ChoiceOrder}

    Selector: Optional[str] = Payload.get("Selector")
    RecodeValues: dict[str, str] = Payload.get("RecodeValues", {})

    Answers: Optional[dict[str, Any]] = Payload.get("Answers")
    ChoiceDataExportTags: Optional[dict[str, str] | bool] = Payload.get(
        "ChoiceDataExportTags"
    )

    root_q_num: str = DataExportTag
    root_q_str: str = QuestionText

    def merge_a_choices(
        a_choices: dict[str, str], questions: dict[str, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Merge answer choices into questions."""
        return [
            {
                **value,
                "answer_choices": a_choices,
            }
            for _, value in questions.items()
        ]

    def create_question(
        q_num: str,
        q_str: str,
        a_choices: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """A question object is a question number, question string, and an optional series of
        answer choices. We collate and normalize all three here.

        Qualtrics preserves the raw HTML in both question string and answer choice string,
        so we strip that away here.
        """
        out = {
            "question_number": q_num,
            "question_string": q_str,
        }
        if a_choices is not None:
            return {**out, "answer_choices": a_choices}
        else:
            return out

    def explode_question_number() -> dict[str, dict[str, Any]]:
        """If we have choices to pick from, we map those choices to question numbers.
        If a question number is found in the ChoiceDataExportTags object, that takes
        precedence, so we map it to that number."""
        questions = {}
        if Choices is None or ChoiceOrder is None:
            questions["1"] = create_question(root_q_num, root_q_str)
            return questions

        # sort Choices by ChoiceOrder:

        for key, value in Choices.items():
            sub_q_num = RecodeValues.get(key, key)
            q_num = f"{root_q_num}_{sub_q_num}"

            value = Choices[key]
            q_str = value["Display"]

            if isinstance(ChoiceDataExportTags, dict):
                q_num = ChoiceDataExportTags.get(key, q_num)

            if QuestionType != "TE" and value.get("TextEntry") is not None:
                questions[key] = create_question(q_num, q_str)

                q_num += "_TEXT"
                key += "_TEXT"

                questions[key] = create_question(q_num, q_str)
            else:
                questions[key] = create_question(q_num, q_str)

        return questions

    def process_question() -> Optional[list[dict[str, Any]]]:
        if QuestionType == "Matrix":
            """A 2-d matrix option has one column of questions, then a series of columns as answers.
            For each question in the question column, we merge the answer choices, creating the final 2-d
            result.

            Example in 2-d form:
                a0  a1  a2
            q0  00  00  00
            q1  00  00  00

            Then as a pseudo-dict:

            q0: {a0: 00, a1: 00, a2: 00}
            q1: {a0: 00, a1: 00, a2: 00}
            """
            a_choices = {
                RecodeValues.get(key, key): value["Display"]
                for key, value in Answers.items()  # type: ignore
            }
            questions = explode_question_number()
            return merge_a_choices(a_choices, questions)
        # Multiple choice
        elif QuestionType == "MC":
            # Single answer
            if Selector == "DL" or Selector == "SAVR":
                a_choices = {
                    RecodeValues.get(key, key): value["Display"]
                    for key, value in Choices.items()  # type: ignore
                }
                return [create_question(root_q_num, root_q_str, a_choices)]
            # Multiple answer, which creates a sort-of 2-d matrix.
            elif Selector == "MAVR":
                a_choices = {"-1": "Not Selected", "1": "Selected", "Null": "Not Shown"}
                questions = explode_question_number()
                return merge_a_choices(a_choices, questions)
        # Text entry, so no answer choices here.
        elif QuestionType == "TE":
            questions = explode_question_number()
            return list(questions.values())

        return None

    return {
        "question_number": root_q_num,
        "question_string": root_q_str,
        "question_type": QuestionType,
        "questions": process_question(),
    }


def format_codebook(codebook: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Formats the codebook to be more readable.

    Sorts by question number, and then normalizes the HTML
    in the question string and answer choices."""

    # sort by question number
    codebook.sort(key=lambda x: float(str(x["question_number"]).lstrip("Q")))

    for root_question in codebook:
        root_q_str = root_question["question_string"]
        root_question["question_string"] = normalize_html_string(root_q_str)

        if root_question["questions"] is None:
            continue

        for question in root_question["questions"]:
            q_str, a_choices = (
                question.get("question_string", ""),
                question.get("answer_choices"),
            )
            question["question_string"] = normalize_html_string(q_str)

            if a_choices is not None:
                a_choices = {
                    key: normalize_html_string(value)
                    for key, value in a_choices.items()
                }
                question["answer_choices"] = a_choices

    return codebook


def generate_codebook(filepath: pathlib.Path) -> list[dict[str, Any]]:
    """Generates a codebook from a Qualtrics .qsf file.

    For more information on .qsf files, see:
    https://api.qualtrics.com/docs/qsf

    Args:
        filepath (pathlib.Path): The path to the .qsf file.
    """
    codebook: list[dict[str, Any]] = []

    with open(filepath, "r") as file:
        qsf_json = json.load(file)

        SurveyElements = qsf_json["SurveyElements"]

        for element in SurveyElements:
            Element = element["Element"]

            if Element == "SQ":
                questions = map_questions(element)
                if questions is not None:
                    codebook.append(questions)

    codebook = format_codebook(codebook)

    return codebook


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file path.", type=pathlib.Path)
    args = parser.parse_args()

    filepath = args.input

    if filepath.suffix != ".qsf":
        raise ValueError("Please input a valid .qsf file.")

    out_path = filepath.parent / f"{filepath.stem}-codebook.json"

    codebook = generate_codebook(filepath)

    with open(out_path, "w") as file:
        json.dump(codebook, file, indent=4)


if __name__ == "__main__":
    main()
