"""
Account related API methods
"""

import logging
from typing import List, Optional
from urllib.parse import urlencode

from .epic_api import EpicAPI
from .error import *
from .types.account import AccountData, AccountInfo
from .types.friends import Friend
from .types.entitlement import Entitlement

logger = logging.getLogger(__name__)


class AccountMixin(EpicAPI):
    """Account functionality for Epic API"""

    async def account_details(self) -> AccountData:
        """Get account details for current user"""
        if not self.user_data.account_id:
            raise InvalidParamsError("No account ID available")

        url = f"https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/{self.user_data.account_id}"

        response_data = await self._make_request("GET", url)
        return AccountData.model_validate(response_data)

    async def account_ids_details(self, ids: List[str]) -> List[AccountInfo]:
        """Get account details for multiple account IDs"""
        if not ids:
            raise InvalidParamsError("Account IDs list is empty")

        query_params = "&".join(f"accountId={account_id}" for account_id in ids)
        url = f"https://account-public-service-prod03.ol.epicgames.com/account/api/public/account?{query_params}"

        response_data = await self._make_request("GET", url)
        return [AccountInfo.model_validate(item) for item in response_data]

    async def account_friends(self, include_pending: bool = False) -> List[Friend]:
        """Get friends list for current user"""
        if not self.user_data.account_id:
            raise InvalidParamsError("No account ID available")

        url = f"https://friends-public-service-prod06.ol.epicgames.com/friends/api/public/friends/{self.user_data.account_id}?includePending={include_pending}"

        response_data = await self._make_request("GET", url)
        return [Friend.model_validate(item) for item in response_data]

    async def user_entitlements(self) -> List[Entitlement]:
        """Get user entitlements"""
        if not self.user_data.account_id:
            raise InvalidCredentialsError("No account ID available")

        url = f"https://entitlement-public-service-prod08.ol.epicgames.com/entitlement/api/account/{self.user_data.account_id}/entitlements?start=0&count=5000"

        response_data = await self._make_request("GET", url)
        return [Entitlement.model_validate(item) for item in response_data]
