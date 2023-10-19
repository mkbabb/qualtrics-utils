# qualtrics-utils

Utilities for qualtrics surveys. Get survey responses, generate codebooks, & c.

## [`surveys`](qualtrics_utils/surveys.py)

Module to interact with Qualtrics surveys.

Example (get a survey's responses, convert to a pandas DataFrame):

```python
from qualtrics_utils.survey import Surveys

qs = Surveys(api_token=QUALTRICS_API_TOKEN)

exported_file = qs.get_responses_df(
    survey_id=SURVEY_ID, parse_dates=["StartDate", "EndDate"]
)
df = exported_file.data
```

## Codebook mapping

### [`generate.py`](qualtrics_utils/codebook/generate_codebook.py)

Takes the exported `.qsf` file from Qualtrics and generates a codebook mapping question
IDs to question text and answer choices. The output is a JSON file containing a list of
dictionaries.

Example row:

```json
{
        "question_number": "Q5.10",
        "question_string": "What is your role at this school?",
        "answer_choices": "..."
},
```

### [`map_columns.py`](qualtrics_utils/codebook/map_codebook_columns.py)

Takes a codebook mapping (generated by the above function) and creates conditional
statements to map the question columns into valid Tableau or SQL code. Used to create a
singular question column in the above formats when there are multiple questions in a
single question block (e.g. multiple Likert scale questions).
