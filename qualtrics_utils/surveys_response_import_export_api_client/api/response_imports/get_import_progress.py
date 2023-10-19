from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.import_status_response import ImportStatusResponse
from ...models.import_status_response_not_found import ImportStatusResponseNotFound
from ...models.internal_error import InternalError
from ...types import Response, Unset


def _get_kwargs(
    survey_id: str,
    import_progress_id: str,
    *,
    idempotency_key: Union[Unset, str] = "",
) -> Dict[str, Any]:
    headers = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    return {
        "method": "get",
        "url": "/surveys/{surveyId}/import-responses/{importProgressId}".format(
            surveyId=survey_id,
            importProgressId=import_progress_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ImportStatusResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ImportStatusResponseNotFound.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = InternalError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    import_progress_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: Union[Unset, str] = "",
) -> Response[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]:
    """Get Import Progress

     Retrieves the status of an import. See the [Response Import/Export API
    Overview](responseImportsExports.json) for more detail on how to use this endpoint within an import
    workflow.

    If you receive a status of failed, record your requestId and try your import again. Contact support
    with your requestId and date and time of the call to troubleshoot.



    Args:
        survey_id (str):
        import_progress_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        import_progress_id=import_progress_id,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    import_progress_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: Union[Unset, str] = "",
) -> Optional[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]:
    """Get Import Progress

     Retrieves the status of an import. See the [Response Import/Export API
    Overview](responseImportsExports.json) for more detail on how to use this endpoint within an import
    workflow.

    If you receive a status of failed, record your requestId and try your import again. Contact support
    with your requestId and date and time of the call to troubleshoot.



    Args:
        survey_id (str):
        import_progress_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]
    """

    return sync_detailed(
        survey_id=survey_id,
        import_progress_id=import_progress_id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    import_progress_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: Union[Unset, str] = "",
) -> Response[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]:
    """Get Import Progress

     Retrieves the status of an import. See the [Response Import/Export API
    Overview](responseImportsExports.json) for more detail on how to use this endpoint within an import
    workflow.

    If you receive a status of failed, record your requestId and try your import again. Contact support
    with your requestId and date and time of the call to troubleshoot.



    Args:
        survey_id (str):
        import_progress_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        import_progress_id=import_progress_id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    import_progress_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: Union[Unset, str] = "",
) -> Optional[Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]]:
    """Get Import Progress

     Retrieves the status of an import. See the [Response Import/Export API
    Overview](responseImportsExports.json) for more detail on how to use this endpoint within an import
    workflow.

    If you receive a status of failed, record your requestId and try your import again. Contact support
    with your requestId and date and time of the call to troubleshoot.



    Args:
        survey_id (str):
        import_progress_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ImportStatusResponse, ImportStatusResponseNotFound, InternalError]
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            import_progress_id=import_progress_id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed
