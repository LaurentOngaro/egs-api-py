"""
Epic API base implementation
"""

import aiohttp
import logging
from typing import Optional, Dict, Any
from urllib.parse import urljoin

from .types.account import UserData
from .error import *

logger = logging.getLogger(__name__)


class EpicAPI:
    """Base Epic API client"""

    def __init__(self):
        self.user_data = UserData()
        self.session: Optional[aiohttp.ClientSession] = None

    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for requests"""
        headers = {
            "User-Agent": "UELauncher/17.0.1-37584233+++Portal+Release-Live Windows/10.0.19043.1.0.64bit",
            "X-Epic-Correlation-ID": "UE4-c176f7154c2cda1061cc43ab52598e2b-93AFB486488A22FDF70486BD1D883628-BFCD88F649E997BA203FF69F07CE578C"
        }

        if self.user_data.access_token and self.user_data.token_type:
            headers["Authorization"] = f"{self.user_data.token_type} {self.user_data.access_token}"

        return headers

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self._get_headers(), cookie_jar=aiohttp.CookieJar())
        return self.session

    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        session = await self._get_session()

        try:
            async with session.request(method=method, url=url, params=params, data=data, json=json, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    raise InvalidCredentialsError()
                elif response.status == 403:
                    raise FabTimeoutError()
                elif response.status >= 500:
                    raise ServerError()
                else:
                    text = await response.text()
                    logger.warning(f"Request failed with status {response.status}: {text}")
                    raise APIError(f"Request failed with status {response.status}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            raise UnknownError() from e
