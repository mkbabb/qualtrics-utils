from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_response_request import CreateResponseRequest
from ...models.create_response_response import CreateResponseResponse
from ...models.create_response_with_file_attachments_request import (
    CreateResponseWithFileAttachmentsRequest,
)
from ...models.default_error_response import DefaultErrorResponse
from ...models.survey_not_found_response import SurveyNotFoundResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    survey_id: str,
    *,
    multipart_data: CreateResponseWithFileAttachmentsRequest,
    json_body: CreateResponseRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    json_body.to_dict()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/surveys/{surveyId}/responses".format(
            surveyId=survey_id,
        ),
        "files": multipart_multipart_data,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateResponseResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DefaultErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = DefaultErrorResponse.from_dict(response.json())

        return response_401
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
) -> Response[
    Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
]:
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
    multipart_data: CreateResponseWithFileAttachmentsRequest,
    json_body: CreateResponseRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
]:
    r"""Create a New Response

     <!--From Readme-->
    <!-- theme: info -->

    >### Import Response Format
    >The fields in `values` depend on the survey definition. The easiest way to find this format is to
    perform a get a single response call for the survey which you are trying import values for [Retrieve
    a Survey Response](../reference/singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{respon
    seId}/get). The result of that call will demonstrate the format for the Create a New Response Call.


    <!--From Readme-->
    <!-- theme: info -->

    >### Uploading Files for File Upload Questions
    >Files can be included in your import to be associated with file upload questions in your survey.
    Select `multipart/form-data` as the request type in the documentation below to see the full request
    format.
    >
    >`multipart/form-data` requests allow you to send multiple different entities as body parts in a
    single request. We can use this to create a request to upload a survey response with file
    attachments. A minimum of two body parts are required in addition to the files you wish to upload.
    >1. `response`: This body part is the JSON representation of the survey response. As with the
    regular `application/json` POST request for this endpoint, the minimum required object is
    `{\"values\": {}}`. Note that you do not need to include any file metadata in the survey response as
    the necessary metadata will automatically be added to the response from the files that you upload
    with it.
    >1. `fileMapping`: This body part is also a JSON object. Its purpose is to tell the importer which
    files go with which questions in your survey. E.g. if we wanted to import a file with the body part
    key of `file1` and we wanted that file to be associated with the file upload question `QID1`, our
    `fileMapping` object would be `{\"file1\": \"QID1\"}`.
    >For the remainder of your request you can attach up to five files. Each file must have a body part
    key of `file1`, `file2`, `file3`, `file4`, or `file5`.


    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):
        multipart_data (CreateResponseWithFileAttachmentsRequest):
        json_body (CreateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        multipart_data=multipart_data,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    multipart_data: CreateResponseWithFileAttachmentsRequest,
    json_body: CreateResponseRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
]:
    r"""Create a New Response

     <!--From Readme-->
    <!-- theme: info -->

    >### Import Response Format
    >The fields in `values` depend on the survey definition. The easiest way to find this format is to
    perform a get a single response call for the survey which you are trying import values for [Retrieve
    a Survey Response](../reference/singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{respon
    seId}/get). The result of that call will demonstrate the format for the Create a New Response Call.


    <!--From Readme-->
    <!-- theme: info -->

    >### Uploading Files for File Upload Questions
    >Files can be included in your import to be associated with file upload questions in your survey.
    Select `multipart/form-data` as the request type in the documentation below to see the full request
    format.
    >
    >`multipart/form-data` requests allow you to send multiple different entities as body parts in a
    single request. We can use this to create a request to upload a survey response with file
    attachments. A minimum of two body parts are required in addition to the files you wish to upload.
    >1. `response`: This body part is the JSON representation of the survey response. As with the
    regular `application/json` POST request for this endpoint, the minimum required object is
    `{\"values\": {}}`. Note that you do not need to include any file metadata in the survey response as
    the necessary metadata will automatically be added to the response from the files that you upload
    with it.
    >1. `fileMapping`: This body part is also a JSON object. Its purpose is to tell the importer which
    files go with which questions in your survey. E.g. if we wanted to import a file with the body part
    key of `file1` and we wanted that file to be associated with the file upload question `QID1`, our
    `fileMapping` object would be `{\"file1\": \"QID1\"}`.
    >For the remainder of your request you can attach up to five files. Each file must have a body part
    key of `file1`, `file2`, `file3`, `file4`, or `file5`.


    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):
        multipart_data (CreateResponseWithFileAttachmentsRequest):
        json_body (CreateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
    """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
        multipart_data=multipart_data,
        json_body=json_body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    multipart_data: CreateResponseWithFileAttachmentsRequest,
    json_body: CreateResponseRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
]:
    r"""Create a New Response

     <!--From Readme-->
    <!-- theme: info -->

    >### Import Response Format
    >The fields in `values` depend on the survey definition. The easiest way to find this format is to
    perform a get a single response call for the survey which you are trying import values for [Retrieve
    a Survey Response](../reference/singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{respon
    seId}/get). The result of that call will demonstrate the format for the Create a New Response Call.


    <!--From Readme-->
    <!-- theme: info -->

    >### Uploading Files for File Upload Questions
    >Files can be included in your import to be associated with file upload questions in your survey.
    Select `multipart/form-data` as the request type in the documentation below to see the full request
    format.
    >
    >`multipart/form-data` requests allow you to send multiple different entities as body parts in a
    single request. We can use this to create a request to upload a survey response with file
    attachments. A minimum of two body parts are required in addition to the files you wish to upload.
    >1. `response`: This body part is the JSON representation of the survey response. As with the
    regular `application/json` POST request for this endpoint, the minimum required object is
    `{\"values\": {}}`. Note that you do not need to include any file metadata in the survey response as
    the necessary metadata will automatically be added to the response from the files that you upload
    with it.
    >1. `fileMapping`: This body part is also a JSON object. Its purpose is to tell the importer which
    files go with which questions in your survey. E.g. if we wanted to import a file with the body part
    key of `file1` and we wanted that file to be associated with the file upload question `QID1`, our
    `fileMapping` object would be `{\"file1\": \"QID1\"}`.
    >For the remainder of your request you can attach up to five files. Each file must have a body part
    key of `file1`, `file2`, `file3`, `file4`, or `file5`.


    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):
        multipart_data (CreateResponseWithFileAttachmentsRequest):
        json_body (CreateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        multipart_data=multipart_data,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    multipart_data: CreateResponseWithFileAttachmentsRequest,
    json_body: CreateResponseRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
]:
    r"""Create a New Response

     <!--From Readme-->
    <!-- theme: info -->

    >### Import Response Format
    >The fields in `values` depend on the survey definition. The easiest way to find this format is to
    perform a get a single response call for the survey which you are trying import values for [Retrieve
    a Survey Response](../reference/singleResponses.json/paths/~1surveys~1{surveyId}~1responses~1{respon
    seId}/get). The result of that call will demonstrate the format for the Create a New Response Call.


    <!--From Readme-->
    <!-- theme: info -->

    >### Uploading Files for File Upload Questions
    >Files can be included in your import to be associated with file upload questions in your survey.
    Select `multipart/form-data` as the request type in the documentation below to see the full request
    format.
    >
    >`multipart/form-data` requests allow you to send multiple different entities as body parts in a
    single request. We can use this to create a request to upload a survey response with file
    attachments. A minimum of two body parts are required in addition to the files you wish to upload.
    >1. `response`: This body part is the JSON representation of the survey response. As with the
    regular `application/json` POST request for this endpoint, the minimum required object is
    `{\"values\": {}}`. Note that you do not need to include any file metadata in the survey response as
    the necessary metadata will automatically be added to the response from the files that you upload
    with it.
    >1. `fileMapping`: This body part is also a JSON object. Its purpose is to tell the importer which
    files go with which questions in your survey. E.g. if we wanted to import a file with the body part
    key of `file1` and we wanted that file to be associated with the file upload question `QID1`, our
    `fileMapping` object would be `{\"file1\": \"QID1\"}`.
    >For the remainder of your request you can attach up to five files. Each file must have a body part
    key of `file1`, `file2`, `file3`, `file4`, or `file5`.


    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):
        multipart_data (CreateResponseWithFileAttachmentsRequest):
        json_body (CreateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateResponseResponse, DefaultErrorResponse, SurveyNotFoundResponse]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
            multipart_data=multipart_data,
            json_body=json_body,
            idempotency_key=idempotency_key,
        )
    ).parsed
