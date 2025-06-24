"""
Entitlement data structures
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class Entitlement(BaseModel):
    id: str
    entitlement_name: str
    namespace: str
    catalog_item_id: str
    account_id: str
    identity_id: str
    entitlement_type: str
    grant_date: datetime
    consumable: bool
    status: str
    active: bool
    use_count: int
    entitlement_source: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    platform_type: Optional[str] = None
    created: datetime
    updated: datetime
