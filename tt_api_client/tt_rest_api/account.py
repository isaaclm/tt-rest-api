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

    def get_accounts(self, mine_only: bool = False):
        """
        Gets a list of accounts associated with the application key.

        Args:
            mine_only (bool): Set as True to return only the account through which the user can trade.

        Returns:
            dict: JSON response containing response status and account information. Use the "accounts" key to reference the list of accounts.

        Raises:
            PostRequestError: If the response status code is not 200.
        """
        query = {
            "mineOnly": str(mine_only).lower()
        }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/accounts"
        response = self._authenticated_get(url, query=query)
        return response.json()
