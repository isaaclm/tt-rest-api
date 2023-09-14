from .rest_client import TTRestClient
from .authenticator import TTAuthenticator
from enum import Enum

import logging

log = logging.getLogger()


class ScaleQty(Enum):
    """
    Enums for the scale quantity settings.
    """
    DEFAULT = None
    CONTRACTS = 0
    IN_FLOW = 1


class TTMonitorClient(TTRestClient):
    """
    A Rest API Client implementing the TT Monitor endpoints.

    Args:
        auth_handler (TTAuthenticator): An authenticator.
    """
    endpoint = "ttmonitor"

    def __init__(self, auth_handler: TTAuthenticator):
        super().__init__(auth_handler)

    def get_credit_utilization(self, account_id, include_product_pos=None, next_page_key=None):
        """
        Gets credit limit and credit utilization details for a given account.
        For more information on the values returned in this request, consult the documentation on credit limit settings.
        Link: https://library.tradingtechnologies.com/user-setup/rl-configuring-sod-settings-and-credit-limits.html

        Args:
            account_id: Account ID
            include_product_pos: Include product position
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns: JSON record of credit limit and credit utilization details for a given account. For more information on the values returned in this request, consult the TT documentation on credit limit settings.
        """
        query = {
            "accountId": account_id
        }

        if include_product_pos is not None:
            query.update({
                "includeProductPos": str(include_product_pos)
            })

        if next_page_key is not None:
            query.update({
                "nextPageKey": str(next_page_key)
            })

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/creditutilization"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_credit_utilization(self, account_id, include_product_pos=None):
        """
        Gets all credit limit and credit utilization details for a given account.
        For more information on the values returned in this request, consult the documentation on credit limit settings.
        Link: https://library.tradingtechnologies.com/user-setup/rl-configuring-sod-settings-and-credit-limits.html

        Args:
            account_id: Account ID
            include_product_pos: Include product position

        Returns: JSON record of credit limit and credit utilization details for a given account. For more information on the values returned in this request, consult the TT documentation on credit limit settings.
        """
        return self._generic_paginated_request(
            self.get_credit_utilization,
            results_key="creditUtilization",
            account_id=account_id,
            include_product_pos=include_product_pos
        )

    def get_position(self, account_ids: [None, list, int, str] = None, scale_qty: ScaleQty=ScaleQty.DEFAULT, next_page_key=None):
        """
        Gets positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs.
         - TT recommends using the account_ids parameter to filter positions if your company uses many accounts or layers of nested accounts to avoid response timeouts.
         - P&L is expressed in the instrument's currency.

        Args:
            account_ids: Comma-separated list of Account IDs
            scale_qty [ScaleQty]: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns: JSON record of positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs. P&L is expressed in the instrument's currency.

        """
        query = {}

        if account_ids:
            query.update({
                "accountIds": ",".join([str(account_id) for account_id in account_ids]) if isinstance(account_ids, list) else account_ids
            })

        if scale_qty != scale_qty.DEFAULT:
            query.update({
                "scaleQty": str(scale_qty.value)
            })

        if next_page_key is not None:
            query.update({
                "nextPageKey": str(next_page_key)
            })

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/position"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_position(self, account_ids: [None, list, int, str] = None, scale_qty: ScaleQty=ScaleQty.DEFAULT):
        """
        Gets all positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs.

        Args:
            account_ids: Comma-separated list of Account IDs
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

        Returns: JSON record of positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs. P&L is expressed in the instrument's currency.

        """
        return self._generic_paginated_request(
            self.get_position,
            results_key="positions",
            account_ids=account_ids,
            scale_qty=scale_qty
        )

    def get_position_for_account(self, account_id: [int, str], scale_qty=None):
        """
        Gets positions based on today's fills for the provided account ID. Included in the response are SODs.

        Args:
            account_id: Account ID
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns: JSON record of positions based on today's fills for the provided accountId. Included in the response are SODs. P&L is expressed in the instrument's currency.
        """
        query = None
        if scale_qty:
            query = {
                "scaleQty": str(scale_qty)
            }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/position/{account_id}"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_position_for_account(self, account_id: [int, str], scale_qty=None):
        """
        Gets all positions based on today's fills for the provided account ID. Included in the response are SODs.

        Args:
            account_id: Account ID
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns: JSON record of positions based on today's fills for the provided accountId. P&L is expressed in the instrument's currency.
        """
        return self._generic_paginated_request(
            self.get_position_for_account,
            results_key="positions",
            account_id=account_id,
            scale_qty=scale_qty
        )

    def get_product_family_position(self, account_ids: [list, int, str] = None, scale_qty: ScaleQty=ScaleQty.DEFAULT):
        """

        Args:
            account_ids: Comma-separated list of Account IDs
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

        Returns: JSON record of product family positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs. P&L is expressed in the instrument's currency.

        """
        query = {}

        if account_ids:
            query.update({
                "accountIds": ",".join([str(account_id) for account_id in account_ids]) if isinstance(account_ids, list) else account_ids
            })

        if scale_qty:
            query.update({
                "scaleQty": str(scale_qty)
            })

        if (not account_ids) and (not scale_qty):
            query = None

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamilyposition"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_product_family_position_for_account(self, account_id: [int, str], scale_qty: ScaleQty=ScaleQty.DEFAULT):
        """

        Args:
            account_id: Account ID
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

        Returns: JSON record of product family positions based on today's fills for the provided accountId. Included in the response are SODs. P&L is expressed in the instrument's currency.

        """
        query = None
        if scale_qty:
            query = {
                "scaleQty": str(scale_qty)
            }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamilyposition/{account_id}"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_product_position(self, account_ids: [list, int, str] = None, scale_qty: ScaleQty=ScaleQty.DEFAULT):
        """

        Args:
            account_ids: Comma-separated list of Account IDs
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

        Returns: JSON record of product positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs. P&L is expressed in the instrument's currency.

        """
        query = {}

        if account_ids:
            query.update({
                "accountIds": ",".join([str(account_id) for account_id in account_ids]) if isinstance(account_ids, list) else account_ids
            })

        if scale_qty:
            query.update({
                "scaleQty": str(scale_qty)
            })

        if (not account_ids) and (not scale_qty):
            query = None

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productposition"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_product_position_for_account(self, account_id: [int, str], scale_qty: ScaleQty=ScaleQty.DEFAULT):
        """

        Args:
            account_id: Account ID
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

        Returns: JSON record of product positions based on today's fills for the provided accountId. Included in the response are SODs. P&L is expressed in the instrument's currency.

        """
        query = None
        if scale_qty:
            query = {
                "scaleQty": str(scale_qty)
            }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productposition/{account_id}"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_sod(self, account_id, next_page_key=None):
        """
        Args:
            account_id: Account ID
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns: JSON record of SODs for a given account ID.
        """
        query = {}
        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/sod/{account_id}"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_sod(self, account_id):
        """
        Args:
            account_id: Account ID

        Returns: JSON record of all SODs for a given account ID.
        """
        return self._generic_paginated_request(
            self.get_sod,
            results_key="sod",
            account_id=account_id
        )
