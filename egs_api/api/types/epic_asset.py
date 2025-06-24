"""
Epic Asset data structure
"""

from pydantic import BaseModel


class EpicAsset(BaseModel):
    app_name: str
    label_name: str
    build_version: str
    catalog_item_id: str
    namespace: str
    asset_id: str
