from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.meta import Meta
from ...types import File, Response


def _get_kwargs(
    survey_id: str,
    file_id: str,
) -> Dict[str, Any]:

    pass

    return {
        "method": "get",
        "url": "/surveys/{surveyId}/export-responses/{fileId}/file".format(
            surveyId=survey_id,
            fileId=file_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[File, Meta]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.content))

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
) -> Response[Union[File, Meta]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[File, Meta]]:
    r""" Get Response Export File

     Retrieves the response export file after the file export process completes. By default, the export
    file is returned as a ZIP file, but you can also request the export file in a different file format
    when you start the export with the file format you specified in [Start Response
    Export](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses/post) call. The supported formats for the export file are CSV, NDJSON, TSV, XML, JSON, or
    SPSS. Without an extension, the export file defaults to a ZIP file.

    The compressed file inside the retrieved ZIP file has this naming convention: {Survey Project
    Name}.{Export Format}. Note that the file does not return time and date of export. For date and time
    information, you need to record this information manually during the export process.

    The example below shows a sample cURL request for this endpoint. Please note that you need to
    include your `surveyId` and the `fileId` in the URL of this request. The `fileId` is returned in the
    response to the [Get Response Export
    Progress](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses~1{exportProgressId}/get) call.

    <!-- title: Retrieve file -->
    ```shell
    curl --request GET \
    --url https://ca1.qualtrics.com/API/v3/surveys/surveyId/export-responses/fileId/file \
    --header 'Content-Type: application/json' \
    --header 'X-API-TOKEN: ' \
    -OJ myResponseFile
    ```

    <!-- theme: warning -->
    ### Try it Feature Limitation
    >The 'Try it' tab above does not allow data export. Please use cURL or the Postman app to send this
    request.

    <!-- theme: info -->
    ### File Expiration
    >Export files expire one week after the completion of an export. After that expiration, the file is
    no longer available, and you will have to start the export request again.

    Args:
        survey_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[File, Meta]]
     """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        file_id=file_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[File, Meta]]:
    r""" Get Response Export File

     Retrieves the response export file after the file export process completes. By default, the export
    file is returned as a ZIP file, but you can also request the export file in a different file format
    when you start the export with the file format you specified in [Start Response
    Export](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses/post) call. The supported formats for the export file are CSV, NDJSON, TSV, XML, JSON, or
    SPSS. Without an extension, the export file defaults to a ZIP file.

    The compressed file inside the retrieved ZIP file has this naming convention: {Survey Project
    Name}.{Export Format}. Note that the file does not return time and date of export. For date and time
    information, you need to record this information manually during the export process.

    The example below shows a sample cURL request for this endpoint. Please note that you need to
    include your `surveyId` and the `fileId` in the URL of this request. The `fileId` is returned in the
    response to the [Get Response Export
    Progress](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses~1{exportProgressId}/get) call.

    <!-- title: Retrieve file -->
    ```shell
    curl --request GET \
    --url https://ca1.qualtrics.com/API/v3/surveys/surveyId/export-responses/fileId/file \
    --header 'Content-Type: application/json' \
    --header 'X-API-TOKEN: ' \
    -OJ myResponseFile
    ```

    <!-- theme: warning -->
    ### Try it Feature Limitation
    >The 'Try it' tab above does not allow data export. Please use cURL or the Postman app to send this
    request.

    <!-- theme: info -->
    ### File Expiration
    >Export files expire one week after the completion of an export. After that expiration, the file is
    no longer available, and you will have to start the export request again.

    Args:
        survey_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[File, Meta]
     """

    return sync_detailed(
        survey_id=survey_id,
        file_id=file_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[File, Meta]]:
    r""" Get Response Export File

     Retrieves the response export file after the file export process completes. By default, the export
    file is returned as a ZIP file, but you can also request the export file in a different file format
    when you start the export with the file format you specified in [Start Response
    Export](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses/post) call. The supported formats for the export file are CSV, NDJSON, TSV, XML, JSON, or
    SPSS. Without an extension, the export file defaults to a ZIP file.

    The compressed file inside the retrieved ZIP file has this naming convention: {Survey Project
    Name}.{Export Format}. Note that the file does not return time and date of export. For date and time
    information, you need to record this information manually during the export process.

    The example below shows a sample cURL request for this endpoint. Please note that you need to
    include your `surveyId` and the `fileId` in the URL of this request. The `fileId` is returned in the
    response to the [Get Response Export
    Progress](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses~1{exportProgressId}/get) call.

    <!-- title: Retrieve file -->
    ```shell
    curl --request GET \
    --url https://ca1.qualtrics.com/API/v3/surveys/surveyId/export-responses/fileId/file \
    --header 'Content-Type: application/json' \
    --header 'X-API-TOKEN: ' \
    -OJ myResponseFile
    ```

    <!-- theme: warning -->
    ### Try it Feature Limitation
    >The 'Try it' tab above does not allow data export. Please use cURL or the Postman app to send this
    request.

    <!-- theme: info -->
    ### File Expiration
    >Export files expire one week after the completion of an export. After that expiration, the file is
    no longer available, and you will have to start the export request again.

    Args:
        survey_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[File, Meta]]
     """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        file_id=file_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[File, Meta]]:
    r""" Get Response Export File

     Retrieves the response export file after the file export process completes. By default, the export
    file is returned as a ZIP file, but you can also request the export file in a different file format
    when you start the export with the file format you specified in [Start Response
    Export](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses/post) call. The supported formats for the export file are CSV, NDJSON, TSV, XML, JSON, or
    SPSS. Without an extension, the export file defaults to a ZIP file.

    The compressed file inside the retrieved ZIP file has this naming convention: {Survey Project
    Name}.{Export Format}. Note that the file does not return time and date of export. For date and time
    information, you need to record this information manually during the export process.

    The example below shows a sample cURL request for this endpoint. Please note that you need to
    include your `surveyId` and the `fileId` in the URL of this request. The `fileId` is returned in the
    response to the [Get Response Export
    Progress](../../../../reference/responseImportsExports.json/paths/~1surveys~1{surveyId}~1export-
    responses~1{exportProgressId}/get) call.

    <!-- title: Retrieve file -->
    ```shell
    curl --request GET \
    --url https://ca1.qualtrics.com/API/v3/surveys/surveyId/export-responses/fileId/file \
    --header 'Content-Type: application/json' \
    --header 'X-API-TOKEN: ' \
    -OJ myResponseFile
    ```

    <!-- theme: warning -->
    ### Try it Feature Limitation
    >The 'Try it' tab above does not allow data export. Please use cURL or the Postman app to send this
    request.

    <!-- theme: info -->
    ### File Expiration
    >Export files expire one week after the completion of an export. After that expiration, the file is
    no longer available, and you will have to start the export request again.

    Args:
        survey_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[File, Meta]
     """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            file_id=file_id,
            client=client,
        )
    ).parsed
