from .base_client import TTBaseClient
from .authentication import TTAuthentication
from .exceptions import UsageError

import pandas as pd


class TTPdsClient(TTBaseClient):
    endpoint = "ttpds"

    def __init__(self, auth_handler: TTAuthentication):
        super().__init__(auth_handler)

    def get_algo_data(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algodata"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["algoData"])

    def get_algos(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algos"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["algos"])

    def get_algos_user_parameters(self, algo_id, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algos/{algo_id}/userparameters"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["userParameters"])

    def get_currrency_rates(self, to_currency_name=None, from_currency_name=None, as_dataframe=False):
        query = {}
        if to_currency_name and from_currency_name:
            query = {
                "fromCurrencyName": from_currency_name,
                "toCurrencyName": to_currency_name
            }
        elif (to_currency_name is not None) != (from_currency_name is not None):  #  XOR
            raise UsageError("get_currrency_rates can be called with either (a) no args, or (b) with a named pair."
                             + " Calling with no args will results in all currency pairs being returned.")

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/currencyrates"
        response = self._authenticated_get(url, query=query)
        json = response.json()
        print(json)

        if not as_dataframe:
            return json
        else:
            data_frames = {}
            if "currency_rates" in json:
                data_frames["currency_rates"] = pd.DataFrame(json["currency_rates"])

            if "currency_rate" in json:
                data_frames["currency_rate"] = pd.DataFrame(json["currency_rate"], index=[1])

            return data_frames

    def get_currrency_rates_by_id(self, to_currency_id=None, from_currency_id=None, as_dataframe=False):
        query = {}
        if to_currency_id and from_currency_id:
            query = {
                "fromCurrencyName": from_currency_id,
                "toCurrencyName": to_currency_id
            }
        elif (to_currency_id is not None) != (from_currency_id is not None):  #  XOR
            raise UsageError("get_currrency_rates_by_id can be called with either (a) no args, or (b) with an id pair."
                             + " Calling with no args will results in all currency pairs being returned.")

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/currencyrates"
        response = self._authenticated_get(url, query=query)
        json = response.json()
        print(json)

        if not as_dataframe:
            return json
        else:
            data_frames = {}
            if "currency_rates" in json:
                data_frames["currency_rates_id"] = pd.DataFrame(json["currency_rates"])

            if "currency_rate" in json:
                data_frames["currency_rate_id"] = pd.DataFrame(json["currency_rate"], index=[1])

            return data_frames

    def get_instrument(self, instrument_id, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/instrument/{instrument_id}"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["instrument"])

    def get_instrument_data(self):
        raise NotImplementedError()

    def get_instruments(self, product_type_id, product_id=None, alias=None):
        raise NotImplementedError()

    def get_markets(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/markets"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["markets"])

    def get_miccodes(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/miccodes"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["micCodes"])

    def get_mics(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/mics"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["markets"])

    def get_product(self, product_id, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/product/{product_id}"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["product"])

    def get_product_data(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productdata"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return {
                "currencies": pd.DataFrame(json["currencies"]),
                "productTypes": pd.DataFrame(json["productTypes"])
            }

    def get_product_families(self, market_ids, as_dataframe=False):
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
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["productFamilies"])

    def get_product_family(self, product_family_id, as_dataframe=False):
        query = {
            "productFamilyId": product_family_id
        }
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamily"
        response = self._authenticated_get(url, query=query)
        json = response.json()
        print(json)

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["products"])

    def get_product_family_by_id(self, product_family_id, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamily/{product_family_id}"
        response = self._authenticated_get(url)
        json = response.json()
        print(json)

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["productFamily"])

    def get_products(self, market_id, as_dataframe=False):
        query = {
            "marketId": market_id
        }

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/products"
        response = self._authenticated_get(url, query=query)
        json = response.json()
        print(json)

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["products"])

    def get_security_exchanges(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/securityexchanges"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["securityExchanges"])

    def get_synthetic_instruments(self, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/syntheticinstruments"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            return json
        else:
            return pd.DataFrame(json["syntheticInstruments"])
