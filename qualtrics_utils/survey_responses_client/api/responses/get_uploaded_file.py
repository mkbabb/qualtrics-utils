from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.default_error_response import DefaultErrorResponse
from ...models.survey_not_found_response import SurveyNotFoundResponse
from ...types import Response


def _get_kwargs(
    survey_id: str,
    response_id: str,
    file_id: str,
) -> Dict[str, Any]:

    pass

    return {
        "method": "get",
        "url": "/surveys/{surveyId}/responses/{responseId}/uploaded-files/{fileId}".format(
            surveyId=survey_id,
            responseId=response_id,
            fileId=file_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultErrorResponse, SurveyNotFoundResponse]]:
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
) -> Response[Union[DefaultErrorResponse, SurveyNotFoundResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    response_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DefaultErrorResponse, SurveyNotFoundResponse]]:
    """Retrieve a User-Uploaded File

     Retrieves a file uploaded by a survey respondent for a file upload question.

    <!-- theme: info -->

    > #### Default Server Timeout is 100 Seconds
    >
    > To accommodate retrieval of large file sizes, the default server timeout is 100 seconds for this
    endpoint.

    Args:
        survey_id (str):
        response_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        response_id=response_id,
        file_id=file_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    response_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DefaultErrorResponse, SurveyNotFoundResponse]]:
    """Retrieve a User-Uploaded File

     Retrieves a file uploaded by a survey respondent for a file upload question.

    <!-- theme: info -->

    > #### Default Server Timeout is 100 Seconds
    >
    > To accommodate retrieval of large file sizes, the default server timeout is 100 seconds for this
    endpoint.

    Args:
        survey_id (str):
        response_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, SurveyNotFoundResponse]
    """

    return sync_detailed(
        survey_id=survey_id,
        response_id=response_id,
        file_id=file_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    response_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DefaultErrorResponse, SurveyNotFoundResponse]]:
    """Retrieve a User-Uploaded File

     Retrieves a file uploaded by a survey respondent for a file upload question.

    <!-- theme: info -->

    > #### Default Server Timeout is 100 Seconds
    >
    > To accommodate retrieval of large file sizes, the default server timeout is 100 seconds for this
    endpoint.

    Args:
        survey_id (str):
        response_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        response_id=response_id,
        file_id=file_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    response_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DefaultErrorResponse, SurveyNotFoundResponse]]:
    """Retrieve a User-Uploaded File

     Retrieves a file uploaded by a survey respondent for a file upload question.

    <!-- theme: info -->

    > #### Default Server Timeout is 100 Seconds
    >
    > To accommodate retrieval of large file sizes, the default server timeout is 100 seconds for this
    endpoint.

    Args:
        survey_id (str):
        response_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, SurveyNotFoundResponse]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            response_id=response_id,
            file_id=file_id,
            client=client,
        )
    ).parsed
