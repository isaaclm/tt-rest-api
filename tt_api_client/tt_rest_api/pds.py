from .base_client import TTBaseClient
from .authentication import TTAuthentication
from .exceptions import UsageError


class TTPdsClient(TTBaseClient):
    endpoint = "ttpds"

    def __init__(self, auth_handler: TTAuthentication):
        super().__init__(auth_handler)

    def get_algo_data(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algodata"
        response = self._authenticated_get(url)
        return response.json()

    def get_algos(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algos"
        response = self._authenticated_get(url)
        return response.json()

    def get_algos_user_parameters(self, algo_id):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algos/{algo_id}/userparameters"
        response = self._authenticated_get(url)
        return response.json()

    def get_currrency_rates(self, to_currency_name=None, from_currency_name=None):
        query = {}
        if to_currency_name and from_currency_name:
            query = {
                "fromCurrencyName": from_currency_name,
                "toCurrencyName": to_currency_name
            }
        elif (to_currency_name is not None) != (from_currency_name is not None):  # XOR
            raise UsageError("get_currrency_rates can be called with either (a) no args, or (b) with a named pair."
                             + " Calling with no args will results in all currency pairs being returned.")

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/currencyrates"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_currrency_rates_by_id(self, to_currency_id=None, from_currency_id=None):
        query = {}
        if to_currency_id and from_currency_id:
            query = {
                "fromCurrencyName": from_currency_id,
                "toCurrencyName": to_currency_id
            }
        elif (to_currency_id is not None) != (from_currency_id is not None):  # XOR
            raise UsageError("get_currrency_rates_by_id can be called with either (a) no args, or (b) with an id pair."
                             + " Calling with no args will results in all currency pairs being returned.")

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/currencyrates"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_instrument(self, instrument_id):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/instrument/{instrument_id}"
        response = self._authenticated_get(url)
        return response.json()

    def get_instrument_data(self):
        raise NotImplementedError()

    def get_instruments(self, product_type_id, product_id=None, alias=None):
        raise NotImplementedError()

    def get_markets(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/markets"
        response = self._authenticated_get(url)
        return response.json()

    def get_miccodes(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/miccodes"
        response = self._authenticated_get(url)
        return response.json()

    def get_mics(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/mics"
        response = self._authenticated_get(url)
        return response.json()

    def get_product(self, product_id):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/product/{product_id}"
        response = self._authenticated_get(url)
        return response.json()

    def get_product_data(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productdata"
        response = self._authenticated_get(url)
        return response.json()

    def get_product_families(self, market_ids):
        # Note: To avoid errors when requesting product data, TT strongly recommends listing a maximum of 10
        if isinstance(market_ids, (list, tuple, set)):
            query = {
                "marketId": market_ids[0] if len(market_ids) == 1 else ",".join([str(market_id) for market_id in market_ids])
            }
        else:
            query = {
                "marketId": market_ids  # assume just a singular value
            }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamilies"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_product_family(self, product_family_id):
        query = {
            "productFamilyId": product_family_id
        }
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamily"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_product_family_by_id(self, product_family_id):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamily/{product_family_id}"
        response = self._authenticated_get(url)
        return response.json()

    def get_products(self, market_id):
        query = {
            "marketId": market_id
        }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/products"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_security_exchanges(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/securityexchanges"
        response = self._authenticated_get(url)
        return response.json()

    def get_synthetic_instruments(self):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/syntheticinstruments"
        response = self._authenticated_get(url)
        return response.json()
