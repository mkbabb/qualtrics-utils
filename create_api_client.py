#! /usr/bin/env python3

from pathlib import Path
import shutil
from openapi_python_client import create_new_client, MetaType, Config
import urllib.parse

MODULE_PATH = Path("./qualtrics_utils")

BASE_URL = (
    "https://stoplight.io/api/v1/projects/qualtricsv2/publicapidocs/nodes/reference/"
)


def get_curr_folders() -> set[Path]:
    cwd = Path.cwd()
    return set([p for p in cwd.glob("*") if p.is_dir()])


def generate_openapi_clients() -> None:
    urls = [
        # Single Response Export
        "singleResponses.json?fromExportButton=true&snapshotType=http_service",
        # Survey Responses Export
        "responseImportsExports.json?fromExportButton=true&snapshotType=http_service",
    ]

    curr_folders = get_curr_folders()

    for url in urls:
        url = urllib.parse.urljoin(BASE_URL, url)

        print(f"Generating client for {url}")

        errors = create_new_client(
            url=url, path=None, meta=MetaType.NONE, config=Config()
        )
        if len(errors) > 0:
            print(errors)

        t_curr_folders = get_curr_folders()
        new_folders = list(t_curr_folders - curr_folders)

        if not len(new_folders):
            continue

        new_folder = new_folders[0]

        t_new_folder: Path = MODULE_PATH / new_folder.name
        if t_new_folder.exists():
            shutil.rmtree(t_new_folder)

        shutil.move(new_folder, MODULE_PATH / new_folder.name)


if __name__ == "__main__":
    generate_openapi_clients()
