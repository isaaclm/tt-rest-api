import unittest
from unittest.mock import Mock, patch
from tt_api_client.tt_rest_api.authenticator import TTAuthentication
from tt_api_client.tt_rest_api.ledger import TTLedgerClient
from tt_api_client.tt_rest_api.environments import TTEnvironments
from tt_api_client.tt_rest_api.rest_client import TTRestClient


class TestTTLedgerClient(unittest.TestCase):
    def setUp(self):
        self.auth_handler = Mock(spec=TTAuthentication)
        self.ledger_client = TTLedgerClient(self.auth_handler)

    @patch("tt_api_client.tt_rest_api.base_client.TTBaseClient._authenticated_get")
    def test_get_fills_with_query_parameters(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.ledger_client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.ledger_client.get_fills(
            account_id=0,
            max_timestamp=1690930800000000000,
            min_timestamp=1690844400000000000,
            order_id=1234,
            product_id=5678,
            include_otc=True
        )

        expected_url = f"{self.ledger_client.TT_BASE_URL}/ttledger/{TTEnvironments.UAT.value}/fills"
        expected_query = {
            "accountId": 0,
            "maxTimestamp": 1690930800000000000,
            "minTimestamp": 1690844400000000000,
            "orderId": 1234,
            "productId": 5678,
            "includeOTC": True
        }

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )

    @patch("tt_api_client.tt_rest_api.base_client.TTBaseClient._authenticated_get")
    def test_get_fills_return_json(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "fill_data"}
        mock_authenticated_get.return_value = mock_response

        result = self.ledger_client.get_fills()

        self.assertEqual(result, {"data": "fill_data"})


if __name__ == '__main__':
    unittest.main()
