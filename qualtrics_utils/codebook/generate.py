import argparse
import json
import pathlib
import re
from typing import *

from qualtrics_utils.utils import get_multiple, normalize_whitespace

RE_HTML_TAG = re.compile(r"<(.|\s)*?>")

RE_SPACE = re.compile(r"&nbsp;")


def normalize_html_string(s: str) -> str:
    s = re.sub(RE_HTML_TAG, "", s)
    s = re.sub(RE_SPACE, " ", s)
    s = normalize_whitespace(s)
    return s


def map_questions(survey_element: dict) -> Optional[dict]:
    PrimaryAttribute, Payload = (
        survey_element["PrimaryAttribute"],
        survey_element["Payload"],
    )
    (
        QuestionText,
        DataExportTag,
        QuestionType,
        QuestionDescription,
        Choices,
        ChoiceOrder,
        Selector,
        RecodeValues,
        Answers,
        ChoiceDataExportTags,
    ) = get_multiple(
        Payload,
        "QuestionText",
        "DataExportTag",
        "QuestionType",
        "QuestionDescription",
        "Choices",
        "ChoiceOrder",
        "Selector",
        "RecodeValues",
        "Answers",
        "ChoiceDataExportTags",
    ).values()

    root_q_num = DataExportTag
    root_q_str = QuestionText

    map_recode_values: Callable[[str], str] = (
        lambda key: RecodeValues.get(key, key) if RecodeValues is not None else key
    )

    merge_a_choices: Callable[[dict, dict], list[dict]] = lambda a_choices, questions: [
        {
            **value,
            "answer_choices": a_choices,
        }
        for _, value in questions.items()
    ]

    def create_question(
        q_num: str,
        q_str: str,
        a_choices: Optional[dict] = None,
    ) -> dict:
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

    def explode_question_number() -> dict:
        """If we have choices to pick from, we map those choices to question numbers.
        If a question number is found in the ChoiceDataExportTags object, that takes
        precedence, so we map it to that number."""
        questions = {}

        if isinstance(Choices, dict):
            for key in ChoiceOrder:
                key = str(key)
                value = Choices[key]

                q_str = f"{root_q_str} - {value['Display']}"

                sub_q_num = map_recode_values(key)
                q_num = f"{root_q_num}_{sub_q_num}"

                if isinstance(ChoiceDataExportTags, dict):
                    q_num = ChoiceDataExportTags.get(key, q_num)

                if QuestionType != "TE" and value.get("TextEntry") is not None:
                    questions[key] = create_question(q_num, q_str)

                    q_num += "_TEXT"
                    key += "_TEXT"

                    questions[key] = create_question(q_num, q_str)
                else:
                    questions[key] = create_question(q_num, q_str)
        else:
            questions["1"] = create_question(root_q_num, root_q_str)

        return questions

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
            map_recode_values(key): value["Display"] for key, value in Answers.items()
        }
        questions = explode_question_number()

        return merge_a_choices(a_choices, questions)
    # Multiple choice
    elif QuestionType == "MC":
        # Single answer
        if Selector == "DL" or Selector == "SAVR":
            a_choices = {
                map_recode_values(key): value["Display"]
                for key, value in Choices.items()
            }
            return [create_question(root_q_num, root_q_str, a_choices)]
        # Multiple answer, which creates a sort of 2-d matrix.
        elif Selector == "MAVR":
            a_choices = {"-1": "Not Selected", "1": "Selected", "Null": "Not Shown"}
            questions = explode_question_number()
            return merge_a_choices(a_choices, questions)
        else:
            return None
    # Text entry, so no answer choices here.
    elif QuestionType == "TE":
        questions = explode_question_number()
        return list(questions.values())
    else:
        return None


def format_codebook(codebook: list[dict]) -> list[dict]:
    """Format the codebook to be more readable.
    Sorts the codebook by question number, and normalizes the HTML
    in the question string and answer choices."""

    def codebook_key(question: dict) -> float:
        try:
            question_number = question["question_number"]
            return float(question_number.split("Q")[1])
        except:
            return float("inf")

    codebook = sorted(codebook, key=codebook_key)

    for question in codebook:
        q_str, a_choices = (
            question.get("question_string", ""),
            question.get("answer_choices"),
        )

        question["question_string"] = normalize_html_string(q_str)

        if a_choices is not None:
            a_choices = {
                key: normalize_html_string(value) for key, value in a_choices.items()
            }
            question["answer_choices"] = a_choices

    return codebook


def generate_codebook(filepath: pathlib.Path) -> list[dict]:
    """Generate a codebook from a Qualtrics .qsf file."""
    codebook: list[dict] = []

    with open(filepath, "r") as file:
        qsf_json = json.load(file)

        SurveyElements = qsf_json["SurveyElements"]

        for element in SurveyElements:
            Element = element["Element"]

            if Element == "SQ":
                questions = map_questions(element)
                if questions is not None:
                    codebook.extend(questions)

    codebook = format_codebook(codebook)

    return codebook


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file path.", type=pathlib.Path)
    args = parser.parse_args()

    filepath = args.input

    if filepath.suffix != ".qsf":
        raise ValueError("Please input a valid .qsf file.")

    out_path = filepath.parent / f"{filepath.stem}-codebook"

    codebook = generate_codebook(filepath)

    with open(out_path, "w") as file:
        json.dump(codebook, file, indent=4)


if __name__ == "__main__":
    main()
