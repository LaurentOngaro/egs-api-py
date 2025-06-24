"""
API modules
"""

from .epic_api import EpicAPI
from .login import LoginMixin
from .account import AccountMixin
from .egs import EGSMixin
from .fab import FabMixin


# Combined API class with all mixins
class CombinedAPI(LoginMixin, AccountMixin, EGSMixin, FabMixin):
    """Combined Epic API with all functionality"""
    pass


__all__ = ["EpicAPI", "LoginMixin", "AccountMixin", "EGSMixin", "FabMixin", "CombinedAPI"]
