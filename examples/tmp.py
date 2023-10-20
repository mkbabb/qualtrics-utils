import json
import pathlib

import pandas as pd

from qualtrics_utils import (
    Surveys,
    coalesce_multiselect,
    generate_codebook,
    rename_columns,
)
from googleapiutils2 import Sheets, get_oauth2_creds

from qualtrics_utils.sync import sync, SyncType
from qualtrics_utils.utils import create_mysql_engine


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
    tmp = rename_columns(tmp, codebook=codebook, verbose=False)

    return tmp


# sync(
#     survey_id=survey_id,
#     surveys=surveys,
#     sync_type=SyncType.SHEETS,
#     response_post_processing_func=post_processing_func,
#     sheet_name="Sheet1",
#     sheet_url=responses_url,
#     sheets=sheets,
# )


start_date = "2023-05-09T00:00:00Z"
start_date = pd.to_datetime(start_date)

engine = create_mysql_engine(
    **config["mysql"],
)


with engine.connect() as conn:
    table_name = "de_2023"

    sync(
        survey_id=survey_id,
        surveys=surveys,
        sync_type=SyncType.SQL,
        response_post_processing_func=post_processing_func,
        #
        start_date=start_date,
        #
        conn=conn,
        table_name=table_name,
    )
