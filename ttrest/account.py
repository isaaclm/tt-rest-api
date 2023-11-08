from .rest_client import TTRestClient
from .authenticator import TTAuthenticator


class TTAccountClient(TTRestClient):
    """
    A Rest API Client implementing the TT Account endpoints.

    Args:
        auth_handler (TTAuthenticator): An authenticator.
    """
    endpoint = "ttaccount"

    def __init__(self, auth_handler: TTAuthenticator):
        super().__init__(auth_handler)

    def get_limits(self, account_id, next_page_key=None):
        """
        Gets the account limits associated for the specified account ID.
        This returns the:
         - Risk limit settings
         - Risk limits

        Args:
            account_id: The account ID. Can be retrieved from the get_accounts() method.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict:  JSON response containing a list of limits.
        """
        query = {}

        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/account/{account_id}/limits"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_limits(self, account_id):
        """
        Gets all account limits associated for the specified account ID.
        This returns the:
         - Risk limit settings
         - Risk limits

        Args:
            account_id: The account ID. Can be retrieved from the get_accounts() method.

        Returns:
            dict:  JSON response containing a list of limits.
        """
        return self._generic_paginated_request(
            self.get_limits,
            results_key="accountLimits",
            account_id=account_id
        )

    def get_accounts(self, mine_only: bool = False, next_page_key=None):
        """
        Gets a list of accounts associated with the application key.

        Args:
            mine_only (bool): Set as True to return only the account through which the user can trade.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict: JSON response containing response status and account information. Use the "accounts" key to reference the list of accounts.

        Raises:
            PostRequestError: If the response status code is not 200.
        """
        query = {
            "mineOnly": str(mine_only).lower()
        }

        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/accounts"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_accounts(self, mine_only: bool = False):
        """
        Gets a list of accounts associated with the application key.

        Args:
            mine_only (bool): Set as True to return only the account through which the user can trade.

        Returns:
            dict: JSON response containing response status and all account information. Use the "accounts" key to reference the list of accounts.

        Raises:
            PostRequestError: If the response status code is not 200.
        """
        return self._generic_paginated_request(
            self.get_accounts,
            results_key="accounts",
            mine_only=mine_only
        )
