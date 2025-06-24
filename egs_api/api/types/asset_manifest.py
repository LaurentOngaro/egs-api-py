"""
Asset manifest data structures
"""

from typing import List, Optional
from pydantic import BaseModel
from urllib.parse import urlparse


class QueryParam(BaseModel):
    name: str
    value: str


class Manifest(BaseModel):
    uri: str
    queryParams: List[QueryParam]


class Element(BaseModel):
    appName: str
    labelName: str
    buildVersion: str
    hash: str
    manifests: List[Manifest]


class AssetManifest(BaseModel):
    elements: List[Element]
    platform: Optional[str] = None
    label: Optional[str] = None
    namespace: Optional[str] = None
    item_id: Optional[str] = None
    app: Optional[str] = None

    def url_csv(self) -> str:
        """Get comma-separated list of manifest URLs"""
        urls = []
        for elem in self.elements:
            for manifest in elem.manifests:
                urls.append(manifest.uri)
        return ",".join(urls)
