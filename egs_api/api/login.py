"""
Login/authentication methods
"""

import base64
import logging
from typing import Optional, Dict, Any

from .epic_api import EpicAPI
from .error import *
from .types.account import UserData

logger = logging.getLogger(__name__)


class LoginMixin(EpicAPI):
    """Login functionality for Epic API"""

    async def start_session(self, exchange_token: Optional[str] = None, authorization_code: Optional[str] = None) -> bool:
        """Start a new session with Epic Games"""

        if exchange_token:
            params = {"grant_type": "exchange_code", "exchange_code": exchange_token, "token_type": "eg1"}
        elif authorization_code:
            params = {"grant_type": "authorization_code", "code": authorization_code, "token_type": "eg1"}
        elif self.user_data.refresh_token:
            params = {"grant_type": "refresh_token", "refresh_token": self.user_data.refresh_token, "token_type": "eg1"}
        else:
            raise InvalidCredentialsError("No authentication method provided")

        # Epic client credentials
        client_id = "34a02cf8f4414e29b15921876da36f9a"
        client_secret = "daafbccc737745039dffe53d94fc76cf"

        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

        session = await self._get_session()

        try:
            async with session.post(
                "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                data=params,
                headers={
                    **self._get_headers(), "Authorization": f"Basic {auth_header}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            ) as response:

                if response.status == 500:
                    raise ServerError()

                response_data = await response.json()

                if response.status == 200:
                    new_user_data = UserData.model_validate(response_data)
                    self.user_data.update(new_user_data)

                    if self.user_data.error_message:
                        raise APIError(self.user_data.error_message)

                    return True
                else:
                    error_msg = response_data.get("errorMessage", "Unknown error")
                    raise APIError(error_msg)

        except Exception as e:
            if isinstance(e, EpicAPIError):
                raise
            logger.error(f"Login error: {e}")
            raise UnknownError() from e

    async def resume_session(self) -> bool:
        """Resume existing session"""
        try:
            response_data = await self._make_request("GET", "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/verify")

            new_user_data = UserData.model_validate(response_data)
            self.user_data.update(new_user_data)

            if self.user_data.error_message:
                raise APIError(self.user_data.error_message)

            return True

        except Exception as e:
            logger.error(f"Session resume error: {e}")
            return False

    async def invalidate_session(self) -> bool:
        """Invalidate current session"""
        if not self.user_data.access_token:
            return False

        try:
            session = await self._get_session()
            url = f"https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/sessions/kill/{self.user_data.access_token}"

            async with session.delete(url) as response:
                if response.status == 200:
                    logger.info("Session invalidated")
                    return True
                else:
                    logger.warning(f"Failed to invalidate session: {response.status}")
                    return False

        except Exception as e:
            logger.warning(f"Unable to invalidate session: {e}")
            return False
