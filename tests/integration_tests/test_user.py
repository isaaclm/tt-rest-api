from tests.integration_tests import ClientIntegrationTest
from ttrest import TTUserClient

import unittest

CONFIG_SECTION = "USER_CLIENT_TESTING"
USER_ID_SETTING = "user_id"
ACCOUNT_ID_SETTING = "account_id"


class TTUserClientIntegrationTest(ClientIntegrationTest):
    def setUp(self):
        # Set up the test variables including config and auth_handler via super class
        super().setUp()

        # Initialise the client
        self.client = TTUserClient(self.auth_handler)

        # Get the test user and account IDs from the config file. They need to be set in the TT UAT environment
        self.user_id = str(self.config.get(CONFIG_SECTION, USER_ID_SETTING))
        self.account_id = str(self.config.get(CONFIG_SECTION, ACCOUNT_ID_SETTING))

    def test_get_accounts(self):
        # Run the test function
        test_function = self.client.get_accounts
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function(self.user_id)

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("accounts" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("userId" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains the expected user_id
        self.assertTrue(str(response["userId"]) == self.user_id)

        # Verify that the response contains accounts including the expected account
        accounts = response["accounts"]
        self.assertTrue(isinstance(accounts, list))
        self.assertTrue(len(accounts) > 0)
        account = next((account for account in accounts if str(account.get("accountId")) == self.account_id), None)
        self.assertTrue(isinstance(account, dict))

        # Verify that the account contains the expected keys
        self.assertTrue("accountId" in account)
        self.assertTrue("accountName" in account)
        self.assertTrue("orderPermissions" in account)
        self.assertTrue("permissions" in account)
        self.assertTrue(isinstance(account["orderPermissions"], dict))
        self.assertTrue(isinstance(account["permissions"], dict))

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_all_accounts(self):
        # Run the test function
        test_function = self.client.get_all_accounts
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function(self.user_id)

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("accounts" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("userId" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains the expected user_id
        self.assertTrue(str(response["userId"]) == self.user_id)

        # Verify that the response contains accounts including the expected account
        accounts = response["accounts"]
        self.assertTrue(isinstance(accounts, list))
        self.assertTrue(len(accounts) > 0)
        account = next((account for account in accounts if str(account.get("accountId")) == self.account_id), None)
        self.assertTrue(isinstance(account, dict))

        # Verify that the account contains the expected keys
        self.assertTrue("accountId" in account)
        self.assertTrue("accountName" in account)
        self.assertTrue("orderPermissions" in account)
        self.assertTrue("permissions" in account)
        self.assertTrue(isinstance(account["orderPermissions"], dict))
        self.assertTrue(isinstance(account["permissions"], dict))

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_limits(self):
        # Run the test function
        test_function = self.client.get_limits
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function(self.user_id)

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("userLimits" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        limits = response["userLimits"]
        self.assertTrue(isinstance(limits, list))
        self.assertTrue(len(limits) > 0)
        limit = next((limit for limit in limits if str(limit.get("userId")) == self.user_id), None)
        self.assertTrue(isinstance(limit, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("userId" in limit)
        self.assertTrue("riskLimits" in limit)

        risk_limits = limit["riskLimits"]
        self.assertTrue("contractLimits" in risk_limits)
        self.assertTrue("interProductLimits" in risk_limits)
        self.assertTrue("productLimits" in risk_limits)

        # Verify that the keys are the correct types
        self.assertTrue(isinstance(risk_limits["contractLimits"], list))
        self.assertTrue(isinstance(risk_limits["interProductLimits"], list))
        self.assertTrue(isinstance(risk_limits["productLimits"], list))

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_all_limits(self):
        # Run the test function
        test_function = self.client.get_all_limits
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function(self.user_id)

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("userLimits" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        limits = response["userLimits"]
        self.assertTrue(isinstance(limits, list))
        self.assertTrue(len(limits) > 0)
        limit = next((limit for limit in limits if str(limit.get("userId")) == self.user_id), None)
        self.assertTrue(isinstance(limit, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("userId" in limit)
        self.assertTrue("riskLimits" in limit)

        risk_limits = limit["riskLimits"]
        self.assertTrue("contractLimits" in risk_limits)
        self.assertTrue("interProductLimits" in risk_limits)
        self.assertTrue("productLimits" in risk_limits)

        # Verify that the keys are the correct types
        self.assertTrue(isinstance(risk_limits["contractLimits"], list))
        self.assertTrue(isinstance(risk_limits["interProductLimits"], list))
        self.assertTrue(isinstance(risk_limits["productLimits"], list))

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_users(self):
        # Run the test function
        test_function = self.client.get_users
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function()

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("users" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        users = response["users"]
        self.assertTrue(isinstance(users, list))
        self.assertTrue(len(users) > 0)
        user = next((user for user in users if str(user.get("id")) == self.user_id), None)
        self.assertTrue(isinstance(user, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("id" in user)
        self.assertTrue("email" in user)
        self.assertTrue("firstname" in user)
        self.assertTrue("lastname" in user)
        self.assertTrue("alias" in user)

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")

    def test_get_all_users(self):
        # Run the test function
        test_function = self.client.get_all_users
        print(f"Running functional test for {self.client.__class__.__name__}.{test_function.__name__}()...")
        response = test_function()

        # Verify that the response is a JSON object
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, dict))

        # Verify that the response contains the expected keys
        self.assertTrue("users" in response)
        self.assertTrue("lastPage" in response)
        self.assertTrue("status" in response)

        # Verify that the response was successful
        self.assertTrue(response["status"].strip().lower() == "ok")

        # Verify that the response contains users including the expected user
        users = response["users"]
        self.assertTrue(isinstance(users, list))
        self.assertTrue(len(users) > 0)
        user = next((user for user in users if str(user.get("id")) == self.user_id), None)
        self.assertTrue(isinstance(user, dict))

        # Verify that the user contains the expected keys
        self.assertTrue("id" in user)
        self.assertTrue("email" in user)
        self.assertTrue("firstname" in user)
        self.assertTrue("lastname" in user)
        self.assertTrue("alias" in user)

        print(f"... {self.client.__class__.__name__}.{test_function.__name__}() test completed successfully.")


if __name__ == '__main__':
    unittest.main()
