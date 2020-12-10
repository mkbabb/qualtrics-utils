import json
import mimetypes
import os
import pickle
import urllib.parse
import urllib.request
from typing import *

import apiclient
import google
import googleapiclient
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery

from utils.utils import (
    file_components,
    update_url_params,
    url_components,
    download_url_to_json,
)

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

AUTH_DIR = "auth/"

CREDENTIALS_PATH = os.path.join(AUTH_DIR, "credentials.json")
TOKEN_PATH = os.path.join(AUTH_DIR, "token.pickle")

GoogleCredentials = Union["InstalledAppFlow.credentials"]
GoogleService = Union["discovery.Resource"]


def call_google_geocoding_api(address: str, api_key: str) -> Optional[Dict[str, Any]]:
    url = update_url_params(GEOCODE_URL, {"address": address, "key": api_key})

    return download_url_to_json(url=url)


def get_oauth2_creds() -> Optional[GoogleCredentials]:
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)
    return creds


def read_file_from_url(url: str, service: GoogleService) -> Tuple[dict, bytes]:
    files = service.files()
    file_id = url_components(url)["id"][0]

    metadata = files.get(fileId=file_id).execute()
    media = files.get_media(fileId=file_id).execute()

    return (metadata, media)


def update_file_from_url(filepath: str, url: str, service: GoogleService) -> None:
    files = service.files()
    file_id = url_components(url)["id"][0]

    files.update(fileId=file_id, media_body=filepath).execute()


def create_drive_file_object(
    filepath: str,
    google_mime_type: str,
    service: GoogleService,
    mime_type: Optional[str] = None,
    kwargs: Optional[dict] = None,
) -> Dict[str, str]:
    files = service.files()

    if kwargs is None:
        kwargs = {}

    kwargs.setdefault("body", {})
    kwargs.get("body").setdefault(
        "mimeType", f"application/vnd.google-apps.{google_mime_type}"
    )

    if google_mime_type == "folder":
        dirs = str(os.path.normpath(filepath)).split(os.sep)

        # The case of creating a nested folder set.
        # Recurse until we hit the end of the path.
        if len(dirs) > 1:
            parent_id = ""
            for dirname in dirs:
                if parent_id != "":
                    kwargs["body"]["parents"] = [parent_id]

                parent_req = create_drive_file_object(
                    dirname, google_mime_type, service, mime_type, kwargs
                )
                parent_id = parent_req.get("id")

        else:
            kwargs["body"]["name"] = dirs[0]

    else:
        # Else, we need to upload the file via a MediaFileUpload POST.
        _, filename, ext = file_components(filepath)
        kwargs["body"]["name"] = filename + ext

        mime_type = (
            mimetypes.guess_type(filepath)[0] if mime_type is None else mime_type
        )

        media = apiclient.http.MediaFileUpload(
            filepath, mimetype=mime_type, resumable=True
        )
        kwargs["media_body"] = media

    req = files.create(**kwargs)

    return req.execute()


def search_for_file(filename: str, service: GoogleService) -> dict:
    files = service.files()
    return files.list(q=f"name='{filename}'").execute()


def list_files_in_folder(folder_id: str, service: GoogleService) -> dict:
    files = service.files()
    return files.list(q=f"name='{filename}'").execute()


def get_spreadsheet(
    spreadsheet_id: str, range_name: str, service: GoogleService
) -> dict:
    sheet = service.spreadsheets()
    return sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()


def update_spreadsheet(
    spreadsheet_id: str,
    range_name: str,
    values: List[List[Any]],
    service: GoogleService,
    value_input_option: Optional[str] = "USER_ENTERED",
) -> dict:
    sheet = service.spreadsheets()

    body = {"values": values}

    return (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body=body,
            valueInputOption=value_input_option,
        )
        .execute()
    )


if __name__ == "__main__":
    pass
    # filepath = "backend/utils/drive_tests.txt"
    # dirpath, filename, ext = file_components(filepath)

    # creds = get_oauth2_creds()
    # service = discovery.build("drive", "v3", credentials=creds)

    # create_drive_file_object(
    #     filepath,
    #     "file",
    #     service,
    #     None,
    #     {
    #         "body": {
    #             "driveId": "0AGmqvIbfLeKWUk9PVA",
    #             "parents": ["0AGmqvIbfLeKWUk9PVA"],
    #         },
    #         "supportsAllDrives": True,
    #     },
    # )

    # creds = get_oauth2_creds()
    # service = discovery.build("sheets", "v4", credentials=creds)

    # spreadsheet_id = "1m7TFky9XHgTDfLEaQLQFyFqCOg6X8QgImxO_hoeuUEA"
    # range_name = "'Shodan'"

    # data = get_spreadsheet(spreadsheet_id, range_name, service)

    # values = data["values"]

    # values[0][0] = "start_time"

    # update_spreadsheet(spreadsheet_id, range_name, values, service)

