import argparse
import json
import pathlib
from typing import *

from qualtrics_utils.codebook.generate import generate_codebook
from qualtrics_utils.utils import normalize_html_string, quote_value

GENERATOR_TYPES = ["tableau", "sql"]


def sql_qualtrics_map_func(mapping: dict) -> dict:
    question_number, question_string, answer_choices = (
        mapping["question_number"],
        mapping["question_string"],
        mapping.get("answer_choices", {}),
    )

    return {
        "key": question_number,
        "alias": question_string,
        "mapping": answer_choices,
    }


def generate_sql(table_name: str, key_mapping: dict) -> Tuple[str, str]:
    key = key_mapping.get("key", "")
    alias = key_mapping.get("alias", key)
    mapping = key_mapping.get("mapping", {})

    s = "CASE\n"

    for sub_key, sub_value in mapping.items():
        sub_key, sub_value = (
            quote_value(sub_key, '"'),
            quote_value(normalize_html_string(sub_value), '"'),
        )
        s += f"\tWHEN {key} = {sub_key} THEN {sub_value}\n"

    s += f"END AS {alias}"
    return key, s


def tableau_qualtrics_map_func(mapping: dict) -> dict:
    question_number, answer_choices = (
        mapping["question_number"],
        mapping.get("answer_choices", {}),
    )
    return {
        "key": question_number,
        "mapping": answer_choices,
    }


def generate_tableau(key_mapping: dict) -> Tuple[str, str]:
    key = key_mapping.get("key", "")
    mapping = key_mapping.get("mapping", {})

    s = ""
    for n, (sub_key, sub_value) in enumerate(mapping.items()):
        sub_key = sub_key if str(sub_key).isnumeric() else quote_value(sub_key, "'")
        sub_value = quote_value(normalize_html_string(sub_value), "'")

        s += "ELSE" if n > 0 else ""
        s += f"IF [{key}] == {sub_key} THEN "
        s += f"{sub_value} "

    s += f"END"
    return key, s


def get_map_and_generator_funcs(kind: str) -> tuple[Callable, Callable]:
    if kind == "sql":
        map_func = sql_qualtrics_map_func
        generator_func = lambda key_mapping: generate_sql("$$TABLE_NAME$$", key_mapping)
        return map_func, generator_func
    elif kind == "tableau":
        return tableau_qualtrics_map_func, generate_tableau

    raise ValueError(f"Invalid kind: {kind}")


def map_columns(
    input_filepath: pathlib.Path,
    kind: str,
) -> dict:
    map_func, generator_func = get_map_and_generator_funcs(kind)

    with open(input_filepath, "r") as file:
        mapping_list = (
            json.load(file)
            if input_filepath.suffix == ".json"
            else generate_codebook(input_filepath)
        )

        commands = {}
        for mapping in mapping_list:
            key_mapping = map_func(mapping)

            if key_mapping is None:
                continue

            key, command = generator_func(key_mapping)
            commands[key] = command

        return commands


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file path.", type=pathlib.Path)
    parser.add_argument(
        "--kind",
        help="Generated output kind.",
        choices=GENERATOR_TYPES,
        default=GENERATOR_TYPES[0],
    )

    args = parser.parse_args()

    filepath = args.input
    kind = args.kind
    out_path = filepath.parent / f"{filepath.name}-{kind}-map.json"

    commands = map_columns(filepath, kind)

    with open(out_path, "w") as file:
        json.dump(commands, file, indent=4)


if __name__ == "__main__":
    main()
