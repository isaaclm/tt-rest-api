from enum import Enum


class TTEnvironments(Enum):
    """
    Enumeration for Trading Technologies API environments.

    Attributes:
        UAT (str): User Acceptance Testing environment.
        LIVE (str): Production environment.
    """

    UAT = "ext_uat_cert"
    LIVE = "ext_prod_live"
