from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.default_error_response import DefaultErrorResponse
from ...models.get_schema_response import GetSchemaResponse
from ...models.survey_not_found_response import SurveyNotFoundResponse
from ...types import Response


def _get_kwargs(
    survey_id: str,
) -> Dict[str, Any]:

    pass

    return {
        "method": "get",
        "url": "/surveys/{surveyId}/response-schema".format(
            surveyId=survey_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetSchemaResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = SurveyNotFoundResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = DefaultErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]:
    r"""Retrieve Survey JSON Schema

     ## Introduction

    This documentation is meant to help explain the purpose and value of the Retrieve the JSON Schema
    endpoint in the public api. In short, this endpoint provides a [standard JSON Schema](https://json-
    schema.org/) that can be used for parsing the results from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint
    and the [Create Response Export](./legacyResponseImportsExports.json/paths/~1responseexports/post)
    endpoint when exporting in the json format. Finally this endpoint can also be useful for preparing
    responses for the [Create a New
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses/post) endpoint.

    # Example

    Note, before reading through this example, it might be helpful to take a quick detour and gain a bit
    of familiarity around Json Schemas.
    For this example we created a simple survey with a single multiple choice question `Which type of
    Ice Cream is your favorite?` and 4 options `Chocolate`, `Vanilla`, `Cookies & Cream`, and
    `Strawberry`.
    Here's an example response that we requested from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint:

    ```json
    {
        \"responseId\": \"R_240YEnuWbbwZOy1\",
        \"values\": {
            \"startDate\": \"2020-05-13T19:26:15Z\",
            \"endDate\": \"2020-05-13T19:26:18Z\",
            \"status\": 0,
            \"ipAddress\": \"70.103.180.85\",
            \"progress\": 100,
            \"duration\": 2,
            \"finished\": 1,
            \"recordedDate\": \"2020-05-13T19:26:18.487Z\",
            \"locationLatitude\": \"40.3941955566\",
            \"locationLongitude\": \"-111.848297119\",
            \"distributionChannel\": \"anonymous\",
            \"userLanguage\": \"EN\",
            \"QID1\": 3,
            \"QID1_DO\": [
                \"1\",
                \"2\",
                \"3\",
                \"4\"
            ]
        },
        \"labels\": {
            \"status\": \"IP Address\",
            \"finished\": \"True\",
            \"QID1\": \"Cookies & Cream\",
            \"QID1_DO\": [
                \"Chocolate\",
                \"Vanilla\",
                \"Cookies & Cream\",
                \"Strawberry\"
            ]
        },
        \"displayedFields\": [
            \"QID1\"
        ],
        \"displayedValues\": {
            \"QID1\": [
                1,
                2,
                3,
                4
            ]
        }
    }
    ```

    Now, let's look at the pieces of the schema to understand them a little better. Note: this
    documentation won't attempt to cover all the aspects of the JSON Schema specification, for more
    information see [https://json-schema.org/](https://json-schema.org/).

    ```json
    {
        \"$schema\": \"https://json-schema.org/draft/2019-09/schema\",
        \"$id\": \"http://qualtrics.com/API/v3/surveys/SV_ai71yqu2ZLvpadf/response-schema\",
        \"title\": \"JSON Schema Example (SV_ai71yqu2ZLvpadf) - Survey Response\",
        \"description\": \"This is a schema for survey responses from SV_ai71yqu2ZLvpadf\",
        \"type\": \"object\",
    ```

    The schema starts with several standard fields from the Json Schema specification. The value for
    `$schema` is explained [here](https://json-schema.org/draft/2019-09/json-schema-
    core.html#rfc.section.8.1.1) and the value for `$id` is explained [here](https://json-
    schema.org/draft/2019-09/json-schema-core.html#id-keyword). Then, the schema is given a title and a
    description. Finally, the schema is defined for a JSON [object](https://json-
    schema.org/draft/2019-09/json-schema-core.html#rfc.section.4.2.1) primitive type.

    ```json
        \"required\": [
            \"values\",
            \"displayedFields\",
            \"displayedValues\",
            \"labels\",
            \"responseId\"
        ],
    ```

    Next, the `required` field specifies that our JSON `object` will have the certain required fields.
    Looking back at our example response, we see that each of these fields is present.

    ```json
        \"properties\": {
            \"responseId\": {
                \"type\": \"string\"
            },
    ```

    Inside of the `properties` object, each field previously mentioned in the `required` array are given
    a schema. The simplest of these fields is the responseId field which will just be provided as a
    string.

    ```json
            \"displayedFields\": {
                \"type\": \"array\",
                \"description\": \"A list of questions or question rows that were displayed to the
    survey respondent\",
                \"items\": {
                    \"type\": \"string\"
                }
            },
            \"displayedValues\": {
                \"type\": \"object\",
                \"description\": \"A list of the possible answers shown to the survey respondent for
    each question or question row\",
                \"additionalProperties\": {
                    \"type\": \"array\"
                }
            },
            \"labels\": {
                \"type\": \"object\",
                \"description\": \"The labels of the answers given by the survey respondent for each
    question or question row\",
                \"additionalProperties\": true
            },
    ```

    The next fields `displayedFields`, `displayedValues`, and `labels` have descriptions built in to the
    schema. Again, we can see how these schemas translate into a response object by consulting our
    example.

    ```json
            \"values\": {
                \"type\": \"object\",
                \"description\": \"The answers given by the survey respondent\",
                \"properties\": {
                    \"QID1\": {
                        \"description\": \"Which type of Ice Cream is your favorite?\",
                        \"dataType\": \"question\",
                        \"type\": \"number\",
                        \"oneOf\": [
                            {
                                \"label\": \"Chocolate\",
                                \"const\": 1
                            },
                            {
                                \"label\": \"Vanilla\",
                                \"const\": 2
                            },
                            {
                                \"label\": \"Cookies & Cream\",
                                \"const\": 3
                            },
                            {
                                \"label\": \"Strawberry\",
                                \"const\": 4
                            }
                        ],
                        \"exportTag\": \"Q1\",
                        \"questionId\": \"QID1\"
                    },
                    \"recordedDate\": {
                        \"description\": \"Recorded Date\",
                        \"dataType\": \"metadata\",
                        \"type\": \"string\",
                        \"format\": \"date-time\",
                        \"exportTag\": \"RecordedDate\"
                    },
                    \"duration\": {
                        \"description\": \"Duration (in seconds)\",
                        \"dataType\": \"metadata\",
                        \"type\": \"number\",
                        \"exportTag\": \"Duration (in seconds)\"
                    },
    ```

    Finally, the values property defines the schema for each value available in the response. I've
    pulled a couple of the fields from the schema into this documentation but we can see from the
    example response that there are many more fields in this schema. Here we can see a `description` for
    each field as well as a `type` and several other pieces of information. We can see that the `type`
    matches up with the JSON data type for each value as found in the example response. The `dataType`
    can be used to know the source for that value and the `exportTag` is useful for understanding the
    header columns when using the [Create Response
    Export](./responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-responses/post) endpoint
    with the CSV or TSV formats. Lastly, oneOf enumerates the possible options for values that have a
    known, finite domain. For this example, a multiple choice question would have a oneOf field since
    there are only 4 possible values. However, a text entry field that only allows numbers would not
    have a oneOf field, since the domain can't be enumerated.

    ## Additional Tooling for JSON Schemas

    One of the benefits of having a schema is that it can be used to automate some of the parsing and
    usage of json schemas. One such tool for automating this step is
    [Quicktype](https://app.quicktype.io/#l=schema). More information about that tool can be found on
    [Github](https://github.com/quicktype/quicktype).


    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]:
    r"""Retrieve Survey JSON Schema

     ## Introduction

    This documentation is meant to help explain the purpose and value of the Retrieve the JSON Schema
    endpoint in the public api. In short, this endpoint provides a [standard JSON Schema](https://json-
    schema.org/) that can be used for parsing the results from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint
    and the [Create Response Export](./legacyResponseImportsExports.json/paths/~1responseexports/post)
    endpoint when exporting in the json format. Finally this endpoint can also be useful for preparing
    responses for the [Create a New
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses/post) endpoint.

    # Example

    Note, before reading through this example, it might be helpful to take a quick detour and gain a bit
    of familiarity around Json Schemas.
    For this example we created a simple survey with a single multiple choice question `Which type of
    Ice Cream is your favorite?` and 4 options `Chocolate`, `Vanilla`, `Cookies & Cream`, and
    `Strawberry`.
    Here's an example response that we requested from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint:

    ```json
    {
        \"responseId\": \"R_240YEnuWbbwZOy1\",
        \"values\": {
            \"startDate\": \"2020-05-13T19:26:15Z\",
            \"endDate\": \"2020-05-13T19:26:18Z\",
            \"status\": 0,
            \"ipAddress\": \"70.103.180.85\",
            \"progress\": 100,
            \"duration\": 2,
            \"finished\": 1,
            \"recordedDate\": \"2020-05-13T19:26:18.487Z\",
            \"locationLatitude\": \"40.3941955566\",
            \"locationLongitude\": \"-111.848297119\",
            \"distributionChannel\": \"anonymous\",
            \"userLanguage\": \"EN\",
            \"QID1\": 3,
            \"QID1_DO\": [
                \"1\",
                \"2\",
                \"3\",
                \"4\"
            ]
        },
        \"labels\": {
            \"status\": \"IP Address\",
            \"finished\": \"True\",
            \"QID1\": \"Cookies & Cream\",
            \"QID1_DO\": [
                \"Chocolate\",
                \"Vanilla\",
                \"Cookies & Cream\",
                \"Strawberry\"
            ]
        },
        \"displayedFields\": [
            \"QID1\"
        ],
        \"displayedValues\": {
            \"QID1\": [
                1,
                2,
                3,
                4
            ]
        }
    }
    ```

    Now, let's look at the pieces of the schema to understand them a little better. Note: this
    documentation won't attempt to cover all the aspects of the JSON Schema specification, for more
    information see [https://json-schema.org/](https://json-schema.org/).

    ```json
    {
        \"$schema\": \"https://json-schema.org/draft/2019-09/schema\",
        \"$id\": \"http://qualtrics.com/API/v3/surveys/SV_ai71yqu2ZLvpadf/response-schema\",
        \"title\": \"JSON Schema Example (SV_ai71yqu2ZLvpadf) - Survey Response\",
        \"description\": \"This is a schema for survey responses from SV_ai71yqu2ZLvpadf\",
        \"type\": \"object\",
    ```

    The schema starts with several standard fields from the Json Schema specification. The value for
    `$schema` is explained [here](https://json-schema.org/draft/2019-09/json-schema-
    core.html#rfc.section.8.1.1) and the value for `$id` is explained [here](https://json-
    schema.org/draft/2019-09/json-schema-core.html#id-keyword). Then, the schema is given a title and a
    description. Finally, the schema is defined for a JSON [object](https://json-
    schema.org/draft/2019-09/json-schema-core.html#rfc.section.4.2.1) primitive type.

    ```json
        \"required\": [
            \"values\",
            \"displayedFields\",
            \"displayedValues\",
            \"labels\",
            \"responseId\"
        ],
    ```

    Next, the `required` field specifies that our JSON `object` will have the certain required fields.
    Looking back at our example response, we see that each of these fields is present.

    ```json
        \"properties\": {
            \"responseId\": {
                \"type\": \"string\"
            },
    ```

    Inside of the `properties` object, each field previously mentioned in the `required` array are given
    a schema. The simplest of these fields is the responseId field which will just be provided as a
    string.

    ```json
            \"displayedFields\": {
                \"type\": \"array\",
                \"description\": \"A list of questions or question rows that were displayed to the
    survey respondent\",
                \"items\": {
                    \"type\": \"string\"
                }
            },
            \"displayedValues\": {
                \"type\": \"object\",
                \"description\": \"A list of the possible answers shown to the survey respondent for
    each question or question row\",
                \"additionalProperties\": {
                    \"type\": \"array\"
                }
            },
            \"labels\": {
                \"type\": \"object\",
                \"description\": \"The labels of the answers given by the survey respondent for each
    question or question row\",
                \"additionalProperties\": true
            },
    ```

    The next fields `displayedFields`, `displayedValues`, and `labels` have descriptions built in to the
    schema. Again, we can see how these schemas translate into a response object by consulting our
    example.

    ```json
            \"values\": {
                \"type\": \"object\",
                \"description\": \"The answers given by the survey respondent\",
                \"properties\": {
                    \"QID1\": {
                        \"description\": \"Which type of Ice Cream is your favorite?\",
                        \"dataType\": \"question\",
                        \"type\": \"number\",
                        \"oneOf\": [
                            {
                                \"label\": \"Chocolate\",
                                \"const\": 1
                            },
                            {
                                \"label\": \"Vanilla\",
                                \"const\": 2
                            },
                            {
                                \"label\": \"Cookies & Cream\",
                                \"const\": 3
                            },
                            {
                                \"label\": \"Strawberry\",
                                \"const\": 4
                            }
                        ],
                        \"exportTag\": \"Q1\",
                        \"questionId\": \"QID1\"
                    },
                    \"recordedDate\": {
                        \"description\": \"Recorded Date\",
                        \"dataType\": \"metadata\",
                        \"type\": \"string\",
                        \"format\": \"date-time\",
                        \"exportTag\": \"RecordedDate\"
                    },
                    \"duration\": {
                        \"description\": \"Duration (in seconds)\",
                        \"dataType\": \"metadata\",
                        \"type\": \"number\",
                        \"exportTag\": \"Duration (in seconds)\"
                    },
    ```

    Finally, the values property defines the schema for each value available in the response. I've
    pulled a couple of the fields from the schema into this documentation but we can see from the
    example response that there are many more fields in this schema. Here we can see a `description` for
    each field as well as a `type` and several other pieces of information. We can see that the `type`
    matches up with the JSON data type for each value as found in the example response. The `dataType`
    can be used to know the source for that value and the `exportTag` is useful for understanding the
    header columns when using the [Create Response
    Export](./responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-responses/post) endpoint
    with the CSV or TSV formats. Lastly, oneOf enumerates the possible options for values that have a
    known, finite domain. For this example, a multiple choice question would have a oneOf field since
    there are only 4 possible values. However, a text entry field that only allows numbers would not
    have a oneOf field, since the domain can't be enumerated.

    ## Additional Tooling for JSON Schemas

    One of the benefits of having a schema is that it can be used to automate some of the parsing and
    usage of json schemas. One such tool for automating this step is
    [Quicktype](https://app.quicktype.io/#l=schema). More information about that tool can be found on
    [Github](https://github.com/quicktype/quicktype).


    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]
    """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]:
    r"""Retrieve Survey JSON Schema

     ## Introduction

    This documentation is meant to help explain the purpose and value of the Retrieve the JSON Schema
    endpoint in the public api. In short, this endpoint provides a [standard JSON Schema](https://json-
    schema.org/) that can be used for parsing the results from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint
    and the [Create Response Export](./legacyResponseImportsExports.json/paths/~1responseexports/post)
    endpoint when exporting in the json format. Finally this endpoint can also be useful for preparing
    responses for the [Create a New
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses/post) endpoint.

    # Example

    Note, before reading through this example, it might be helpful to take a quick detour and gain a bit
    of familiarity around Json Schemas.
    For this example we created a simple survey with a single multiple choice question `Which type of
    Ice Cream is your favorite?` and 4 options `Chocolate`, `Vanilla`, `Cookies & Cream`, and
    `Strawberry`.
    Here's an example response that we requested from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint:

    ```json
    {
        \"responseId\": \"R_240YEnuWbbwZOy1\",
        \"values\": {
            \"startDate\": \"2020-05-13T19:26:15Z\",
            \"endDate\": \"2020-05-13T19:26:18Z\",
            \"status\": 0,
            \"ipAddress\": \"70.103.180.85\",
            \"progress\": 100,
            \"duration\": 2,
            \"finished\": 1,
            \"recordedDate\": \"2020-05-13T19:26:18.487Z\",
            \"locationLatitude\": \"40.3941955566\",
            \"locationLongitude\": \"-111.848297119\",
            \"distributionChannel\": \"anonymous\",
            \"userLanguage\": \"EN\",
            \"QID1\": 3,
            \"QID1_DO\": [
                \"1\",
                \"2\",
                \"3\",
                \"4\"
            ]
        },
        \"labels\": {
            \"status\": \"IP Address\",
            \"finished\": \"True\",
            \"QID1\": \"Cookies & Cream\",
            \"QID1_DO\": [
                \"Chocolate\",
                \"Vanilla\",
                \"Cookies & Cream\",
                \"Strawberry\"
            ]
        },
        \"displayedFields\": [
            \"QID1\"
        ],
        \"displayedValues\": {
            \"QID1\": [
                1,
                2,
                3,
                4
            ]
        }
    }
    ```

    Now, let's look at the pieces of the schema to understand them a little better. Note: this
    documentation won't attempt to cover all the aspects of the JSON Schema specification, for more
    information see [https://json-schema.org/](https://json-schema.org/).

    ```json
    {
        \"$schema\": \"https://json-schema.org/draft/2019-09/schema\",
        \"$id\": \"http://qualtrics.com/API/v3/surveys/SV_ai71yqu2ZLvpadf/response-schema\",
        \"title\": \"JSON Schema Example (SV_ai71yqu2ZLvpadf) - Survey Response\",
        \"description\": \"This is a schema for survey responses from SV_ai71yqu2ZLvpadf\",
        \"type\": \"object\",
    ```

    The schema starts with several standard fields from the Json Schema specification. The value for
    `$schema` is explained [here](https://json-schema.org/draft/2019-09/json-schema-
    core.html#rfc.section.8.1.1) and the value for `$id` is explained [here](https://json-
    schema.org/draft/2019-09/json-schema-core.html#id-keyword). Then, the schema is given a title and a
    description. Finally, the schema is defined for a JSON [object](https://json-
    schema.org/draft/2019-09/json-schema-core.html#rfc.section.4.2.1) primitive type.

    ```json
        \"required\": [
            \"values\",
            \"displayedFields\",
            \"displayedValues\",
            \"labels\",
            \"responseId\"
        ],
    ```

    Next, the `required` field specifies that our JSON `object` will have the certain required fields.
    Looking back at our example response, we see that each of these fields is present.

    ```json
        \"properties\": {
            \"responseId\": {
                \"type\": \"string\"
            },
    ```

    Inside of the `properties` object, each field previously mentioned in the `required` array are given
    a schema. The simplest of these fields is the responseId field which will just be provided as a
    string.

    ```json
            \"displayedFields\": {
                \"type\": \"array\",
                \"description\": \"A list of questions or question rows that were displayed to the
    survey respondent\",
                \"items\": {
                    \"type\": \"string\"
                }
            },
            \"displayedValues\": {
                \"type\": \"object\",
                \"description\": \"A list of the possible answers shown to the survey respondent for
    each question or question row\",
                \"additionalProperties\": {
                    \"type\": \"array\"
                }
            },
            \"labels\": {
                \"type\": \"object\",
                \"description\": \"The labels of the answers given by the survey respondent for each
    question or question row\",
                \"additionalProperties\": true
            },
    ```

    The next fields `displayedFields`, `displayedValues`, and `labels` have descriptions built in to the
    schema. Again, we can see how these schemas translate into a response object by consulting our
    example.

    ```json
            \"values\": {
                \"type\": \"object\",
                \"description\": \"The answers given by the survey respondent\",
                \"properties\": {
                    \"QID1\": {
                        \"description\": \"Which type of Ice Cream is your favorite?\",
                        \"dataType\": \"question\",
                        \"type\": \"number\",
                        \"oneOf\": [
                            {
                                \"label\": \"Chocolate\",
                                \"const\": 1
                            },
                            {
                                \"label\": \"Vanilla\",
                                \"const\": 2
                            },
                            {
                                \"label\": \"Cookies & Cream\",
                                \"const\": 3
                            },
                            {
                                \"label\": \"Strawberry\",
                                \"const\": 4
                            }
                        ],
                        \"exportTag\": \"Q1\",
                        \"questionId\": \"QID1\"
                    },
                    \"recordedDate\": {
                        \"description\": \"Recorded Date\",
                        \"dataType\": \"metadata\",
                        \"type\": \"string\",
                        \"format\": \"date-time\",
                        \"exportTag\": \"RecordedDate\"
                    },
                    \"duration\": {
                        \"description\": \"Duration (in seconds)\",
                        \"dataType\": \"metadata\",
                        \"type\": \"number\",
                        \"exportTag\": \"Duration (in seconds)\"
                    },
    ```

    Finally, the values property defines the schema for each value available in the response. I've
    pulled a couple of the fields from the schema into this documentation but we can see from the
    example response that there are many more fields in this schema. Here we can see a `description` for
    each field as well as a `type` and several other pieces of information. We can see that the `type`
    matches up with the JSON data type for each value as found in the example response. The `dataType`
    can be used to know the source for that value and the `exportTag` is useful for understanding the
    header columns when using the [Create Response
    Export](./responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-responses/post) endpoint
    with the CSV or TSV formats. Lastly, oneOf enumerates the possible options for values that have a
    known, finite domain. For this example, a multiple choice question would have a oneOf field since
    there are only 4 possible values. However, a text entry field that only allows numbers would not
    have a oneOf field, since the domain can't be enumerated.

    ## Additional Tooling for JSON Schemas

    One of the benefits of having a schema is that it can be used to automate some of the parsing and
    usage of json schemas. One such tool for automating this step is
    [Quicktype](https://app.quicktype.io/#l=schema). More information about that tool can be found on
    [Github](https://github.com/quicktype/quicktype).


    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]]:
    r"""Retrieve Survey JSON Schema

     ## Introduction

    This documentation is meant to help explain the purpose and value of the Retrieve the JSON Schema
    endpoint in the public api. In short, this endpoint provides a [standard JSON Schema](https://json-
    schema.org/) that can be used for parsing the results from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint
    and the [Create Response Export](./legacyResponseImportsExports.json/paths/~1responseexports/post)
    endpoint when exporting in the json format. Finally this endpoint can also be useful for preparing
    responses for the [Create a New
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses/post) endpoint.

    # Example

    Note, before reading through this example, it might be helpful to take a quick detour and gain a bit
    of familiarity around Json Schemas.
    For this example we created a simple survey with a single multiple choice question `Which type of
    Ice Cream is your favorite?` and 4 options `Chocolate`, `Vanilla`, `Cookies & Cream`, and
    `Strawberry`.
    Here's an example response that we requested from the [Retrieve a Survey
    Response](./singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{responseId}/get) endpoint:

    ```json
    {
        \"responseId\": \"R_240YEnuWbbwZOy1\",
        \"values\": {
            \"startDate\": \"2020-05-13T19:26:15Z\",
            \"endDate\": \"2020-05-13T19:26:18Z\",
            \"status\": 0,
            \"ipAddress\": \"70.103.180.85\",
            \"progress\": 100,
            \"duration\": 2,
            \"finished\": 1,
            \"recordedDate\": \"2020-05-13T19:26:18.487Z\",
            \"locationLatitude\": \"40.3941955566\",
            \"locationLongitude\": \"-111.848297119\",
            \"distributionChannel\": \"anonymous\",
            \"userLanguage\": \"EN\",
            \"QID1\": 3,
            \"QID1_DO\": [
                \"1\",
                \"2\",
                \"3\",
                \"4\"
            ]
        },
        \"labels\": {
            \"status\": \"IP Address\",
            \"finished\": \"True\",
            \"QID1\": \"Cookies & Cream\",
            \"QID1_DO\": [
                \"Chocolate\",
                \"Vanilla\",
                \"Cookies & Cream\",
                \"Strawberry\"
            ]
        },
        \"displayedFields\": [
            \"QID1\"
        ],
        \"displayedValues\": {
            \"QID1\": [
                1,
                2,
                3,
                4
            ]
        }
    }
    ```

    Now, let's look at the pieces of the schema to understand them a little better. Note: this
    documentation won't attempt to cover all the aspects of the JSON Schema specification, for more
    information see [https://json-schema.org/](https://json-schema.org/).

    ```json
    {
        \"$schema\": \"https://json-schema.org/draft/2019-09/schema\",
        \"$id\": \"http://qualtrics.com/API/v3/surveys/SV_ai71yqu2ZLvpadf/response-schema\",
        \"title\": \"JSON Schema Example (SV_ai71yqu2ZLvpadf) - Survey Response\",
        \"description\": \"This is a schema for survey responses from SV_ai71yqu2ZLvpadf\",
        \"type\": \"object\",
    ```

    The schema starts with several standard fields from the Json Schema specification. The value for
    `$schema` is explained [here](https://json-schema.org/draft/2019-09/json-schema-
    core.html#rfc.section.8.1.1) and the value for `$id` is explained [here](https://json-
    schema.org/draft/2019-09/json-schema-core.html#id-keyword). Then, the schema is given a title and a
    description. Finally, the schema is defined for a JSON [object](https://json-
    schema.org/draft/2019-09/json-schema-core.html#rfc.section.4.2.1) primitive type.

    ```json
        \"required\": [
            \"values\",
            \"displayedFields\",
            \"displayedValues\",
            \"labels\",
            \"responseId\"
        ],
    ```

    Next, the `required` field specifies that our JSON `object` will have the certain required fields.
    Looking back at our example response, we see that each of these fields is present.

    ```json
        \"properties\": {
            \"responseId\": {
                \"type\": \"string\"
            },
    ```

    Inside of the `properties` object, each field previously mentioned in the `required` array are given
    a schema. The simplest of these fields is the responseId field which will just be provided as a
    string.

    ```json
            \"displayedFields\": {
                \"type\": \"array\",
                \"description\": \"A list of questions or question rows that were displayed to the
    survey respondent\",
                \"items\": {
                    \"type\": \"string\"
                }
            },
            \"displayedValues\": {
                \"type\": \"object\",
                \"description\": \"A list of the possible answers shown to the survey respondent for
    each question or question row\",
                \"additionalProperties\": {
                    \"type\": \"array\"
                }
            },
            \"labels\": {
                \"type\": \"object\",
                \"description\": \"The labels of the answers given by the survey respondent for each
    question or question row\",
                \"additionalProperties\": true
            },
    ```

    The next fields `displayedFields`, `displayedValues`, and `labels` have descriptions built in to the
    schema. Again, we can see how these schemas translate into a response object by consulting our
    example.

    ```json
            \"values\": {
                \"type\": \"object\",
                \"description\": \"The answers given by the survey respondent\",
                \"properties\": {
                    \"QID1\": {
                        \"description\": \"Which type of Ice Cream is your favorite?\",
                        \"dataType\": \"question\",
                        \"type\": \"number\",
                        \"oneOf\": [
                            {
                                \"label\": \"Chocolate\",
                                \"const\": 1
                            },
                            {
                                \"label\": \"Vanilla\",
                                \"const\": 2
                            },
                            {
                                \"label\": \"Cookies & Cream\",
                                \"const\": 3
                            },
                            {
                                \"label\": \"Strawberry\",
                                \"const\": 4
                            }
                        ],
                        \"exportTag\": \"Q1\",
                        \"questionId\": \"QID1\"
                    },
                    \"recordedDate\": {
                        \"description\": \"Recorded Date\",
                        \"dataType\": \"metadata\",
                        \"type\": \"string\",
                        \"format\": \"date-time\",
                        \"exportTag\": \"RecordedDate\"
                    },
                    \"duration\": {
                        \"description\": \"Duration (in seconds)\",
                        \"dataType\": \"metadata\",
                        \"type\": \"number\",
                        \"exportTag\": \"Duration (in seconds)\"
                    },
    ```

    Finally, the values property defines the schema for each value available in the response. I've
    pulled a couple of the fields from the schema into this documentation but we can see from the
    example response that there are many more fields in this schema. Here we can see a `description` for
    each field as well as a `type` and several other pieces of information. We can see that the `type`
    matches up with the JSON data type for each value as found in the example response. The `dataType`
    can be used to know the source for that value and the `exportTag` is useful for understanding the
    header columns when using the [Create Response
    Export](./responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-responses/post) endpoint
    with the CSV or TSV formats. Lastly, oneOf enumerates the possible options for values that have a
    known, finite domain. For this example, a multiple choice question would have a oneOf field since
    there are only 4 possible values. However, a text entry field that only allows numbers would not
    have a oneOf field, since the domain can't be enumerated.

    ## Additional Tooling for JSON Schemas

    One of the benefits of having a schema is that it can be used to automate some of the parsing and
    usage of json schemas. One such tool for automating this step is
    [Quicktype](https://app.quicktype.io/#l=schema). More information about that tool can be found on
    [Github](https://github.com/quicktype/quicktype).


    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, GetSchemaResponse, SurveyNotFoundResponse]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
        )
    ).parsed
