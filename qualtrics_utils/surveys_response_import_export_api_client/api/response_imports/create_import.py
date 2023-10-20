from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_import_json_body import CreateImportJsonBody
from ...models.creation_response import CreationResponse
from ...models.creation_response_invalid import CreationResponseInvalid
from ...models.creation_response_too_large import CreationResponseTooLarge
from ...models.internal_error import InternalError
from ...models.meta import Meta
from ...models.survey_not_found import SurveyNotFound
from ...types import Response, Unset


def _get_kwargs(
    survey_id: str,
    *,
    json_body: CreateImportJsonBody,
    idempotency_key: Union[Unset, str] = "",
) -> Dict[str, Any]:
    headers = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/surveys/{surveyId}/import-responses".format(
            surveyId=survey_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreationResponse,
        CreationResponseInvalid,
        CreationResponseTooLarge,
        InternalError,
        Meta,
        SurveyNotFound,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreationResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreationResponseInvalid.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Meta.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = SurveyNotFound.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        response_413 = CreationResponseTooLarge.from_dict(response.json())

        return response_413
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        response_429 = CreationResponseTooLarge.from_dict(response.json())

        return response_429
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = InternalError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreationResponse,
        CreationResponseInvalid,
        CreationResponseTooLarge,
        InternalError,
        Meta,
        SurveyNotFound,
    ]
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
    json_body: CreateImportJsonBody,
    idempotency_key: Union[Unset, str] = "",
) -> Response[
    Union[
        CreationResponse,
        CreationResponseInvalid,
        CreationResponseTooLarge,
        InternalError,
        Meta,
        SurveyNotFound,
    ]
]:
    r""" Start Response Import

     Starts an import of a CSV or TSV file. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within an import workflow.

    <!-- theme: warning -->
    > ### The API console does not generate code correctly for this endpoint. Use curl for sending
    requests.
    > The API console does not render code generation correctly when used to upload CSV or TSV files to
    this endpoint. Use curl for testing this endpoint.


    ### Import via Locally Hosted File
    To import using a locally hosted CSV or TSV file, see this example:

    <!--
    title: Import via Locally Hosted File
    -->
    ```shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
      --data-binary '@MyResponses.csv'--header 'Content-Type: text/csv' \
      --header 'charset: UTF-8' \
      --header 'Authorization: Bearer ec9f2045-e33d-4201-80c7-beee28728ef6'
    ```

    ### Import via a File Hosted at a Public URL
    To import using a remote, publicly hosted CSV or TSV file, see this example:

    <!--
    title: Import via a File Hosted at a Public URL
    lineNumbers: true
    -->
    ``` shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
        --header 'Content-Type: application/json' \
        --header 'Authorization: Bearer 8c1e372c-b65a-4ef1-b761-51affbc80216' \
        --data-raw '{
            \"format\": \"csv\",
            \"fileUrl\": \"http://myfilehost.com/MyResponses.csv\"
        }'
    ```

    <!-- theme: danger -->
    > ### Files Uploaded from a Remote Location Require a Public URL
    > A CSV or TSV file uploaded from a remote location must be available via a publicly accessible URL.

    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.
        json_body (CreateImportJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreationResponse, CreationResponseInvalid, CreationResponseTooLarge, InternalError, Meta, SurveyNotFound]]
     """

    kwargs = _get_kwargs(
        survey_id=survey_id,
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
    json_body: CreateImportJsonBody,
    idempotency_key: Union[Unset, str] = "",
) -> Optional[
    Union[
        CreationResponse,
        CreationResponseInvalid,
        CreationResponseTooLarge,
        InternalError,
        Meta,
        SurveyNotFound,
    ]
]:
    r""" Start Response Import

     Starts an import of a CSV or TSV file. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within an import workflow.

    <!-- theme: warning -->
    > ### The API console does not generate code correctly for this endpoint. Use curl for sending
    requests.
    > The API console does not render code generation correctly when used to upload CSV or TSV files to
    this endpoint. Use curl for testing this endpoint.


    ### Import via Locally Hosted File
    To import using a locally hosted CSV or TSV file, see this example:

    <!--
    title: Import via Locally Hosted File
    -->
    ```shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
      --data-binary '@MyResponses.csv'--header 'Content-Type: text/csv' \
      --header 'charset: UTF-8' \
      --header 'Authorization: Bearer ec9f2045-e33d-4201-80c7-beee28728ef6'
    ```

    ### Import via a File Hosted at a Public URL
    To import using a remote, publicly hosted CSV or TSV file, see this example:

    <!--
    title: Import via a File Hosted at a Public URL
    lineNumbers: true
    -->
    ``` shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
        --header 'Content-Type: application/json' \
        --header 'Authorization: Bearer 8c1e372c-b65a-4ef1-b761-51affbc80216' \
        --data-raw '{
            \"format\": \"csv\",
            \"fileUrl\": \"http://myfilehost.com/MyResponses.csv\"
        }'
    ```

    <!-- theme: danger -->
    > ### Files Uploaded from a Remote Location Require a Public URL
    > A CSV or TSV file uploaded from a remote location must be available via a publicly accessible URL.

    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.
        json_body (CreateImportJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreationResponse, CreationResponseInvalid, CreationResponseTooLarge, InternalError, Meta, SurveyNotFound]
     """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreateImportJsonBody,
    idempotency_key: Union[Unset, str] = "",
) -> Response[
    Union[
        CreationResponse,
        CreationResponseInvalid,
        CreationResponseTooLarge,
        InternalError,
        Meta,
        SurveyNotFound,
    ]
]:
    r""" Start Response Import

     Starts an import of a CSV or TSV file. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within an import workflow.

    <!-- theme: warning -->
    > ### The API console does not generate code correctly for this endpoint. Use curl for sending
    requests.
    > The API console does not render code generation correctly when used to upload CSV or TSV files to
    this endpoint. Use curl for testing this endpoint.


    ### Import via Locally Hosted File
    To import using a locally hosted CSV or TSV file, see this example:

    <!--
    title: Import via Locally Hosted File
    -->
    ```shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
      --data-binary '@MyResponses.csv'--header 'Content-Type: text/csv' \
      --header 'charset: UTF-8' \
      --header 'Authorization: Bearer ec9f2045-e33d-4201-80c7-beee28728ef6'
    ```

    ### Import via a File Hosted at a Public URL
    To import using a remote, publicly hosted CSV or TSV file, see this example:

    <!--
    title: Import via a File Hosted at a Public URL
    lineNumbers: true
    -->
    ``` shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
        --header 'Content-Type: application/json' \
        --header 'Authorization: Bearer 8c1e372c-b65a-4ef1-b761-51affbc80216' \
        --data-raw '{
            \"format\": \"csv\",
            \"fileUrl\": \"http://myfilehost.com/MyResponses.csv\"
        }'
    ```

    <!-- theme: danger -->
    > ### Files Uploaded from a Remote Location Require a Public URL
    > A CSV or TSV file uploaded from a remote location must be available via a publicly accessible URL.

    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.
        json_body (CreateImportJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreationResponse, CreationResponseInvalid, CreationResponseTooLarge, InternalError, Meta, SurveyNotFound]]
     """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreateImportJsonBody,
    idempotency_key: Union[Unset, str] = "",
) -> Optional[
    Union[
        CreationResponse,
        CreationResponseInvalid,
        CreationResponseTooLarge,
        InternalError,
        Meta,
        SurveyNotFound,
    ]
]:
    r""" Start Response Import

     Starts an import of a CSV or TSV file. See the [Response Import/Export API
    Overview](../../../../reference/responseImportsExports.json) for more detail on how to use this
    endpoint within an import workflow.

    <!-- theme: warning -->
    > ### The API console does not generate code correctly for this endpoint. Use curl for sending
    requests.
    > The API console does not render code generation correctly when used to upload CSV or TSV files to
    this endpoint. Use curl for testing this endpoint.


    ### Import via Locally Hosted File
    To import using a locally hosted CSV or TSV file, see this example:

    <!--
    title: Import via Locally Hosted File
    -->
    ```shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
      --data-binary '@MyResponses.csv'--header 'Content-Type: text/csv' \
      --header 'charset: UTF-8' \
      --header 'Authorization: Bearer ec9f2045-e33d-4201-80c7-beee28728ef6'
    ```

    ### Import via a File Hosted at a Public URL
    To import using a remote, publicly hosted CSV or TSV file, see this example:

    <!--
    title: Import via a File Hosted at a Public URL
    lineNumbers: true
    -->
    ``` shell
    curl --location --request POST 'iad1.qualtrics.com/API/v3/surveys/SV_bwrylOA5nNnI9M1/import-
    responses' \
        --header 'Content-Type: application/json' \
        --header 'Authorization: Bearer 8c1e372c-b65a-4ef1-b761-51affbc80216' \
        --data-raw '{
            \"format\": \"csv\",
            \"fileUrl\": \"http://myfilehost.com/MyResponses.csv\"
        }'
    ```

    <!-- theme: danger -->
    > ### Files Uploaded from a Remote Location Require a Public URL
    > A CSV or TSV file uploaded from a remote location must be available via a publicly accessible URL.

    Args:
        survey_id (str):
        idempotency_key (Union[Unset, str]):  Default: ''.
        json_body (CreateImportJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreationResponse, CreationResponseInvalid, CreationResponseTooLarge, InternalError, Meta, SurveyNotFound]
     """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
            json_body=json_body,
            idempotency_key=idempotency_key,
        )
    ).parsed
