import unittest
from unittest.mock import MagicMock
from tt_api_client.tt_rest_api.rest_client import TTRestClient


class TestTTRestClient(unittest.TestCase):
    def setUp(self):
        # Create a mock authentication handler for testing
        self.auth_handler = MagicMock()

    def test_not_paginated_request(self):
        # Create an instance of TTRestClient with the mock authentication handler
        tt_client = TTRestClient(self.auth_handler)

        # Define a mock request function for testing
        def mock_request_func(*args, **kwargs):
            return {
                "results_key": [1, 2, 3],
                "lastPage": "true"
            }

        # Call the _generic_paginated_request function with the mock request function
        response = tt_client._generic_paginated_request(
            request_func=mock_request_func,
            results_key="results_key",
            arg1="arg1",
            arg2="arg2"
        )

        # Assert that the response matches the expected structure after pagination
        self.assertEqual(response, {
            "results_key": [1, 2, 3],
            "lastPage": "true"
        })

    def test_generic_paginated_request(self):
        # Create an instance of TTRestClient with the mock authentication handler
        tt_client = TTRestClient(self.auth_handler)

        # Define a mock request function for testing
        responses = [
            {
                "results_key": [1, 2, 3],
                "lastPage": "false",
                "nextPageKey": "next_page_key"
            },
            {
                "results_key": [4, 5, 6],
                "lastPage": "true"
            }
        ]

        def mock_request_func(*args, **kwargs):
            return responses.pop(0)

        # Call the _generic_paginated_request function with the mock request function
        response = tt_client._generic_paginated_request(
            request_func=mock_request_func,
            results_key="results_key",
            arg1="arg1",
            arg2="arg2"
        )

        # Assert that the response matches the expected structure after pagination
        self.assertEqual(response, {
            "results_key": [1, 2, 3, 4, 5, 6],
            "lastPage": "true"
        })

    def test_generic_paginated_request_no_nextPage_key(self):
        # Create an instance of TTRestClient with the mock authentication handler
        tt_client = TTRestClient(self.auth_handler)

        # Define a mock request function that does not return nextPageKey
        def mock_request_func(*args, **kwargs):
            response_data = {
                "results_key": [1, 2, 3],
                "lastPage": "false"
            }
            return response_data

        # Call the _generic_paginated_request function with the mock request function
        response = tt_client._generic_paginated_request(
            request_func=mock_request_func,
            results_key="results_key",
            arg1="arg1",
            arg2="arg2"
        )

        # Assert that the response matches the expected structure
        self.assertEqual(response, {
            "results_key": [1, 2, 3],
            "lastPage": "false"
        })

        print("This test should have generated a warning...")


if __name__ == '__main__':
    unittest.main()
