import json
import pathlib

import pandas as pd

from qualtrics_utils import (
    Surveys,
    generate_codebook,
    coalesce_multiselect,
    rename_columns,
)


config_path = pathlib.Path("auth/config.json")
config = json.loads(config_path.read_text())

qualtrics_api_token = config["qualtrics"]["api_token"]
qs = Surveys(api_token=qualtrics_api_token)

survey_id = config["qualtrics"]["survey_id"]

exported_file = qs.get_responses_df(
    surveyId=survey_id, parse_dates=["StartDate", "EndDate"]
)
if exported_file is None:
    raise ValueError("No responses found.")

responses_df = exported_file.data

codebook_path = pathlib.Path(config["qualtrics"]["codebook_path"])

codebook = generate_codebook(codebook_path)
tmp = coalesce_multiselect(responses_df, codebook=codebook)
tmp = rename_columns(tmp, codebook=codebook)
