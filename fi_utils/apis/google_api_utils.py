from fi_utils.utils import url_get_json
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
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from utils.utils import file_components, update_url_params, url_components

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

AUTH_DIR = "auth/"

CREDENTIALS_PATH = os.path.join(AUTH_DIR, "shodan-reporter-credentials.json")
TOKEN_PATH = os.path.join(AUTH_DIR, "token.pickle")

GoogleCredentials = Union["InstalledAppFlow.credentials"]
GoogleService = Union["discovery.Resource"]


MIME_TYPES = {
    "Documents": {"Plain text": "text/plain"},
    "Spreadsheets": {
        "MS Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "CSV (first sheet only)": "text/csv",
    },
}


def call_google_geocoding_api(address: str, api_key: str) -> Optional[Dict[str, Any]]:
    url = update_url_params(GEOCODE_URL, {"address": address, "key": api_key})
    return url_get_json(url=url)


def get_oauth2_creds(is_service_account: bool = False) -> Optional[GoogleCredentials]:
    if not is_service_account:
        creds = None

        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)
        return creds
    else:
        if os.path.exists(CREDENTIALS_PATH):
            service_account_info = json.load(open(CREDENTIALS_PATH, "r"))

            return service_account.Credentials.from_service_account_info(
                service_account_info, scopes=SCOPES
            )


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


def create_google_mime_type(google_mime_type: str) -> str:
    return f"application/vnd.google-apps.{google_mime_type}"


def upload_drive_file_object(
    filepath: str,
    google_mime_type: str,
    service: GoogleService,
    mime_type: Optional[str] = None,
    kwargs: Optional[dict] = None,
) -> Dict[str, str]:
    files = service.files()

    if kwargs is None:
        kwargs = {}

    kwargs["body"] = {
        "name": filepath,
        "mimeType": create_google_mime_type(google_mime_type),
        **kwargs.get("body", {}),
    }

    if google_mime_type == "folder":
        dirs = str(os.path.normpath(filepath)).split(os.sep)

        # The case of creating a nested folder set.
        # Recurse until we hit the end of the path.
        if len(dirs) > 1:
            parent_id = ""
            for dirname in dirs:
                if parent_id != "":
                    kwargs["body"]["parents"] = [parent_id]

                parent_req = upload_drive_file_object(
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


def create_drive_file_object(
    filepath: str,
    google_mime_type: str,
    service: GoogleService,
    kwargs: Optional[dict] = None,
):
    files = service.files()

    if kwargs is None:
        kwargs = {}

    kwargs["body"] = {
        "name": filepath,
        "mimeType": create_google_mime_type(google_mime_type),
        **kwargs.get("body", {}),
    }

    req = files.create(**kwargs)

    return req.execute()


def copy_file(
    service: GoogleService,
    file_id: str,
    filename: Optional[str],
    folder_id: Optional[str],
) -> Optional[dict]:
    body = {"name": filename, "parents": [folder_id]}

    try:
        return service.files().copy(fileId=file_id, body=body).execute()
    except:
        return None


def get_files(q: str, service: GoogleService) -> Iterable[dict]:
    files = service.files()

    page_token = None
    while True:
        response = files.list(q=q, pageToken=page_token).execute()

        for file in response.get("files", []):
            yield file

        page_token = response.get("nextPageToken", None)

        if page_token is None:
            break


def list_files_in_folder(folder_id: str, service: GoogleService) -> Iterable[dict]:
    return get_files(q=f"'{folder_id}' in parents", service=service)


def get_spreadsheet(
    spreadsheet_id: str, range_name: str, service: GoogleService
) -> dict:
    sheets = service.spreadsheets()
    return sheets.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()


def update_spreadsheet(
    spreadsheet_id: str,
    range_name: str,
    values: List[List[Any]],
    service: GoogleService,
    value_input_option: Optional[str] = "USER_ENTERED",
) -> dict:
    sheets = service.spreadsheets()

    body = {"values": values}

    return (
        sheets.values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body=body,
            valueInputOption=value_input_option,
        )
        .execute()
    )


def export_document(
    out_filepath: str, file_id: str, mime_type: str, service: GoogleService
):
    files = service.files()
    request = files.export_media(fileId=file_id, mimeType=mime_type)

    with open(out_filepath, "wb") as out_file:
        downloader = apiclient.http.MediaIoBaseDownload(out_file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()


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
