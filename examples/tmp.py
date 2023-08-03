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

config_path = pathlib.Path("auth/config.json")
config = json.loads(config_path.read_text())

qualtrics_api_token = config["qualtrics"]["api_token"]
qs = Surveys(api_token=qualtrics_api_token)

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


sync_responses_sheets(
    survey_id=survey_id,
    sheet_name="Sheet1",
    sheet_url=responses_url,
    surveys=qs,
    sheets=sheets,
    post_processing_func=post_processing_func,
)
