# This file creates the OpenAPI Python client(s) from the OpenAPI specification.
# See https://api.qualtrics.com/ for each indiviudal API.

cd qualtrics_utils

SINGLE_SURVEY_RESPONSE_URL="https://stoplight.io/api/v1/projects/qualtricsv2/publicapidocs/nodes/reference/surveyResponses.json\?fromExportButton\=true\&snapshotType\=http_service"
SURVEYS_RESPONSE_IMPORT_EXPORT_URL="https://stoplight.io/api/v1/projects/qualtricsv2/publicapidocs/nodes/reference/responseImportsExports.json?fromExportButton=true&snapshotType=http_service"

# array of urls to download
URLS=($SURVEYS_RESPONSE_IMPORT_EXPORT_URL)

# for each url, call the openapi-python-client generate --url command
for url in "${URLS[@]}"
do
    echo "Generating client for $url"
    openapi-python-client generate --url $url
done