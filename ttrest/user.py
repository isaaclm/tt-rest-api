from .rest_client import TTRestClient
from .authenticator import TTAuthenticator

import logging

log = logging.getLogger()


class TTUserClient(TTRestClient):
    endpoint = "ttuser"

    def __init__(self, auth_handler: TTAuthenticator):
        super().__init__(auth_handler)

    def get_accounts(self, user_id, next_page_key=None):
        """
        Gets the list of accounts associated with the specified user ID.

        Args:
            user_id: The user ID. Can be retrieved from the get_users() method.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict:  JSON response containing a list of accounts.
        """
        query = {}

        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/user/{user_id}/accounts"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_accounts(self, user_id):
        """
        Gets the list of all accounts associated with the specified user ID.

        Args:
            user_id:  The user ID. Can be retrieved from the get_users() method.

        Returns:
            dict:  JSON response containing a list of accounts.
        """
        return self._generic_paginated_request(
            self.get_accounts,
            results_key="accounts",
            user_id=user_id
        )

    def get_limits(self, user_id, next_page_key=None):
        """
        Gets the list of limits associated with the specified user ID.

        Args:
            user_id: The user ID. Can be retrieved from the get_users() method.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict:  JSON response containing a list of limits.
        """
        query = {}

        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/user/{user_id}/limits"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_limits(self, user_id):
        """
        Gets the list of all limits associated with the specified user ID.

        Args:
            user_id:  The user ID. Can be retrieved from the get_users() method.

        Returns:
            dict:  JSON response containing a list of limits.
        """
        return self._generic_paginated_request(
            self.get_limits,
            results_key="userLimits",
            user_id=user_id
        )

    def get_users(self, next_page_key=None):
        """
        Gets the list of users associated with the application key.

        Args:
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict:  JSON response containing a list of users.
        """
        query = {}

        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/users"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_users(self):
        """
        Gets the list of all users associated with the application key.

        Returns:
            dict:  JSON response containing a list of users.
        """
        return self._generic_paginated_request(
            self.get_users,
            results_key="users"
        )
