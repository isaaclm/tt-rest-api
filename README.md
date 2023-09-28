# TT Rest API
This is a client for the Trading Technolgies (TT) Rest API version 2.0.

It's based around a few key components
- TTAuthenticator, used to generate tokens and authenticate API requests
- TTEnvironments, allows connection to either the live or UAT environment
- TT Rest Clients, API clients for the TT services (refer to the list of services below)

TT Documentation: https://library.tradingtechnologies.com/tt-rest/v2/gs-intro.html

## TT API Services
- The **ttpds** service of the TT REST API is used for requests pertaining to exchanges, products and instruments *- fully implemented*
- The **ttledger** service of the TT REST API is used for requests pertaining to viewing order details and transaction history *- partially implemented*
- The **ttmonitor** service of the TT REST API is used for requests pertaining to viewing positions and SOD records for a given account *- all GET methods implemented*
- The **ttsetup** service of the TT REST API is used for requests pertaining to company-level product margins, order tag defaults, exchange connections, and organizations. *- not implemented*
- The **ttuser** service of the TT REST API is used for requests pertaining to risk limits, market data access, contracts, and product settings for given users or user groups *- not implemented*
- The **ttaccount** service of the TT REST API is used for requests pertaining to risk limits, trade permissions, and users for a given account *- partially implemented*
- The **ttgroup** service of the TT REST API is used for requests pertaining to risk limits for risk groups, risk accounts, and user groups *- not implemented*
- The **ttbacktest** service of the TT REST API is used for starting and stopping backtests for ADL algos as well as retrieving their results *- not implemented*

## Code Examples

### Get all fills:

```python
from ttrest import TTAuthenticator
from ttrest import TTEnvironments
from ttrest import TTLedgerClient

app_name = "Your App"
company_name = "Your Company"

# your api secret, the key is the first portion
api_secret = "00000000-0000-0000-0000-000000000000:11111111-1111-1111-1111-111111111111"
api_key = api_secret.split(":")[0]

# use the UAT environment for development
environment = TTEnvironments.UAT

# create and TTAuthentication to handle the API authentication
auth_handler = TTAuthenticator(environment, api_key, api_secret, app_name, company_name)

# create a ledger client
ledger_client = TTLedgerClient(auth_handler)

# get and print all fills, the 'all' methods handle pagination
fills = ledger_client.get_all_fills()
print(fills)
```

Output:

```python
[
  {
    'account': 'account_1',
    'accountId': 123456,
    'aggressorIndicator': 'true',
    'algoId': 0,
    'avgPx': 1234.00,
    ...
  },
  {
    'account': 'account_2',
    'accountId': 098765,
    'aggressorIndicator': 'true',
    'algoId': 0,
    'avgPx': 999.99,
    ...
  },
  ...
]
```


### Get all accounts:

```python
# continued from above ...

from ttrest import TTAccountClient

# create an account client
account_client = TTAccountClient(auth_handler)

# get all accounts
accounts = account_client.get_accounts()
print(accounts)

# the 'all' method was not used so you would want to handle pagination here to ensure all accounts were collected
...

```

Output:

```python
{
  'accounts':
  [
    {
      'accountType': 1,
      'companyId': 123,
      'id': 123456,
      'name': 'account_1',
      'parentAccountId': 098765,
      'parentId': 098765,
      'revision': 1
    },
    {
      'accountType': 1,
      'companyId': 123,
      'id': 098765,
      'name': 'account_2',
      ...
    },
    ...
  ],
  lastPage': 'true',
  'nextPageKey': 'sOmeLOooo000o0ngNEXtPageKey',
  'requestVersion': 1111111,
  'status': 'Ok'
}
```

## Contributions
My focus is on pulling data for use in analytics, therefore my I have been implementing the GET endpoints. Contribution is welcome, especially to implement the POST endpoints.
