from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_filters_list_response import GetFiltersListResponse
from ...models.survey_not_found import SurveyNotFound
from ...types import Response


def _get_kwargs(
    survey_id: str,
) -> Dict[str, Any]:

    pass

    return {
        "method": "get",
        "url": "/surveys/{surveyId}/filters".format(
            surveyId=survey_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetFiltersListResponse, SurveyNotFound]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetFiltersListResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = SurveyNotFound.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetFiltersListResponse, SurveyNotFound]]:
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
) -> Response[Union[GetFiltersListResponse, SurveyNotFound]]:
    """Get List of Available Filters

     Gets a list of the available filters for the given survey. Filters are survey specific, and can only
    be set up via the Qualtrics web page for your brand. You can find more information on how to add
    filters at the [Filtering Responses](https://www.qualtrics.com/support/survey-platform/data-and-
    analysis-module/data/filtering-responses/) support page.

    The most important field in the response you get from this call are the returned filterIds. You can
    use these to narrow your exports to responses that fit conditions of your choice.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetFiltersListResponse, SurveyNotFound]]
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
) -> Optional[Union[GetFiltersListResponse, SurveyNotFound]]:
    """Get List of Available Filters

     Gets a list of the available filters for the given survey. Filters are survey specific, and can only
    be set up via the Qualtrics web page for your brand. You can find more information on how to add
    filters at the [Filtering Responses](https://www.qualtrics.com/support/survey-platform/data-and-
    analysis-module/data/filtering-responses/) support page.

    The most important field in the response you get from this call are the returned filterIds. You can
    use these to narrow your exports to responses that fit conditions of your choice.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetFiltersListResponse, SurveyNotFound]
    """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetFiltersListResponse, SurveyNotFound]]:
    """Get List of Available Filters

     Gets a list of the available filters for the given survey. Filters are survey specific, and can only
    be set up via the Qualtrics web page for your brand. You can find more information on how to add
    filters at the [Filtering Responses](https://www.qualtrics.com/support/survey-platform/data-and-
    analysis-module/data/filtering-responses/) support page.

    The most important field in the response you get from this call are the returned filterIds. You can
    use these to narrow your exports to responses that fit conditions of your choice.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetFiltersListResponse, SurveyNotFound]]
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
) -> Optional[Union[GetFiltersListResponse, SurveyNotFound]]:
    """Get List of Available Filters

     Gets a list of the available filters for the given survey. Filters are survey specific, and can only
    be set up via the Qualtrics web page for your brand. You can find more information on how to add
    filters at the [Filtering Responses](https://www.qualtrics.com/support/survey-platform/data-and-
    analysis-module/data/filtering-responses/) support page.

    The most important field in the response you get from this call are the returned filterIds. You can
    use these to narrow your exports to responses that fit conditions of your choice.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetFiltersListResponse, SurveyNotFound]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
        )
    ).parsed
