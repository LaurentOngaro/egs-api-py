"""
Friends data structures
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class Friend(BaseModel):
    account_id: str
    status: str
    direction: str
    created: datetime
    favorite: bool
    display_name: Optional[str] = None
    alias: Optional[str] = None
    note: Optional[str] = None
