from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.default_error_response import DefaultErrorResponse
from ...models.survey_unauthorized_response import SurveyUnauthorizedResponse
from ...models.update_response_request import UpdateResponseRequest
from ...models.update_response_response import UpdateResponseResponse
from ...types import Response


def _get_kwargs(
    response_id: str,
    *,
    json_body: UpdateResponseRequest,
) -> Dict[str, Any]:

    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/responses/{responseId}".format(
            responseId=response_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateResponseResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DefaultErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = SurveyUnauthorizedResponse.from_dict(response.json())

        return response_401
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
    Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    response_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateResponseRequest,
) -> Response[
    Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
]:
    """Update Response

     Update embedded data on a survey response
     Embedded data fields [edited in the Data & Analysis tab](https://www.qualtrics.com/support/survey-
    platform/data-and-analysis-module/data/response-editing/) are stored in a separate database from the
    raw responses. Updates stored in this separate edits database will always override the raw value.
    The public update embedded data API only updates the raw response, therefore any updates made via
    this API will not show up if the field has been edited via Data & Analysis. The update will still
    successfully update the raw response and return a 200; however, the edit made from Data & Analysis
    [will need to be removed](https://www.qualtrics.com/support/survey-platform/data-and-analysis-
    module/data/response-editing/#RestoringOriginalData) before your value made via this API are
    visible.

    <!-- theme: info -->
    > ### Changes Viewable Only for Fields in Survey Flow
    > Updates to embedded data are only viewable for fields set in your survey flow. Updates to fields
    not in the flow will still be added to your survey responses, but will be hidden until you update
    your survey.

    Args:
        response_id (str):
        json_body (UpdateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]]
    """

    kwargs = _get_kwargs(
        response_id=response_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    response_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateResponseRequest,
) -> Optional[
    Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
]:
    """Update Response

     Update embedded data on a survey response
     Embedded data fields [edited in the Data & Analysis tab](https://www.qualtrics.com/support/survey-
    platform/data-and-analysis-module/data/response-editing/) are stored in a separate database from the
    raw responses. Updates stored in this separate edits database will always override the raw value.
    The public update embedded data API only updates the raw response, therefore any updates made via
    this API will not show up if the field has been edited via Data & Analysis. The update will still
    successfully update the raw response and return a 200; however, the edit made from Data & Analysis
    [will need to be removed](https://www.qualtrics.com/support/survey-platform/data-and-analysis-
    module/data/response-editing/#RestoringOriginalData) before your value made via this API are
    visible.

    <!-- theme: info -->
    > ### Changes Viewable Only for Fields in Survey Flow
    > Updates to embedded data are only viewable for fields set in your survey flow. Updates to fields
    not in the flow will still be added to your survey responses, but will be hidden until you update
    your survey.

    Args:
        response_id (str):
        json_body (UpdateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
    """

    return sync_detailed(
        response_id=response_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    response_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateResponseRequest,
) -> Response[
    Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
]:
    """Update Response

     Update embedded data on a survey response
     Embedded data fields [edited in the Data & Analysis tab](https://www.qualtrics.com/support/survey-
    platform/data-and-analysis-module/data/response-editing/) are stored in a separate database from the
    raw responses. Updates stored in this separate edits database will always override the raw value.
    The public update embedded data API only updates the raw response, therefore any updates made via
    this API will not show up if the field has been edited via Data & Analysis. The update will still
    successfully update the raw response and return a 200; however, the edit made from Data & Analysis
    [will need to be removed](https://www.qualtrics.com/support/survey-platform/data-and-analysis-
    module/data/response-editing/#RestoringOriginalData) before your value made via this API are
    visible.

    <!-- theme: info -->
    > ### Changes Viewable Only for Fields in Survey Flow
    > Updates to embedded data are only viewable for fields set in your survey flow. Updates to fields
    not in the flow will still be added to your survey responses, but will be hidden until you update
    your survey.

    Args:
        response_id (str):
        json_body (UpdateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]]
    """

    kwargs = _get_kwargs(
        response_id=response_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    response_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdateResponseRequest,
) -> Optional[
    Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
]:
    """Update Response

     Update embedded data on a survey response
     Embedded data fields [edited in the Data & Analysis tab](https://www.qualtrics.com/support/survey-
    platform/data-and-analysis-module/data/response-editing/) are stored in a separate database from the
    raw responses. Updates stored in this separate edits database will always override the raw value.
    The public update embedded data API only updates the raw response, therefore any updates made via
    this API will not show up if the field has been edited via Data & Analysis. The update will still
    successfully update the raw response and return a 200; however, the edit made from Data & Analysis
    [will need to be removed](https://www.qualtrics.com/support/survey-platform/data-and-analysis-
    module/data/response-editing/#RestoringOriginalData) before your value made via this API are
    visible.

    <!-- theme: info -->
    > ### Changes Viewable Only for Fields in Survey Flow
    > Updates to embedded data are only viewable for fields set in your survey flow. Updates to fields
    not in the flow will still be added to your survey responses, but will be hidden until you update
    your survey.

    Args:
        response_id (str):
        json_body (UpdateResponseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, SurveyUnauthorizedResponse, UpdateResponseResponse]
    """

    return (
        await asyncio_detailed(
            response_id=response_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
