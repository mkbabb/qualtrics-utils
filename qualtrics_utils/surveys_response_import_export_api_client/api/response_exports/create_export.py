from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.creation_response import CreationResponse
from ...models.export_creation_request import ExportCreationRequest
from ...models.meta import Meta
from ...models.survey_not_found import SurveyNotFound
from ...types import Response


def _get_kwargs(
    survey_id: str,
    *,
    json_body: ExportCreationRequest,
) -> Dict[str, Any]:

    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/surveys/{surveyId}/export-responses".format(
            surveyId=survey_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreationResponse, Meta, SurveyNotFound]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreationResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Meta.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = SurveyNotFound.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreationResponse, Meta, SurveyNotFound]]:
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
    json_body: ExportCreationRequest,
) -> Response[Union[CreationResponse, Meta, SurveyNotFound]]:
    """Start Response Export

     Starts an export of a survey's responses. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within a workflow.

    This page will provide additional details and things you should know about this endpoint.

    <!-- theme: danger -->
    > ### If this call doesn't return an HTTP 200 status code, do not start polling for progress.

    <!-- theme: warning -->
    >### Max File Size
    >Currently, response exports exceeding 1.8 GB will fail. To prevent your export from failing, use
    proper limits and filters to limit the size of your final export file.

    <!-- theme: warning -->
    >### Invalid Parameters with JSON and NDJSON
    >When exporting responses as JSON, not all parameters are meaningful. Consequently, the following
    parameters are not allowed when starting a JSON or NDJSON export:
    >
    >`includeDisplayOrder`
    >`useLabels`
    >`formatDecimalAsComma`
    >`seenUnansweredRecode`
    >`multiselectSeenUnansweredRecode`
    >`timeZone`
    >`newlineReplacement`
    >`breakoutSets`


    Args:
        survey_id (str):
        json_body (ExportCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreationResponse, Meta, SurveyNotFound]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ExportCreationRequest,
) -> Optional[Union[CreationResponse, Meta, SurveyNotFound]]:
    """Start Response Export

     Starts an export of a survey's responses. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within a workflow.

    This page will provide additional details and things you should know about this endpoint.

    <!-- theme: danger -->
    > ### If this call doesn't return an HTTP 200 status code, do not start polling for progress.

    <!-- theme: warning -->
    >### Max File Size
    >Currently, response exports exceeding 1.8 GB will fail. To prevent your export from failing, use
    proper limits and filters to limit the size of your final export file.

    <!-- theme: warning -->
    >### Invalid Parameters with JSON and NDJSON
    >When exporting responses as JSON, not all parameters are meaningful. Consequently, the following
    parameters are not allowed when starting a JSON or NDJSON export:
    >
    >`includeDisplayOrder`
    >`useLabels`
    >`formatDecimalAsComma`
    >`seenUnansweredRecode`
    >`multiselectSeenUnansweredRecode`
    >`timeZone`
    >`newlineReplacement`
    >`breakoutSets`


    Args:
        survey_id (str):
        json_body (ExportCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreationResponse, Meta, SurveyNotFound]
    """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ExportCreationRequest,
) -> Response[Union[CreationResponse, Meta, SurveyNotFound]]:
    """Start Response Export

     Starts an export of a survey's responses. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within a workflow.

    This page will provide additional details and things you should know about this endpoint.

    <!-- theme: danger -->
    > ### If this call doesn't return an HTTP 200 status code, do not start polling for progress.

    <!-- theme: warning -->
    >### Max File Size
    >Currently, response exports exceeding 1.8 GB will fail. To prevent your export from failing, use
    proper limits and filters to limit the size of your final export file.

    <!-- theme: warning -->
    >### Invalid Parameters with JSON and NDJSON
    >When exporting responses as JSON, not all parameters are meaningful. Consequently, the following
    parameters are not allowed when starting a JSON or NDJSON export:
    >
    >`includeDisplayOrder`
    >`useLabels`
    >`formatDecimalAsComma`
    >`seenUnansweredRecode`
    >`multiselectSeenUnansweredRecode`
    >`timeZone`
    >`newlineReplacement`
    >`breakoutSets`


    Args:
        survey_id (str):
        json_body (ExportCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreationResponse, Meta, SurveyNotFound]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ExportCreationRequest,
) -> Optional[Union[CreationResponse, Meta, SurveyNotFound]]:
    """Start Response Export

     Starts an export of a survey's responses. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within a workflow.

    This page will provide additional details and things you should know about this endpoint.

    <!-- theme: danger -->
    > ### If this call doesn't return an HTTP 200 status code, do not start polling for progress.

    <!-- theme: warning -->
    >### Max File Size
    >Currently, response exports exceeding 1.8 GB will fail. To prevent your export from failing, use
    proper limits and filters to limit the size of your final export file.

    <!-- theme: warning -->
    >### Invalid Parameters with JSON and NDJSON
    >When exporting responses as JSON, not all parameters are meaningful. Consequently, the following
    parameters are not allowed when starting a JSON or NDJSON export:
    >
    >`includeDisplayOrder`
    >`useLabels`
    >`formatDecimalAsComma`
    >`seenUnansweredRecode`
    >`multiselectSeenUnansweredRecode`
    >`timeZone`
    >`newlineReplacement`
    >`breakoutSets`


    Args:
        survey_id (str):
        json_body (ExportCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreationResponse, Meta, SurveyNotFound]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
