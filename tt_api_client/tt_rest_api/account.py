from .base_client import TTBaseClient
from .authentication import TTAuthentication


class TTAccountClient(TTBaseClient):
    endpoint = "ttaccount"

    def __init__(self, auth_handler: TTAuthentication):
        super().__init__(auth_handler)

    def get_accounts(self, mine_only: bool = False):
        query = {
            "mineOnly": str(mine_only).lower()
        }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/accounts"
        response = self._authenticated_get(url, query=query)
        return response.json()