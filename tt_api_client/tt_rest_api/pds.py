from .base_client import TTBaseClient
from .authentication import TTAuthentication

from datetime import datetime, timedelta
import pandas as pd


class TTPdsClient(TTBaseClient):
    endpoint = "ttpds"

    def __init__(self, auth_handler: TTAuthentication):
        super().__init__(auth_handler)

    def get_instrument(self, instrument_id, as_dataframe=False):
        url = f"{self.TT_BASE_URL}/{self.endpoint}/{self.auth_handler.environment.value}/instrument/{instrument_id}"
        response = self._authenticated_get(url)
        json = response.json()

        if not as_dataframe:
            json
        else:
            return pd.DataFrame(json["instrument"])