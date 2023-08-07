import unittest
from unittest.mock import Mock, patch
from tt_api_client.tt_rest_api.authentication import *
from tt_api_client.tt_rest_api.environments import TTEnvironments
from tt_api_client.tt_rest_api.exceptions import TokenGenerationError


class TestTTAuthentication(unittest.TestCase):
    def setUp(self):
        self.environment = TTEnvironments.UAT
        self.api_key = "your_api_key"
        self.secret_key = "your_secret_key"
        self.app_name = "YourApp"
        self.company_name = "YourCompany"
        self.auth = TTAuthentication(self.environment, self.api_key, self.secret_key, self.app_name, self.company_name)

    @patch("requests.post")
    def test_get_token_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "token_type": "Bearer",
            "access_token": "your_access_token"
        }
        mock_post.return_value = mock_response

        self.auth.get_token()

        self.assertEqual(self.auth._token, "Bearer your_access_token")

    @patch("requests.post")
    def test_get_token_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with self.assertRaises(TokenGenerationError):
            self.auth.get_token()

    @patch("requests.post")
    def test_get_token_exception(self, mock_post):
        mock_response = Mock()
        mock_post.side_effect = TokenGenerationError(mock_response)

        with self.assertRaises(TokenGenerationError):
            self.auth.get_token()

    @patch("requests.post")
    def test_authenticate_request_with_token(self, mock_post):
        self.auth._token = "Bearer your_existing_access_token"
        mock_request = Mock()

        with patch.object(mock_request, 'headers', {}) as mock_headers:
            authenticated_request = self.auth.authenticate_request(mock_request)

        self.assertFalse(mock_post.called)  # No new calls to get_token
        self.assertEqual(mock_headers["Authorization"], "Bearer your_existing_access_token")
        self.assertEqual(mock_headers["x-api-key"], self.api_key)

    @patch("requests.post")
    def test_authenticate_request_without_token(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "token_type": "Bearer",
            "access_token": "your_new_access_token"
        }
        mock_post.return_value = mock_response

        mock_request = Mock()

        with patch.object(mock_request, 'headers', {}) as mock_headers:
            authenticated_request = self.auth.authenticate_request(mock_request)

        self.assertTrue(mock_post.called)  # Call to get_token is made
        self.assertEqual(mock_headers["Authorization"], "Bearer your_new_access_token")
        self.assertEqual(mock_headers["x-api-key"], self.api_key)


if __name__ == '__main__':
    unittest.main()