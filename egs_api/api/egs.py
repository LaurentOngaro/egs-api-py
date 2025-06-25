"""
Epic Games Store API methods
"""

import logging
from typing import List, Optional, Dict
from urllib.parse import urlencode

from .epic_api import EpicAPI
from .error import *
from .types.epic_asset import EpicAsset
from .types.asset_manifest import AssetManifest
from .types.asset_info import AssetInfo, GameToken, OwnershipToken
from .types.download_manifest import DownloadManifest
from .types.library import Library

logger = logging.getLogger(__name__)


class EGSMixin(EpicAPI):
    """Epic Games Store functionality for Epic API"""

    async def assets(self, platform: Optional[str] = None, label: Optional[str] = None) -> List[EpicAsset]:
        """Get list of assets"""
        platform = platform or "Windows"
        label = label or "Live"
        url = f"https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/{platform}?label={label}"

        response_data = await self._make_request("GET", url)
        return [EpicAsset.model_validate(item) for item in response_data]

    async def asset_manifest(
        self,
        platform: Optional[str] = None,
        label: Optional[str] = None,
        namespace: Optional[str] = None,
        item_id: Optional[str] = None,
        app: Optional[str] = None,
    ) -> AssetManifest:
        """Get asset manifest"""
        if not namespace or not item_id or not app:
            raise InvalidParamsError("namespace, item_id, and app are required")

        platform = platform or "Windows"
        label = label or "Live"

        url = f"https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/{platform}/namespace/{namespace}/catalogItem/{item_id}/app/{app}/label/{label}"

        response_data = await self._make_request("GET", url)

        manifest = AssetManifest.model_validate(response_data)
        manifest.platform = platform
        manifest.label = label
        manifest.namespace = namespace
        manifest.item_id = item_id
        manifest.app = app

        return manifest

    async def asset_info(self, asset: EpicAsset) -> Dict[str, AssetInfo]:
        """Get asset information"""
        url = f"https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/namespace/{asset.namespace}/bulk/items?id={asset.catalog_item_id}&includeDLCDetails=true&includeMainGameDetails=true&country=us&locale=lc"

        response_data = await self._make_request("GET", url)

        result = {}
        for key, value in response_data.items():
            result[key] = AssetInfo.model_validate(value)
        return result

    async def game_token(self) -> GameToken:
        """Get game token"""
        url = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange"

        response_data = await self._make_request("GET", url)
        return GameToken.model_validate(response_data)

    async def ownership_token(self, asset: EpicAsset) -> OwnershipToken:
        """Get ownership token for asset"""
        if not self.user_data.account_id:
            raise InvalidCredentialsError("No account ID available")

        url = f"https://ecommerceintegration-public-service-ecomprod02.ol.epicgames.com/ecommerceintegration/api/public/platforms/EPIC/identities/{self.user_data.account_id}/ownershipToken"

        form_data = {"nsCatalogItemId": f"{asset.namespace}:{asset.catalog_item_id}"}

        response_data = await self._make_request("POST", url, data=form_data)
        return OwnershipToken.model_validate(response_data)

    async def library_items(self, include_metadata: bool = False) -> Library:
        """Get library items"""
        library = Library(records=[], response_metadata=None)
        cursor = None

        while True:
            if cursor:
                url = f"https://library-service.live.use1a.on.epicgames.com/library/api/public/items?includeMetadata={include_metadata}&cursor={cursor}"
            else:
                url = f"https://library-service.live.use1a.on.epicgames.com/library/api/public/items?includeMetadata={include_metadata}"

            try:
                response_data = await self._make_request("GET", url)
                page_library = Library.model_validate(response_data)

                library.records.extend(page_library.records)

                if not page_library.response_metadata or not page_library.response_metadata.next_cursor:
                    break

                cursor = page_library.response_metadata.next_cursor

            except Exception as e:
                logger.error(f"Error fetching library page: {e}")
                break

        return library

    async def asset_download_manifests(self, asset_manifest: AssetManifest) -> List[DownloadManifest]:
        """Get download manifests for asset"""
        base_urls = asset_manifest.url_csv()
        result = []

        for element in asset_manifest.elements:
            for manifest in element.manifests:
                query_params = "&".join(f"{param.name}={param.value}" for param in manifest.queryParams)
                url = f"{manifest.uri}?{query_params}"

                try:
                    session = await self._get_session()
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.read()
                            download_manifest = DownloadManifest.parse(data)

                            if download_manifest:
                                # Set custom fields
                                download_manifest.set_custom_field("BaseUrl", base_urls)

                                if asset_manifest.item_id:
                                    download_manifest.set_custom_field("CatalogItemId", asset_manifest.item_id)
                                if asset_manifest.label:
                                    download_manifest.set_custom_field("BuildLabel", asset_manifest.label)
                                if asset_manifest.namespace:
                                    download_manifest.set_custom_field("CatalogNamespace", asset_manifest.namespace)
                                if asset_manifest.app:
                                    download_manifest.set_custom_field("CatalogAssetName", asset_manifest.app)

                                # Extract base URL from manifest URI
                                url_parts = manifest.uri.split('/')
                                if len(url_parts) > 3:
                                    base_url = '/'.join(url_parts[:-1])
                                    download_manifest.set_custom_field("SourceURL", base_url)

                                result.append(download_manifest)
                        else:
                            logger.warning(f"Failed to download manifest: {response.status}")

                except Exception as e:
                    logger.error(f"Error downloading manifest: {e}")

        return result

    async def close(self):
        """Close the aiohttp session if open"""
        if hasattr(self, 'session') and self.session is not None:
            await self.session.close()
            self.session = None
