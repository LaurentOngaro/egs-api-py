"""
Epic Games Store API Client

Main client class for interacting with Epic Games Store
"""

import logging
from datetime import datetime, timezone
from typing import Optional, List

from .api import CombinedAPI
from .api.error import *
from .api.types.account import UserData, AccountData, AccountInfo
from .api.types.epic_asset import EpicAsset
from .api.types.asset_info import AssetInfo, GameToken
from .api.types.asset_manifest import AssetManifest
from .api.types.download_manifest import DownloadManifest
from .api.types.entitlement import Entitlement
from .api.types.library import Library
from .api.types.fab_library import FabLibrary
from .api.types.fab_asset_manifest import DownloadInfo
from .api.types.friends import Friend

logger = logging.getLogger(__name__)


class EpicGames:
    """Epic Games Store API Client"""

    def __init__(self):
        self.api = CombinedAPI()

    async def close(self):
        """Close the API session"""
        await self.api.close()

    def is_logged_in(self) -> bool:
        """Check whether the user is logged in"""
        if self.api.user_data.expires_at:
            now = datetime.now(timezone.utc)
            td = self.api.user_data.expires_at - now
            return td.total_seconds() > 600
        return False

    def user_details(self) -> UserData:
        """Get user details"""
        return self.api.user_data

    def set_user_details(self, user_details: UserData) -> None:
        """Update user details"""
        self.api.user_data.update(user_details)

    async def auth_code(self, exchange_token: Optional[str] = None, authorization_code: Optional[str] = None) -> bool:
        """Start session with auth code"""
        try:
            return await self.api.start_session(exchange_token, authorization_code)
        except EpicAPIError:
            return False

    async def logout(self) -> bool:
        """Invalidate existing session"""
        return await self.api.invalidate_session()

    async def login(self) -> bool:
        """Perform login based on previous authentication"""

        # Try to reuse existing session
        if self.api.user_data.expires_at:
            now = datetime.now(timezone.utc)
            td = self.api.user_data.expires_at - now
            if td.total_seconds() > 600:
                logger.info("Trying to re-use existing login session...")
                try:
                    success = await self.api.resume_session()
                    if success:
                        logger.info("Logged in")
                        return True
                except EpicAPIError as e:
                    logger.warning(f"Session resume failed: {e}")

        # Try refresh token
        logger.info("Logging in...")
        if self.api.user_data.refresh_expires_at:
            now = datetime.now(timezone.utc)
            td = self.api.user_data.refresh_expires_at - now
            if td.total_seconds() > 600:
                try:
                    success = await self.api.start_session()
                    if success:
                        logger.info("Logged in")
                        return True
                except EpicAPIError as e:
                    logger.error(f"Refresh login failed: {e}")

        return False

    async def list_assets(self, platform: Optional[str] = None, label: Optional[str] = None) -> List[EpicAsset]:
        """Returns all assets"""
        try:
            return await self.api.assets(platform, label)
        except EpicAPIError:
            return []

    async def asset_manifest(
        self,
        platform: Optional[str] = None,
        label: Optional[str] = None,
        namespace: Optional[str] = None,
        item_id: Optional[str] = None,
        app: Optional[str] = None,
    ) -> Optional[AssetManifest]:
        """Return asset manifest"""
        try:
            return await self.api.asset_manifest(platform, label, namespace, item_id, app)
        except EpicAPIError:
            return None

    async def fab_asset_manifest(self, artifact_id: str, namespace: str, asset_id: str, platform: Optional[str] = None, ) -> List[DownloadInfo]:
        """Return FAB asset manifest"""
        return await self.api.fab_asset_manifest(artifact_id, namespace, asset_id, platform)

    async def asset_info(self, asset: EpicAsset) -> Optional[AssetInfo]:
        """Returns info for an asset"""
        try:
            info_dict = await self.api.asset_info(asset)
            return info_dict.get(asset.catalog_item_id)
        except EpicAPIError:
            return None

    async def account_details(self) -> Optional[AccountData]:
        """Returns account details"""
        try:
            return await self.api.account_details()
        except EpicAPIError:
            return None

    async def account_ids_details(self, ids: List[str]) -> Optional[List[AccountInfo]]:
        """Returns account id info"""
        try:
            return await self.api.account_ids_details(ids)
        except EpicAPIError:
            return None

    async def account_friends(self, include_pending: bool = False) -> Optional[List[Friend]]:
        """Returns friends list"""
        try:
            return await self.api.account_friends(include_pending)
        except EpicAPIError:
            return None

    async def game_token(self) -> Optional[GameToken]:
        """Returns game token"""
        try:
            return await self.api.game_token()
        except EpicAPIError:
            return None

    async def ownership_token(self, asset: EpicAsset) -> Optional[str]:
        """Returns ownership token for an Asset"""
        try:
            token = await self.api.ownership_token(asset)
            return token.token
        except EpicAPIError:
            return None

    async def user_entitlements(self) -> List[Entitlement]:
        """Returns user entitlements"""
        try:
            return await self.api.user_entitlements()
        except EpicAPIError:
            return []

    async def library_items(self, include_metadata: bool = False) -> Optional[Library]:
        """Returns the user library"""
        try:
            return await self.api.library_items(include_metadata)
        except EpicAPIError:
            return None

    async def fab_library_items(self, account_id: str) -> Optional[FabLibrary]:
        """Returns the user FAB library"""
        try:
            return await self.api.fab_library_items(account_id)
        except EpicAPIError:
            return None

    async def asset_download_manifests(self, manifest: AssetManifest) -> List[DownloadManifest]:
        """Returns DownloadManifests for a specified file manifest"""
        return await self.api.asset_download_manifests(manifest)

    async def fab_download_manifest(self, download_info: DownloadInfo, distribution_point_url: str) -> DownloadManifest:
        """Return a Download Manifest for specified FAB download and url"""
        return await self.api.fab_download_manifest(download_info, distribution_point_url)
