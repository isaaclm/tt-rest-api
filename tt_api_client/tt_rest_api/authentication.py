import requests
import logging
from uuid import uuid4

from .exceptions import TokenGenerationError

log = logging.getLogger()


class TTAuthentication:
    """
    A class for handling Trading Technologies API authentication.

    Args:
        environment (TTEnvironments): The environment (UAT or LIVE).
        api_key (str): The API key for authentication.
        secret_key (str): The secret key for authentication.
        app_name (str): The name of the application.
        company_name (str): The name of the company.

    Attributes:
        _TT_BASE_URL (str): Base URL for the Trading Technologies API.
    """

    _TT_BASE_URL = "https://apigateway.trade.tt"

    @property
    def environment(self):
        """
        Get the TT environment setting.

        Returns:
            TTEnvironment: The TT environment.
        """
        return self._environment

    @property
    def app_name(self):
        """
        Get the application name.

        Returns:
            str: The application name.
        """
        return self._app_name

    @property
    def company_name(self):
        """
        Get the company name.

        Returns:
            str: The company name.
        """
        return self._company_name

    def __init__(self, environment, api_key, secret_key, app_name, company_name):
        self._environment = environment
        self._app_name = app_name
        self._company_name = company_name
        # secret needs to be in the form key:secret
        # grant_type=user_app&app_key=00000000-0000-0000-0000-000000000000:00000000-0000-0000-0000-000000000000
        self._api_key = api_key
        self._secret_key = secret_key
        self._token = None

    def get_token(self):
        """
        Obtain an authentication token from the Trading Technologies API.
        Refer to https://library.tradingtechnologies.com/tt-rest/v2/ttid.html
        """
        ttid_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-api-key": self._api_key
        }

        ttid_data = {
            "grant_type": "user_app",
            "app_key": self._secret_key
        }

        query = {
            # all requests require a requestId in the format "[app_name]-[co name]--[GUID]"
            "requestId": "{}--{}".format(f"{self._app_name}-{self._company_name}", uuid4())
        }

        url = f"{self._TT_BASE_URL}/ttid/{self._environment.value}/token"
        response = requests.post(url=url, headers=ttid_header, data=ttid_data, params=query)

        if response.status_code == 200:
            json = response.json()
            self._token = '{} {}'.format(json['token_type'].capitalize(), json['access_token'])
        else:
            raise TokenGenerationError(response)

    def authenticate_request(self, request):
        """
        Authenticate an HTTP request with the generated token.

        Args:
            request (Request): The prepared HTTP request.

        Returns:
            request: The authenticated HTTP request.
        """

        if not self._token:
            self.get_token()

        request.headers.update({
            "x-api-key": self._api_key,
            "Authorization": self._token
        })

        return request
