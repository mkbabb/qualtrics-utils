import json
import pathlib

import pandas as pd

from qualtrics_utils import (
    Surveys,
    coalesce_multiselect,
    generate_codebook,
    rename_columns,
    sync_responses_sheets,
)
from googleapiutils2 import Sheets, get_oauth2_creds

from qualtrics_utils.sync import (
    get_last_status_sheets,
    write_responses_sheets,
    write_status_sheets,
)

config_path = pathlib.Path("auth/config.json")
config = json.loads(config_path.read_text())

qualtrics_api_token = config["qualtrics"]["api_token"]
surveys = Surveys(api_token=qualtrics_api_token)

survey_id = config["qualtrics"]["survey_id"]

responses_url = config["google"]["urls"]["responses"]

creds = get_oauth2_creds(config["google"]["credentials_path"])
sheets = Sheets(creds=creds)


def post_processing_func(df: pd.DataFrame):
    codebook_path = pathlib.Path(config["qualtrics"]["codebook_path"])

    codebook = generate_codebook(codebook_path)
    tmp = coalesce_multiselect(df, codebook=codebook)
    tmp = rename_columns(tmp, codebook=codebook)

    return tmp


sheet_url = responses_url
sheet_name = "Sheet1"

last_status = get_last_status_sheets(
    survey_id=survey_id, sheet_url=sheet_url, sheets=sheets
)
last_response_id = last_status["last_response_id"] if last_status is not None else None

exported_file = surveys.get_responses_df(
    survey_id=survey_id,
    last_response_id=last_response_id,
)
exported_file.data = post_processing_func(exported_file.data)

write_responses_sheets(
    exported_file=exported_file,
    sheet_name=sheet_name,
    sheet_url=sheet_url,
    sheets=sheets,
)

write_status_sheets(
    exported_file=exported_file,
    sheet_url=sheet_url,
    sheets=sheets,
)
