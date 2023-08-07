from tt_api_client.tt_rest_api.authentication import TTAuthentication
from tt_api_client.tt_rest_api.environments import TTEnvironments
from tt_api_client.tt_rest_api.ledger import TTLedgerClient


if __name__ == "__main__":
    # A simple example to demonstrate the usage of this library. It prints the fills in your UAT environment.

    app_name = "Your App"
    company_name = "Your Company"

    api_secret = "00000000-0000-0000-0000-000000000000:11111111-1111-1111-1111-111111111111"  # Your API Secret
    api_key = api_secret.split(":")[0]

    environment = TTEnvironments.UAT  # UAT for testing
    print(environment.value)

    # Create and TTAuthentication to handle the API authentication
    auth_handler = TTAuthentication(environment, api_key, api_secret, app_name, company_name)
    # Create a client for the TT ttledger Rest API
    ledger_client = TTLedgerClient(auth_handler)

    # Get and print fills (json)
    fills_json = ledger_client.get_fills()
    print(fills_json)
