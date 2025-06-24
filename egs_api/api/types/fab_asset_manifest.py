"""
FAB asset manifest data structures
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class DistributionPoint(BaseModel):
    manifest_url: str
    signature_expiration: datetime


class DownloadInfo(BaseModel):
    manifest_hash: str
    distribution_point_base_urls: List[str]
    distribution_points: List[DistributionPoint]

    def get_distribution_point_by_base_url(self, base_url: str) -> Optional[DistributionPoint]:
        """Get distribution point by base URL"""
        for point in self.distribution_points:
            if base_url in point.manifest_url:
                return point
        return None


class FabAssetManifest(BaseModel):
    download_info: List[DownloadInfo]
