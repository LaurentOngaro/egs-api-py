"""
Library data structures
"""

from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel


class ResponseMetadata(BaseModel):
    next_cursor: Optional[str] = None


class LibraryRecord(BaseModel):
    app_name: str
    catalog_item_id: str
    namespace: str
    asset_id: str
    app_version: str
    label_name: str
    metadata: Optional[Any] = None
    install_location: Optional[str] = None
    install_size: Optional[int] = None
    main_game_item: Optional[Any] = None
    entitlement_type: str
    entitlement_name: str


class Library(BaseModel):
    records: List[LibraryRecord]
    response_metadata: Optional[ResponseMetadata] = None
