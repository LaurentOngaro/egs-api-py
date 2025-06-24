"""
Asset info data structures
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from urllib.parse import urlparse


class Category(BaseModel):
    path: str


class CustomAttribute(BaseModel):
    type_field: str = Field(alias="type")
    value: str


class ReleaseInfo(BaseModel):
    id: Optional[str] = None
    app_id: Optional[str] = None
    compatible_apps: Optional[List[str]] = None
    platform: Optional[List[str]] = None
    date_added: Optional[datetime] = None
    release_note: Optional[str] = None
    version_title: Optional[str] = None


class KeyImage(BaseModel):
    type_field: str = Field(alias="type")
    url: str
    md5: str
    width: int
    height: int
    size: int
    uploaded_date: datetime


class AssetInfo(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    key_images: Optional[List[KeyImage]] = None
    categories: Optional[List[Category]] = None
    namespace: str
    status: Optional[str] = None
    creation_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    custom_attributes: Optional[Dict[str, CustomAttribute]] = None
    entitlement_name: Optional[str] = None
    entitlement_type: Optional[str] = None
    item_type: Optional[str] = None
    release_info: Optional[List[ReleaseInfo]] = None
    developer: Optional[str] = None
    developer_id: Optional[str] = None
    eula_ids: List[str] = Field(default_factory=list)
    end_of_support: Optional[bool] = None
    dlc_item_list: List['AssetInfo'] = Field(default_factory=list)
    age_gatings: Optional[Any] = None
    application_id: Optional[str] = None
    unsearchable: bool = False
    self_refundable: Optional[bool] = None
    requires_secure_account: Optional[bool] = None
    long_description: Optional[str] = None
    main_game_item: Optional['AssetInfo'] = None
    esrb_game_rating_value: Optional[str] = None
    use_count: Optional[int] = None
    technical_details: Optional[str] = None
    install_modes: List[Any] = Field(default_factory=list)

    def latest_release(self) -> Optional[ReleaseInfo]:
        """Get the latest release by release_date"""
        if releases := self.sorted_releases():
            return releases[0] if releases else None
        return None

    def sorted_releases(self) -> Optional[List[ReleaseInfo]]:
        """Get list of sorted releases newest to oldest"""
        if self.release_info:
            sorted_releases = sorted(self.release_info, key=lambda ri: ri.date_added or datetime.min, reverse=True)
            return sorted_releases
        return None

    def release_info_by_id(self, release_id: str) -> Optional[ReleaseInfo]:
        """Get release info based on the release id"""
        if self.release_info:
            for release in self.release_info:
                if release.id == release_id:
                    return release
        return None

    def release_by_name(self, name: str) -> Optional[ReleaseInfo]:
        """Get release info based on the release name"""
        if self.release_info:
            for release in self.release_info:
                if release.app_id == name:
                    return release
        return None

    def compatible_apps(self) -> Optional[List[str]]:
        """Get list of all compatible apps across all releases"""
        if self.release_info:
            apps = []
            for info in self.release_info:
                if info.compatible_apps:
                    apps.extend(info.compatible_apps)
            return sorted(list(set(apps)))
        return None

    def platforms(self) -> Optional[List[str]]:
        """Get list of all platforms across all releases"""
        if self.release_info:
            platforms = []
            for info in self.release_info:
                if info.platform:
                    platforms.extend(info.platform)
            return sorted(list(set(platforms)))
        return None


class GameToken(BaseModel):
    expires_in_seconds: int
    code: str
    creating_client_id: str


class OwnershipToken(BaseModel):
    token: str
