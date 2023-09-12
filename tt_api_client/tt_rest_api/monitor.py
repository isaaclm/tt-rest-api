from .rest_client import TTRestClient
from .authenticator import TTAuthenticator


class TTMonitorClient(TTRestClient):
    endpoint = "ttmonitor"

    def __init__(self, auth_handler: TTAuthenticator):
        super().__init__(auth_handler)

    def get_credit_utilization(self, account_id, include_product_pos=None):
        """

        Args:
            account_id: Account ID
            include_product_pos: Include product position

        Returns: JSON record of credit limit and credit utilization details for a given account. For more information on the values returned in this request, consult the TT documentation on credit limit settings.

        """
        query = {
            "accountId": account_id
        }

        if include_product_pos is not None:
            query.update({
                "includeProductPos": str(include_product_pos)
            })

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/creditutilization"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_position(self, account_ids: [None, list, int, str] = None, scale_qty=None):
        """

        Args:
            account_ids: Comma-separated list of Account IDs
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

        Returns: JSON record of positions based on today's fills for the all accounts associated with the application key or for specific accounts. Included in the response are SODs. P&L is expressed in the instrument's currency.

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

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/position"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_position_for_account(self, account_id: [int, str], scale_qty=None):
        """

        Args:
            account_id: Account ID
            scale_qty: Receive position quantities in flow or as a number of contracts. (0 = contracts, 1 = in flow). Instruments whose position can be displayed in flow will default to flow. The scaleQty parameter provides the ability to specify how positions are displayed for these instruments.

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

    def get_product_family_position(self, account_ids: [list, int, str] = None, scale_qty=None):
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

    def get_product_family_position_for_account(self, account_id: [int, str], scale_qty=None):
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

    def get_product_position(self, account_ids: [list, int, str] = None, scale_qty=None):
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

    def get_product_position_for_account(self, account_id: [int, str], scale_qty=None):
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

    def get_sod(self, account_id):
        """

        Args:
            account_id: Account ID

        Returns: JSON record of SODs for a given account ID.

        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/sod/{account_id}"
        response = self._authenticated_get(url)
        return response.json()
