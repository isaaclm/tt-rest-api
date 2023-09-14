from .rest_client import TTRestClient
from .authenticator import TTAuthenticator
from .exceptions import UsageError

import logging

log = logging.getLogger()


class TTPdsClient(TTRestClient):
    endpoint = "ttpds"

    def __init__(self, auth_handler: TTAuthenticator):
        super().__init__(auth_handler)

    def get_algo_data(self):
        """
        Retrieves definitions for algo user parameters-related enumerated values.

        Returns:
            dict: JSON response containing algo user parameters.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algodata"
        response = self._authenticated_get(url)
        return response.json()

    def get_algos(self):
        """
        Gets a list of algos.

        Returns:
            dict: JSON response containing a list of algos.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algos"
        response = self._authenticated_get(url)
        return response.json()

    def get_algos_user_parameters(self, algo_id):
        """
        Gets algo user parameters.

        Args:
            algo_id: An algo id.

        Returns:
            dict: JSON response containing algo user parameters.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/algos/{algo_id}/userparameters"
        response = self._authenticated_get(url)
        return response.json()

    def get_currrency_rates_by_name(self, to_currency_name=None, from_currency_name=None):
        """
        Retrieves the rate of exchange between currencies. If names are given then a rate between these named currencies
        will be returned. If currency names are not given then the exchange rates between all currencies will be
        returned. Note that this methods can return a very large amount of data that can take 30 seconds or more to
        retrieve.

        Args:
            from_currency_name: Optional, a three letter currency code.
            to_currency_name: Optional, a three letter currency code.

        Returns:
            dict: JSON response containing exchange rates between currencies.
        """
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
        """
        Retrieves the rate of exchange between currencies. If ids are given then a rate between these currencies
        will be returned. If currency ids are not given then the exchange rates between all currencies will be
        returned. Note that this methods can return a very large amount of data that can take 30 seconds or more to
        retrieve.

        Args:
            to_currency_id: Optional, a Currency ID.
            from_currency_id: Optional, a Currency ID.

        Returns:
            dict: JSON response containing exchange rates between currencies.
        """
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
        """
        Gets detailed information about an individual instrument given its ID. This endpoint now includes additional
        information related to ASE synthetic instruments. The ttpds endpoint also include a /syntheticinstruments
        endpoint which allows users to retrieve a list of available synthetic instruments.

        Note For all contracts, the alias field for leg contracts shows the instrument name which contains both the
        contract name and expiry (e.g., GE Jun22). The term field maps directly to the series term (e.g., Jun22).

        Note This endpoint should not be used to create multiple individual requests for a number of instruments from
        the same ProductID and productTypeID. These instruments can be accessed with a single request to /instruments.

        Args:
            instrument_id: An Instrument ID. Can be retrieved by the /instruments GET request.

        Returns:
            dict: JSON response containing detailed information about an individual instrument.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/instrument/{instrument_id}"
        response = self._authenticated_get(url)
        return response.json()

    def get_instrument_data(self):
        """
        Gets instrument reference data.

        Returns:
            dict: JSON response containing instrument reference data.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/instrumentdata"
        response = self._authenticated_get(url)
        return response.json()

    def get_instruments(self, product_type_id=None, product_id=None, alias=None, next_page_key=None):
        """
        Gets a list of instruments given a product type ID or a product ID.

        Note: Requires a value populated in either the productId or alias parameter. The productTypeId parameter does
        not return any instruments when used by itself.

        Args:
            product_type_id: Product type ID. Can be retrieved by the /productdata GET request.
            product_id: Filter response to fills for a specific product. Product ID can be retrieved using the ttpds
                        service's /products GET request.
            alias: An alias
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict: JSON response containing a list of instruments.
        """
        if (product_type_id is not None) and (sum(param is not None for param in [product_id, alias]) == 0):
            raise UsageError("Requires a value populated in either the product_id or alias parameter. The \
                              product_type_id parameter does not return any instruments when used by itself.")

        query = {}

        if product_type_id is not None:
            query.update({"productTypeId": product_type_id})

        if product_id is not None:
            query.update({"productId": product_id})
        else:
            query.update({"alias": alias})

        if next_page_key is not None:
            query.update({"nextPageKey": str(next_page_key)})

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/instruments"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_instruments(self, product_type_id=None, product_id=None, alias=None):
        """
        Gets a list of instruments given a product type ID or a product ID.

        Note: Requires a value populated in either the productId or alias parameter. The productTypeId parameter does
        not return any instruments when used by itself.

        Args:
            product_type_id: Product type ID. Can be retrieved by the /productdata GET request.
            product_id: Filter response to fills for a specific product. Product ID can be retrieved using the ttpds
                        service's /products GET request.
            alias: An alias

        Returns:
            dict: JSON response containing a list of instruments.
        """
        return self._generic_paginated_request(
            self.get_instruments,
            results_key="instruments",
            product_type_id=product_type_id,
            product_id=product_id,
            alias=alias
        )

    def get_markets(self):
        """
        Gets the list of markets.

        Returns:
            dict: JSON response containing a list of markets.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/markets"
        response = self._authenticated_get(url)
        return response.json()

    def get_miccodes(self):
        """
        Gets a list of Market Identification Codes (MIC).

        Returns:
            dict: JSON response containing a list of Market Identification Codes (MIC).
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/miccodes"
        response = self._authenticated_get(url)
        return response.json()

    def get_mics(self):
        """
        Gets a list of Market Identification Codes (MIC).

        Returns:
            dict: JSON response containing a list of Market Identification Codes (MIC).
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/mics"
        response = self._authenticated_get(url)
        return response.json()

    def get_product(self, product_id):
        """
        Gets detailed information about a product given its ID.

        Args:
            alias: A Product ID.

        Returns:
            dict: JSON response containing a list of instruments.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/product/{product_id}"
        response = self._authenticated_get(url)
        return response.json()

    def get_product_data(self):
        """
        Gets product reference data.

        Returns:
            dict: JSON response containing product reference data.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productdata"
        response = self._authenticated_get(url)
        return response.json()

    def get_product_families(self, market_ids):
        """
        Gets product families associated with specific markets

        Args:
            market_ids: A Market ID.

        Returns:
            dict: JSON response containing a list of product families.
        """
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
        """
        Gets details about a product family and lists products within that family.

        Args:
            product_family_id: A Product Family ID.

        Returns:
            dict: JSON response containing product family details and lists products within that family.
        """
        query = {
            "productFamilyId": product_family_id
        }
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamily"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_product_family_by_id(self, product_family_id):
        """
        Gets details about a product family.

        Args:
            product_family_id: A Product Family ID.

        Returns:
            dict: JSON response containing product family details.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/productfamily/{product_family_id}"
        response = self._authenticated_get(url)
        return response.json()

    def get_products(self, market_id, next_page_key=None):
        """
        Gets a list of products for a given market.

        Args:
            market_id: A Market ID.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        Returns:
            dict: JSON response containing a list of products.
        """
        query = {
            "marketId": market_id
        }

        if next_page_key is not None:
            query.update({
                "nextPageKey": str(next_page_key)
            })

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/products"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_products(self, market_id):
        """
        Gets a list of products for a given market.

        Args:
            market_id: A Market ID.

        Returns:
            dict: JSON response containing a list of products.
        """
        return self._generic_paginated_request(
            self.get_products,
            results_key="products",
            market_id=market_id
        )

    def get_security_exchanges(self):
        """
        Gets the list of security exchanges.

        Returns:
            dict: JSON response containing a list of security exchanges.
        """
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/securityexchanges"
        response = self._authenticated_get(url)
        return response.json()

    def get_synthetic_instruments(self, next_page_key=None):
        """
        Gets a list of synthetic instruments.

        Returns:
            dict: JSON response containing a list of synthetic instruments.
            next_page_key: Key used to request the next page of data following a prior request. Responses are limited to around 500 records. Included in the response is a field named 'lastPage' which indicates if a response is the final page of the data requested. If a response is not the final page, the 'lastPage' value will be 'false' and the key needed to request the next page will be included as the 'nextPageKey' value of the response.

        """
        if next_page_key is not None:
            query = { "nextPageKey": str(next_page_key) }
        else:
            query = None

        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/syntheticinstruments"
        response = self._authenticated_get(url, query=query)
        return response.json()

    def get_all_synthetic_instruments(self):
        """
        Gets a list of synthetic instruments.

        Returns:
            dict: JSON response containing a list of synthetic instruments.
        """
        return self._generic_paginated_request(
            self.get_synthetic_instruments,
            results_key="syntheticInstruments"
        )

