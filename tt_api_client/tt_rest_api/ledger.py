from .base_client import TTBaseClient
from .authentication import TTAuthentication


class TTLedgerClient(TTBaseClient):
    endpoint = "ttledger"

    def __init__(self, auth_handler: TTAuthentication):
        super().__init__(auth_handler)

    def get_fills(self, accountId=None, maxTimestamp=None, minTimestamp=None, orderId=None, productId=None, includeOTC=False, return_json=False):
        # Add all function args to the query then filter out the keys with Null values
        query = {
            "accountId": accountId,
            "maxTimestamp": maxTimestamp,
            "minTimestamp": minTimestamp,
            "orderId": orderId,
            "productId": productId,
            "includeOTC": includeOTC
        }
        # Filter out the keys with Null values
        query = {key: value for key, value in query.items() if value is not None}

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/fills"
        response = self._authenticated_get(url, query=query)

        json = response.json()

        if return_json:
            return response.json()
        else:
            raise Exception("Not implemented")

    def get_order_data(self):
        endpoint = f"{self.TT_BASE_URL}/ttledger/orderdata"
        response = self._authenticated_get(endpoint)
        return response.json()

    def get_orders(self):
        endpoint = f"{self.TT_BASE_URL}/ttledger/orders"
        response = self._authenticated_get(endpoint)
        return response.json()

    def get_order_by_id(self, order_id):
        endpoint = f"{self.TT_BASE_URL}/ttledger/orders/{order_id}"
        response = self._authenticated_get(endpoint)
        return response.json()
