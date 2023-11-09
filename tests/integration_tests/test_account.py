from tests.integration_tests import ClientIntegrationTest
from ttrest import TTAccountClient

import unittest

CONFIG_SECTION = "ACCOUNT_CLIENT_TESTING"
ACCOUNT_ID_SETTING = "account_id"


class TTAccountClientIntegrationTest(ClientIntegrationTest):
    def setUp(self):
        # Set up the test variables including config and auth_handler via super class
        super().setUp()

        # Initialise the client
        self.client = TTAccountClient(self.auth_handler)

        # Get the test user and account IDs from the config file. They need to be set in the TT UAT environment
        self.account_id = str(self.config.get(CONFIG_SECTION, ACCOUNT_ID_SETTING))

    def test_get_limits(self):
        # Run the test function
        test_function = self.client.get_limits
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function(self.account_id)

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("accountLimits" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        limits = response["accountLimits"]
        self.assertTrue(isinstance(limits, list))
        self.assertTrue(len(limits) > 0)
        limit = next((limit for limit in limits if str(limit.get("accountId")) == self.account_id), None)
        self.assertTrue(isinstance(limit, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("riskLimitSettings" in limit)
        self.assertTrue("riskLimits" in limit)
        self.assertTrue("accountId" in limit)

        risk_limit_settings = limit["riskLimitSettings"]
        self.assertTrue(isinstance(risk_limit_settings, dict))

        risk_limits = limit["riskLimits"]
        self.assertTrue(isinstance(risk_limits, dict))
        self.assertTrue("interProductLimits" in risk_limits)
        self.assertTrue("productLimits" in risk_limits)
        self.assertTrue("contractLimits" in risk_limits)

        # Verify that the keys are the correct types
        self.assertTrue(isinstance(risk_limits["interProductLimits"], list))
        self.assertTrue(isinstance(risk_limits["productLimits"], list))
        self.assertTrue(isinstance(risk_limits["contractLimits"], list))

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_all_limits(self):
        # Run the test function
        test_function = self.client.get_all_limits
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function(self.account_id)

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("accountLimits" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        limits = response["accountLimits"]
        self.assertTrue(isinstance(limits, list))
        self.assertTrue(len(limits) > 0)
        limit = next((limit for limit in limits if str(limit.get("accountId")) == self.account_id), None)
        self.assertTrue(isinstance(limit, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("riskLimitSettings" in limit)
        self.assertTrue("riskLimits" in limit)
        self.assertTrue("accountId" in limit)

        risk_limit_settings = limit["riskLimitSettings"]
        self.assertTrue(isinstance(risk_limit_settings, dict))

        risk_limits = limit["riskLimits"]
        self.assertTrue(isinstance(risk_limits, dict))
        self.assertTrue("interProductLimits" in risk_limits)
        self.assertTrue("productLimits" in risk_limits)
        self.assertTrue("contractLimits" in risk_limits)

        # Verify that the keys are the correct types
        self.assertTrue(isinstance(risk_limits["interProductLimits"], list))
        self.assertTrue(isinstance(risk_limits["productLimits"], list))
        self.assertTrue(isinstance(risk_limits["contractLimits"], list))

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_accounts(self):
        # Run the test function
        test_function = self.client.get_accounts
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function()

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("accounts" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        accounts = response["accounts"]
        self.assertTrue(isinstance(accounts, list))
        self.assertTrue(len(accounts) > 0)
        account = next((account for account in accounts if str(account.get("id")) == self.account_id), None)
        self.assertTrue(isinstance(account, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("accountType" in account)
        self.assertTrue("companyId" in account)
        self.assertTrue("id" in account)
        self.assertTrue("name" in account)
        # there are other keys, but they are dependent on settings and so not always present

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_all_accounts(self):
        # Run the test function
        test_function = self.client.get_all_accounts
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function()

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("accounts" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        accounts = response["accounts"]
        self.assertTrue(isinstance(accounts, list))
        self.assertTrue(len(accounts) > 0)
        account = next((account for account in accounts if str(account.get("id")) == self.account_id), None)
        self.assertTrue(isinstance(account, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("accountType" in account)
        self.assertTrue("companyId" in account)
        self.assertTrue("id" in account)
        self.assertTrue("name" in account)
        # there are other keys, but they are dependent on settings and so not always present

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")


if __name__ == '__main__':
    unittest.main()
