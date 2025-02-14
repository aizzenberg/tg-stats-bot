from typing import Union

import httpx
from httpx import Headers
from httpx._types import RequestData

from services.env_service import get_env_var


class ApiService:
    @classmethod
    def _get_api_url(cls) -> str:
        return get_env_var('API_URL')

    @classmethod
    def _get_token(cls) -> str:
        endpoint_url = f'{cls._get_api_url()}/auth/token'
        # print(endpoint_url)
        username, password = get_env_var('API_USERNAME'), get_env_var('API_PASSWORD')
        auth_data = {'username': username, 'password': password}

        try:
            response = httpx.post(url=endpoint_url, data=auth_data)
            response.raise_for_status()
            response = response.json()
        except httpx.HTTPError as exc:
            raise exc

        return response['access_token']

    @classmethod
    def _request(cls, method: str, endpoint: str, data: Union[RequestData, None] = None, **kwargs):
        endpoint_url = f'{cls._get_api_url()}/{endpoint}'
        access_token = cls._get_token()
        headers = Headers({'Authorization': f'Bearer {access_token}'})

        try:
            response = httpx.request(method=method, url=endpoint_url, data=data, headers=headers, **kwargs)
            response.raise_for_status()
            response = response.json()
        except httpx.HTTPError as exc:
            raise exc

        return response

    @classmethod
    def post(cls, endpoint: str, data: Union[RequestData, None] = None, **kwargs):
        return cls._request(method='POST', endpoint=endpoint, data=data, **kwargs)

    @classmethod
    def get(cls, endpoint: str, **kwargs):
        return cls._request(method='GET', endpoint=endpoint, **kwargs)


def get_random_quote():
    endpoint_url = 'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru'
    method = 'GET'

    try:
        response = httpx.request(method=method, url=endpoint_url)
        response.raise_for_status()
        response = response.json()
    except httpx.HTTPError as exc:
        raise exc

    return response

