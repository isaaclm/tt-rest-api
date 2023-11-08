import unittest
from unittest.mock import Mock, patch
from ttrest import TTAuthenticator
from ttrest import TTUserClient
from ttrest import TTEnvironments

# Test constants
TEST_USER_ID = "test_user_id"
TT_GET_USER_ACCOUNTS_URL = f"https://ttrestapi.trade.tt/ttuser/ext_uat_cert/user/{TEST_USER_ID}/accounts"
TT_GET_USERS_LIMITS_URL = f"https://ttrestapi.trade.tt/ttuser/ext_uat_cert/user/{TEST_USER_ID}/limits"
TT_GET_USERS_URL = "https://ttrestapi.trade.tt/ttuser/ext_uat_cert/users"


class TestTTUserClient(unittest.TestCase):
    def setUp(self):
        self.auth_handler = Mock(spec=TTAuthenticator)
        self.client = TTUserClient(self.auth_handler)

    @patch("ttrest.rest_client.TTRestClient._authenticated_get")
    def test_get_accounts(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.client.get_accounts(TEST_USER_ID)

        expected_url = TT_GET_USER_ACCOUNTS_URL
        expected_query = {}

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )

    @patch("ttrest.rest_client.TTRestClient._authenticated_get")
    def test_get_limits(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.client.get_limits(TEST_USER_ID)

        expected_url = TT_GET_USERS_LIMITS_URL
        expected_query = {}

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )

    @patch("ttrest.rest_client.TTRestClient._authenticated_get")
    def test_get_users(self, mock_authenticated_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_authenticated_get.return_value = mock_response

        self.client.auth_handler.environment = TTEnvironments.UAT  # Set the environment to UAT

        self.client.get_users()

        expected_url = TT_GET_USERS_URL
        expected_query = {}

        # Verify that the method is called with the expected URL and query
        mock_authenticated_get.assert_called_once_with(
            expected_url,
            query=expected_query
        )


if __name__ == '__main__':
    unittest.main()
