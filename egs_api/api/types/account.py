"""
Account related data structures
"""

from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field


class AuthId(BaseModel):
    id: str
    type_field: str = Field(alias="type")


class ExternalAuth(BaseModel):
    accountId: str
    authIds: List[AuthId]
    dateAdded: Optional[str] = None
    avatar: Optional[str] = None
    externalAuthId: Optional[str] = None
    externalAuthIdType: Optional[str] = None
    externalDisplayName: str
    typeField: str = Field(alias="type")
    externalAuthSecondaryId: Optional[str] = None


class AccountData(BaseModel):

    id: str
    displayName: str
    name: str
    email: str
    affiliationType: str
    failedLoginAttempts: int
    lastLogin: str
    numberOfDisplayNameChanges: int
    ageGroup: str
    headless: bool
    country: str
    countryUpdatedTime: str
    lastName: str
    phoneNumber: str
    company: str
    preferredLanguage: str
    canUpdateDisplayName: bool
    tfaEnabled: bool
    emailVerified: bool
    minorVerified: bool
    minorExpected: bool
    minorStatus: str
    cabinedMode: bool
    hasHashedEmail: bool
    lastReviewedSecuritySettings: str
    lastDeclinedMFASetup: str
    lastReviewedLinkConsole: str


class AccountInfo(BaseModel):
    displayName: str
    externalAuths: Dict[str, ExternalAuth]
    id: str


class UserData(BaseModel):
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    expires_at: Optional[datetime] = None
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    refresh_expires: Optional[int] = None
    refresh_expires_at: Optional[datetime] = None
    account_id: Optional[str] = None
    client_id: Optional[str] = None
    internal_client: Optional[bool] = None
    client_service: Optional[str] = None
    displayName: Optional[str] = None
    app: Optional[str] = None
    in_app_id: Optional[str] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None

    def update(self, new_data: 'UserData') -> None:
        """Update only present values in the existing user data"""
        for field, value in new_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(self, field, value)
