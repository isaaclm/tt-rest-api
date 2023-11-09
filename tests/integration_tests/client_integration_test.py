from ttrest.authenticator import TTAuthenticator
from ttrest.environments import TTEnvironments
import unittest
import configparser
import os


class ClientIntegrationTest(unittest.TestCase):
    def setUp(self):
        # Set up the test variables
        app_name = "API_Test_App"
        company_name = "Test_Company"
        environment = TTEnvironments.UAT

        # Read the config file
        config_fname = "test_config.ini"
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_fname)
        config = configparser.ConfigParser()
        config.read(config_path)
        self.config = config

        # Get the credentials from the config file
        api_secret = config.get('REST_API', 'tt_rest_key')
        api_key = api_secret.split(":")[0]

        # Initialise the authenticator
        self.auth_handler = TTAuthenticator(environment, api_key, api_secret, app_name, company_name)
