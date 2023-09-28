import requests
import logging
from uuid import uuid4
from .exceptions import PostRequestError
from abc import ABC

log = logging.getLogger()


class TTRestClient(ABC):
    """
    A base client for handling authenticated requests to the Trading Technologies API.

    Args:
        app_name (str): The name of the application.
        company_name (str): The name of the company.
        auth_handler (TTAuthentication): An instance of TTAuthentication for handling authentication.

    Attributes:
        TT_BASE_URL (str): Base URL for the Trading Technologies API.
    """

    TT_BASE_URL = "https://apigateway.trade.tt"

    def __init__(self, auth_handler):
        self.auth_handler = auth_handler

    def _authenticated_get(self, url, header=None, data=None, query=None, http_method="get"):
        """
        Send an authenticated HTTP GET request to the Trading Technologies API.

        Args:
            url (str): The API endpoint URL.
            header (dict, optional): Headers to include in the request. Default is None.
            data: (dict, optional): Request payload data. Default is None.
            query: (dict, optional): Query parameters to include in the request. Default is None.
            http_method (str, optional): The HTTP method to use. Default is "get".

        Returns:
            requests.Response: The response object from the API request.

        Raises:
            PostRequestError: If the response status code is not 200.
        """

        log.debug(f"HTTP GET request to TT REST API 2.0 {url}")

        # all TT requests require "[app name]-[company name]--[GUID]"
        req_id = "{}--{}".format(f"{self.auth_handler.app_name}-{self.auth_handler.company_name}", uuid4())

        if query is None:
            query = {"requestId": req_id}
        else:
            query.update({"requestId": req_id})

        with requests.Session() as session:
            request = requests.Request(http_method.upper(), url=url, headers=header, data=data, params=query)
            prepared_request = self.auth_handler.authenticate_request(request.prepare())
            response = session.send(prepared_request)

        if response.status_code != 200:
            raise PostRequestError(response)

        return response

    def _generic_paginated_request(self, request_func, results_key, *args, **kwargs):
        json_response = request_func(*args, **kwargs)
        items = json_response[results_key]
        is_last_page = json_response["lastPage"].lower().strip() == "true"
        next_page_key = json_response["nextPageKey"] if ("nextPageKey" in json_response) else "[Key not included]"
        logging.debug(f"{request_func.__name__}: lastPage={is_last_page}, nextPageKey={next_page_key}")

        while not is_last_page:
            try:
                next_page_key = json_response["nextPageKey"]
                json_response = request_func(*args, **kwargs, next_page_key=next_page_key)
                items.extend(json_response[results_key])
                is_last_page = json_response["lastPage"].lower().strip() == "true"
                logging.debug(f"{request_func.__name__}: lastPage={is_last_page}, nextPageKey={next_page_key}")
            except KeyError as e:
                error_message = f"'nextPageKey' not returned in server response to {request_func.__name__}(). Returning the retrieved, but possibly incomplete data."
                error_message += f"\n\tError: {e}"
                logging.warning(error_message)
                break

        json_response.update({results_key: items})
        return json_response
