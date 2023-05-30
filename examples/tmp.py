import json
import pathlib

import pandas as pd

from qualtrics_utils import survey
from qualtrics_utils.codebook.generate import generate_codebook

config_path = pathlib.Path("auth/config.json")
config = json.loads(config_path.read_text())

qualtrics_api_token = config["qualtrics"]["api_token"]
qs = survey.Surveys(api_token=qualtrics_api_token)

survey_id = config["qualtrics"]["survey_id"]

exported_file = qs.get_responses_df(
    surveyId=survey_id, parse_dates=["StartDate", "EndDate"]
)
if exported_file is None:
    raise ValueError("No responses found.")

responses_df = exported_file.data
