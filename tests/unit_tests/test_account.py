import unittest
from unittest.mock import Mock, patch
from ttrest import TTAuthenticator
from ttrest import TTAccountClient
from ttrest import TTEnvironments

# Test constants
TEST_ACCOUNT_ID = "test_account_id"
TT_GET_ACCOUNT_LIMITS_URL = f"https://ttrestapi.trade.tt/ttaccount/ext_uat_cert/account/{TEST_ACCOUNT_ID}/limits"
TT_GET_ACCOUNTS_URL = "https://ttrestapi.trade.tt/ttaccount/ext_uat_cert/accounts"


class TestTTUserClient(unittest.TestCase):
    def setUp(self):
        self.auth_handler = Mock(spec=TTAuthenticator)
        self.client = TTAccountClient(self.auth_handler)

    @patch("ttrest.rest_client.TTRestClient._authenticated_get")
    def test_get_limits(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.client.get_limits(TEST_ACCOUNT_ID)

        expected_url = TT_GET_ACCOUNT_LIMITS_URL
        expected_query = {}

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )

    @patch("ttrest.rest_client.TTRestClient._authenticated_get")
    def test_get_accounts(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.client.get_accounts()

        expected_url = TT_GET_ACCOUNTS_URL
        expected_query = {"mineOnly": "false"}

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )

    @patch("ttrest.rest_client.TTRestClient._authenticated_get")
    def test_get_accounts_mine_only(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.client.get_accounts(mine_only=True)

        expected_url = TT_GET_ACCOUNTS_URL
        expected_query = {"mineOnly": "true"}

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )


if __name__ == '__main__':
    unittest.main()
