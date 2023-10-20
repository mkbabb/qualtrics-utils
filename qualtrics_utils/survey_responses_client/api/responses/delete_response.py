from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.default_error_response import DefaultErrorResponse
from ...models.delete_response_response import DeleteResponseResponse
from ...models.survey_not_found_response import SurveyNotFoundResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    survey_id: str,
    response_id: str,
    *,
    decrement_quotas: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:

    pass

    params: Dict[str, Any] = {}
    params["decrementQuotas"] = decrement_quotas

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": "/surveys/{surveyId}/responses/{responseId}".format(
            surveyId=survey_id,
            responseId=response_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteResponseResponse.from_dict(response.json())

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
) -> Response[
    Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
    decrement_quotas: Union[Unset, None, bool] = False,
) -> Response[
    Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
]:
    """Delete a Survey Response

     Deletes a single survey response

    Args:
        survey_id (str):
        response_id (str):
        decrement_quotas (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        response_id=response_id,
        decrement_quotas=decrement_quotas,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
    decrement_quotas: Union[Unset, None, bool] = False,
) -> Optional[
    Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
]:
    """Delete a Survey Response

     Deletes a single survey response

    Args:
        survey_id (str):
        response_id (str):
        decrement_quotas (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
    """

    return sync_detailed(
        survey_id=survey_id,
        response_id=response_id,
        client=client,
        decrement_quotas=decrement_quotas,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
    decrement_quotas: Union[Unset, None, bool] = False,
) -> Response[
    Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
]:
    """Delete a Survey Response

     Deletes a single survey response

    Args:
        survey_id (str):
        response_id (str):
        decrement_quotas (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        response_id=response_id,
        decrement_quotas=decrement_quotas,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
    decrement_quotas: Union[Unset, None, bool] = False,
) -> Optional[
    Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
]:
    """Delete a Survey Response

     Deletes a single survey response

    Args:
        survey_id (str):
        response_id (str):
        decrement_quotas (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultErrorResponse, DeleteResponseResponse, SurveyNotFoundResponse]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            response_id=response_id,
            client=client,
            decrement_quotas=decrement_quotas,
        )
    ).parsed
