import argparse
import json
import os
import re
from typing import *

import yaml

from fi_utils.utils import file_components, get_multiple, normalize_whitespace

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

    merge_a_choices: Callable[[dict, dict], List[dict]] = lambda a_choices, questions: [
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


def create_codebook(filepath: str) -> List[dict]:
    codebook: List[dict] = []

    with open(filepath, "r") as file:
        qsf_json = json.load(file)

        SurveyElements = qsf_json["SurveyElements"]

        for element in SurveyElements:
            Element = element["Element"]

            if Element == "SQ":
                questions = map_questions(element)
                if questions is not None:
                    codebook.extend(questions)

    return codebook


def main() -> None:
    OUTPUT_TYPES = ["json", "yaml"]

    parser = argparse.ArgumentParser(
        description="""Takes in an input Qualtrics qsf file and returns the numeric
    code values mapped to their string counterparts.
    Outputs a true JSON codebook.

    To ensure the output codebook is as accurate as possible, please clear the
    trash in Qualtrics before saving the .qsf file!
    """
    )
    parser.add_argument("input", help="Input file path.")
    parser.add_argument("--output_type", choices=OUTPUT_TYPES, default=OUTPUT_TYPES[0])
    args = parser.parse_args()

    filepath = args.input
    dirpath, filename, ext = file_components(filepath)
    output_type = args.output_type

    if ext != ".qsf":
        raise ValueError("Please input a valid .qsf file.")

    out_path = os.path.join(dirpath, f"{filename}-codebook")

    def codebook_key(question: dict) -> float:
        try:
            question_number = question["question_number"]
            return float(question_number.split("Q")[1])
        except:
            return float("inf")

    codebook = create_codebook(filepath)
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

    if output_type == OUTPUT_TYPES[0]:
        with open(out_path + ".json", "w") as file:
            json.dump(codebook, file, indent=4)
    elif output_type == OUTPUT_TYPES[1]:
        noalias_dumper = yaml.dumper.SafeDumper
        noalias_dumper.ignore_aliases = lambda self, data: True

        with open(out_path + ".yaml", "w") as file:
            stream = yaml.dump(
                codebook,
                Dumper=noalias_dumper,
                indent=4,
                default_flow_style=False,
                sort_keys=False,
            )
            file.write(stream.replace("\n- ", "\n\n- "))


if __name__ == "__main__":
    main()
