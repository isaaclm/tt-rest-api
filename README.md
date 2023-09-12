# TT_Rest_API
This is a client for the Trading Technolgies (TT) Rest API version 2.0.

It's based around a few key componenets
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

## Caveats
A a "lastPage" key will be returned in the JSON response, however in practive a value "True" is always returned. As some endpoints such as ttledger/fills can return a large amount of data, you cannot rely on "lastPage" to determine whether you have recieved the complete data set. Therefore other methods of checking are required. Where necessary, comments are provided in the code which outlines the approach taken.

## Contributions
My focus is on pulling data for use in analytics, therefore my focus has been on implementing the HTTP GET endpoints. You are welcome to contribute and implement the POST endpoints.
