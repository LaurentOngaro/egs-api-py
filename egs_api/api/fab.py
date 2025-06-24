"""
FAB (Fab.com) API methods
"""

import logging
from typing import List, Optional
from datetime import datetime

from .epic_api import EpicAPI
from .error import *
from .types.fab_library import FabLibrary
from .types.fab_asset_manifest import DownloadInfo, FabAssetManifest
from .types.download_manifest import DownloadManifest

logger = logging.getLogger(__name__)


class FabMixin(EpicAPI):
    """FAB functionality for Epic API"""

    async def fab_asset_manifest(self, artifact_id: str, namespace: str, asset_id: str, platform: Optional[str] = None) -> List[DownloadInfo]:
        """Get FAB asset manifest"""
        url = f"https://www.fab.com/e/artifacts/{artifact_id}/manifest"
        print(f"Fetching FAB asset manifest from {url}")  # debugging line
        json_data = {"item_id": asset_id, "namespace": namespace, "platform": platform or "Windows"}

        try:
            response_data = await self._make_request("POST", url, json=json_data)
            manifest = FabAssetManifest.model_validate(response_data)
            return manifest.download_info

        except FabTimeoutError:
            raise
        except Exception as e:
            logger.error(f"Error getting FAB asset manifest: {e}")
            raise UnknownError() from e

    async def fab_download_manifest(self, download_info: DownloadInfo, distribution_point_url: str) -> DownloadManifest:
        """Get FAB download manifest"""
        distribution_point = download_info.get_distribution_point_by_base_url(distribution_point_url)

        if not distribution_point:
            logger.error("Distribution point not found")
            raise UnknownError()

        if distribution_point.signature_expiration < datetime.now():
            logger.error("Expired signature")
            raise UnknownError()

        try:
            session = await self._get_session()
            async with session.get(distribution_point.manifest_url) as response:
                if response.status == 200:
                    data = await response.read()
                    manifest = DownloadManifest.parse(data)

                    if not manifest:
                        logger.error("Unable to parse the Download Manifest")
                        raise UnknownError()

                    return manifest
                else:
                    logger.warning(f"Request failed with status {response.status}")
                    raise UnknownError()

        except Exception as e:
            logger.error(f"Error downloading FAB manifest: {e}")
            raise UnknownError() from e

    async def fab_library_items(self, account_id: str) -> FabLibrary:
        """Get FAB library items"""
        library = FabLibrary()

        while True:
            if library.cursors.next:
                url = f"https://www.fab.com/e/accounts/{account_id}/ue/library?cursor={library.cursors.next}&count=100"
            else:
                url = f"https://www.fab.com/e/accounts/{account_id}/ue/library?count=100"

            try:
                response_data = await self._make_request("GET", url)
                page_library = FabLibrary.model_validate(response_data)

                library.results.extend(page_library.results)
                library.cursors.next = page_library.cursors.next

                if not library.cursors.next:
                    break

            except Exception as e:
                logger.error(f"Error fetching FAB library page: {e}")
                library.cursors.next = None
                break

        return library
