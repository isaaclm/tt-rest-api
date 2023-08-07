from .base_client import TTBaseClient
from .authentication import TTAuthentication

from datetime import datetime, timedelta
import pandas as pd


class TTLedgerClient(TTBaseClient):
    endpoint = "ttledger"

    def __init__(self, auth_handler: TTAuthentication):
        super().__init__(auth_handler)

    def _convert_to_nanoseconds(self, dt):
        if isinstance(dt, datetime):
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

    def get_fills(self, account_id=None, max_timestamp=None, min_timestamp=None, order_id=None, product_id=None, include_otc=False, as_dataframe=False):
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
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["fills"])

    def get_all_fills(self, account_id=None, max_timestamp=None, min_timestamp=None, order_id=None, product_id=None, include_otc=False, as_dataframe=False):
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
            fills_json = self.get_fills(account_id, max_timestamp, min_timestamp, order_id, product_id, include_otc, as_dataframe)

            if not fills_json or not fills_json["fills"]:
                break

            all_fills.extend(fills_json["fills"])

            if fills_json["lastPage"].lower() == "true":
                break

            # TT Docs: the GET request returns a maximum of 500 fills.
            # To retrieve the next set of fills, you can adjust the minTimestamp parameter as follows:
            #  1. From the query results, extract the timestamp of the last record.
            #  2. In the next request, set `minTimestamp` to last_timestamp + 1.
            # Link: https://library.tradingtechnologies.com/tt-rest/v2/ttledger.html#/default/get_fills
            min_timestamp = fills_json["fills"][-1]['transactTime']
            min_timestamp = int(min_timestamp) + 1 if isinstance(min_timestamp, str) else min_timestamp + 1

        return all_fills

    def get_order_data(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/orderdata"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json

        # Initialize an empty dictionary to hold DataFrames
        data_frames = {}

        # Iterate through the "orderData" dictionary
        for key, value in json["orderData"].items():
            # Create a DataFrame from the list of enums (value)
            df = pd.DataFrame(value.items(), columns=["EnumValue", "Description"])

            # Add the DataFrame to the dictionary with the key
            data_frames[key] = df

        return data_frames

    def get_orders(self):
        # url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/orders"
        raise NotImplementedError()

    def get_order_by_id(self, order_id):
        # url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/orders/{order_id}"
        raise NotImplementedError()

