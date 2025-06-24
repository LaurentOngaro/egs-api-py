"""
FAB library data structures
"""

from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel


class FabCursors(BaseModel):
    next: Optional[str] = None


class ProjectVersion(BaseModel):
    artifact_id: str
    version: str
    created_date: datetime
    updated_date: datetime


class FabLibraryItem(BaseModel):
    asset_id: str
    asset_namespace: str
    title: str
    description: Optional[str] = None
    project_versions: List[ProjectVersion]
    tags: List[str] = []
    category: Optional[str] = None
    created_date: datetime
    updated_date: datetime


class FabLibrary(BaseModel):
    results: List[FabLibraryItem] = []
    cursors: FabCursors = FabCursors()
