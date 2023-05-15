import argparse
import json
import pathlib
from typing import *

from qualtrics_utils.utils import normalize_whitespace, quote_value


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


def tableau_qualtrics_map_func(mapping: dict) -> dict:
    question_number, answer_choices = (
        mapping["question_number"],
        mapping.get("answer_choices", {}),
    )
    return {
        "key": question_number,
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
            quote_value(normalize_whitespace(sub_value), '"'),
        )
        s += f"\tWHEN {key} = {sub_key} THEN {sub_value}\n"

    s += f"END AS {alias}"
    return key, s


def generate_tableau(key_mapping: dict) -> Tuple[str, str]:
    key = key_mapping.get("key", "")
    mapping = key_mapping.get("mapping", {})

    s = ""
    for n, (sub_key, sub_value) in enumerate(mapping.items()):
        sub_key = sub_key if str(sub_key).isnumeric() else quote_value(sub_key, "'")
        sub_value = quote_value(normalize_whitespace(sub_value), "'")

        s += "ELSE" if n > 0 else ""
        s += f"IF [{key}] == {sub_key} THEN "
        s += f"{sub_value} "

    s += f"END"
    return key, s


def map_columns(
    map_filepath: pathlib.Path,
    map_func: Callable[[dict], dict],
    generator_func: Callable[[dict], Tuple[str, str]],
) -> dict:
    with open(map_filepath, "r") as file:
        mapping_list = json.load(file)
        commands = {}

        for mapping in mapping_list:
            key_mapping = map_func(mapping)

            if key_mapping is not None:
                key, command = generator_func(key_mapping)
                commands[key] = command

        return commands


def main() -> None:
    generator_types = ["tableau", "sql"]

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file path.", type=pathlib.Path)
    parser.add_argument(
        "--kind",
        help="Generated output kind.",
        choices=generator_types,
        required=True,
    )

    args = parser.parse_args()

    filepath = args.input
    kind = args.kind
    out_path = filepath.parent / f"{filepath.name}-{kind}-map.json"

    def get_map_and_generator_funcs(kind: str) -> Tuple[Callable, Callable]:
        if kind == "sql":
            # TODO: add proper table name retrieval?
            map_func = sql_qualtrics_map_func
            generator_func = lambda key_mapping: generate_sql("table_name", key_mapping)
            return map_func, generator_func
        elif kind == "tableau":
            return tableau_qualtrics_map_func, generate_tableau
        else:
            return None, None

    map_func, generator_func = get_map_and_generator_funcs(args.kind)

    command = map_columns(filepath, map_func, generator_func)

    with open(out_path, "w") as file:
        json.dump(command, file, indent=4)


if __name__ == "__main__":
    main()
