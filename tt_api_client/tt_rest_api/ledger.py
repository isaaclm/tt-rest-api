from .rest_client import TTRestClient
from .authenticator import TTAuthenticator
from datetime import datetime, date, timedelta
import logging

log = logging.getLogger()


class TTLedgerClient(TTRestClient):
    """
    A Rest API Client implementing the TT Account endpoints.

    Args:
        auth_handler (TTAuthenticator): An authenticator.
    """
    endpoint = "ttledger"

    def __init__(self, auth_handler: TTAuthenticator):
        super().__init__(auth_handler)

    def _convert_to_nanoseconds(self, dt):
        if isinstance(dt, datetime):
            epoch_time_ns = int(dt.timestamp() * 1e9)
            return epoch_time_ns
        elif isinstance(dt, date):
            # turn date into datetime with time = midnight = 0:00:00
            dt = datetime.combine(dt, datetime.min.time())
            epoch_time_ns = int(dt.timestamp() * 1e9)
            return epoch_time_ns
        elif isinstance(dt, int):
            # assume already epoch time in ns
            return dt
        else:
            # Can't assume type of data. Throw error
            raise TypeError(f"Expected timestamp or epoch time in nanoseconds but got {type(dt)}")

    def _convert_epoch_time_in_ns_to_datetime(self, epoch_time_ns):
        # Convert nanoseconds to seconds and microseconds
        t_seconds = epoch_time_ns // 1_000_000_000
        t_microseconds = (epoch_time_ns % 1_000_000_000) // 1000

        # Create a datetime object using the converted values
        dt = datetime.utcfromtimestamp(t_seconds) + timedelta(microseconds=t_microseconds)
        return dt

    def get_fills(self, account_id=None, max_timestamp=None, min_timestamp=None, order_id=None, product_id=None, include_otc=False):
        """
        Retrieves fills for specified criteria.

        Args:
            account_id (int): Account ID to filter fills.
            max_timestamp (int/datetime): Filters fills before the specified datetime or int (epoch time in nanoseconds).
            min_timestamp (int/datetime): Filters fills after the specified datetime or int (epoch time in nanoseconds).
            order_id (int): Order ID to filter fills.
            product_id (int): Product ID to filter fills.
            include_otc (int): Whether to include fills for OTC trades.

        Returns:
            dict: JSON response containing fills information.

        Note:
            The GET request returns a maximum of 500 fills. To retrieve the next set of fills,
            adjust the minTimestamp parameter as described in the documentation or use get_all_fills().
        """

        # Add all function args to the query then filter out the keys with Null values
        query = {
            "accountId": account_id,
            "maxTimestamp": self._convert_to_nanoseconds(max_timestamp) if max_timestamp else None,
            "minTimestamp": self._convert_to_nanoseconds(min_timestamp) if min_timestamp else None,
            "orderId": order_id,
            "productId": product_id,
            "includeOTC": include_otc
        }
        # Filter out the keys with Null values
        query = {key: value for key, value in query.items() if value is not None}

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/fills"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_fills(self, account_id=None, max_timestamp=None, min_timestamp=None, order_id=None, product_id=None, include_otc=False):
        """
        Retrieves all fills, handling pagination.

        Args:
            account_id (int): Account ID to filter fills.
            max_timestamp (int/datetime): Filters fills before the specified datetime or int (epoch time in nanoseconds).
            min_timestamp (int/datetime): Filters fills after the specified datetime or int (epoch time in nanoseconds).
            order_id (int): Order ID to filter fills.
            product_id (int): Product ID to filter fills.
            include_otc (bool): Whether to include fills for OTC trades.

        Returns:
            list: Aggregated list of fills across multiple requests.
        """

        all_fills = []

        while True:
            fills_json = self.get_fills(account_id, max_timestamp, min_timestamp, order_id, product_id, include_otc)

            if "fills" in fills_json:
                all_fills.extend(fills_json["fills"])

                message = "Requested fills"
                message += f"\n\tParams: max_timestamp={min_timestamp}, min_timestamp={max_timestamp},min_timestamp=" \
                           f"{max_timestamp}, order_id={order_id}, product_id={product_id}, include_otc={include_otc}"
                message += f"\n\tResults Count: {len(fills_json['fills'])}"
                log.debug(message)

                if len(fills_json["fills"]) == 0:
                    # if fills is an empty set then there are no more fills
                    break
            else:
                # there are no fills
                break

            # TT Docs: the GET request returns a maximum of 500 fills.
            # To retrieve the next set of fills, you can adjust the minTimestamp parameter as follows:
            #  1. From the query results, extract the timestamp of the last record.
            #  2. In the next request, set `minTimestamp` to last_timestamp + 1.
            #  3. Repeat this until (a) you get a response with an empty set of fills, or (b) a response with < 500 fills
            # Link: https://library.tradingtechnologies.com/tt-rest/v2/ttledger.html#/default/get_fills
            min_timestamp = fills_json["fills"][-1]['timeStamp']
            min_timestamp = int(min_timestamp) + 1 if isinstance(min_timestamp, str) else min_timestamp + 1

        return all_fills

    def get_order_data(self):
        """
        Retrieves definitions for order-related enumerated values.

        Returns:
            dict: JSON response containing several order fields, each containing numeric values that correspond to
                  enumerated values. For example, an order with orderType=1 indicates a market order.
        """

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/orderdata"
        response = self._authenticated_get(url)
        return response.json()

    def get_orders(self):
        # url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/orders"
        raise NotImplementedError()

    def get_order_by_id(self, order_id):
        # url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/orders/{order_id}"
        raise NotImplementedError()

