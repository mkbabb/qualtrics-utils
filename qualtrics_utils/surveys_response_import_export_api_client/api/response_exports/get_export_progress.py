from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_status_response import ExportStatusResponse
from ...models.meta import Meta
from ...types import Response


def _get_kwargs(
    survey_id: str,
    export_progress_id: str,
) -> Dict[str, Any]:

    pass

    return {
        "method": "get",
        "url": "/surveys/{surveyId}/export-responses/{exportProgressId}".format(
            surveyId=survey_id,
            exportProgressId=export_progress_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ExportStatusResponse, Meta]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExportStatusResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Meta.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ExportStatusResponse, Meta]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    export_progress_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ExportStatusResponse, Meta]]:
    r"""Get Response Export Progress

     Retrieves the status of a response export for the given `exportProgressId`. Please note you will
    find the `exportProgressId` in the Export Responses POST response in the `progressId` field.

    If you receive a status of `failed`, record your `requestId` and try your export again. Contact
    support with your `requestId` and date and time of the call to troubleshoot.

    <!-- theme: danger -->
    > ### Before calling this API, make sure your `exportProgressId` is not null.
    > You could end up in an infinite loop if you don't code this properly. Please check for null before
    making this call. Also check for a 404 response and stop polling if you receive one.

    <!-- theme: info -->
    >### `percentComplete` Field
    >Please note the percentComplete field is a convenience field. You cannot download the file until
    the \"status\" field indicates `complete` - which is also when you'll receive a fileid.


    Args:
        survey_id (str):
        export_progress_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExportStatusResponse, Meta]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        export_progress_id=export_progress_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    export_progress_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ExportStatusResponse, Meta]]:
    r"""Get Response Export Progress

     Retrieves the status of a response export for the given `exportProgressId`. Please note you will
    find the `exportProgressId` in the Export Responses POST response in the `progressId` field.

    If you receive a status of `failed`, record your `requestId` and try your export again. Contact
    support with your `requestId` and date and time of the call to troubleshoot.

    <!-- theme: danger -->
    > ### Before calling this API, make sure your `exportProgressId` is not null.
    > You could end up in an infinite loop if you don't code this properly. Please check for null before
    making this call. Also check for a 404 response and stop polling if you receive one.

    <!-- theme: info -->
    >### `percentComplete` Field
    >Please note the percentComplete field is a convenience field. You cannot download the file until
    the \"status\" field indicates `complete` - which is also when you'll receive a fileid.


    Args:
        survey_id (str):
        export_progress_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExportStatusResponse, Meta]
    """

    return sync_detailed(
        survey_id=survey_id,
        export_progress_id=export_progress_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    export_progress_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ExportStatusResponse, Meta]]:
    r"""Get Response Export Progress

     Retrieves the status of a response export for the given `exportProgressId`. Please note you will
    find the `exportProgressId` in the Export Responses POST response in the `progressId` field.

    If you receive a status of `failed`, record your `requestId` and try your export again. Contact
    support with your `requestId` and date and time of the call to troubleshoot.

    <!-- theme: danger -->
    > ### Before calling this API, make sure your `exportProgressId` is not null.
    > You could end up in an infinite loop if you don't code this properly. Please check for null before
    making this call. Also check for a 404 response and stop polling if you receive one.

    <!-- theme: info -->
    >### `percentComplete` Field
    >Please note the percentComplete field is a convenience field. You cannot download the file until
    the \"status\" field indicates `complete` - which is also when you'll receive a fileid.


    Args:
        survey_id (str):
        export_progress_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExportStatusResponse, Meta]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        export_progress_id=export_progress_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    export_progress_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ExportStatusResponse, Meta]]:
    r"""Get Response Export Progress

     Retrieves the status of a response export for the given `exportProgressId`. Please note you will
    find the `exportProgressId` in the Export Responses POST response in the `progressId` field.

    If you receive a status of `failed`, record your `requestId` and try your export again. Contact
    support with your `requestId` and date and time of the call to troubleshoot.

    <!-- theme: danger -->
    > ### Before calling this API, make sure your `exportProgressId` is not null.
    > You could end up in an infinite loop if you don't code this properly. Please check for null before
    making this call. Also check for a 404 response and stop polling if you receive one.

    <!-- theme: info -->
    >### `percentComplete` Field
    >Please note the percentComplete field is a convenience field. You cannot download the file until
    the \"status\" field indicates `complete` - which is also when you'll receive a fileid.


    Args:
        survey_id (str):
        export_progress_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExportStatusResponse, Meta]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            export_progress_id=export_progress_id,
            client=client,
        )
    ).parsed
