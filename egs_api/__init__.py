# coding=utf-8
"""
Epic Games Store API Client

A minimal asynchronous interface to Epic Games Store
"""

from .epic_games import EpicGames
from .api.error import EpicAPIError
from .api.types.account import AccountData, AccountInfo, UserData
from .api.types.epic_asset import EpicAsset
from .api.types.asset_info import AssetInfo, GameToken, OwnershipToken
from .api.types.asset_manifest import AssetManifest
from .api.types.download_manifest import DownloadManifest
from .api.types.entitlement import Entitlement
from .api.types.library import Library
from .api.types.fab_library import FabLibrary
from .api.types.fab_asset_manifest import DownloadInfo
from .api.types.friends import Friend

__all__ = [
    "EpicGames", "EpicAPIError", "AccountData", "AccountInfo", "UserData", "EpicAsset", "AssetInfo", "GameToken", "OwnershipToken", "AssetManifest",
    "DownloadManifest", "Entitlement", "Library", "FabLibrary", "DownloadInfo", "Friend",
]

import datetime

year = datetime.date.today().year
__name__ = "egs-api-py"
__version__ = "0.9.4"
__author__ = "Laurent Ongaro"
__codename__ = "v" + __version__
__author_email__ = 'laurent@gameamea.com'
__description__ = 'A minimal asynchronous interface to Epic Games Store in python new FAB marketplace API.'
__copyright__ = f'{year} {__author__}'
__license__ = 'MIT'
__url__ = 'https://github.com/LaurentOngaro/egs-api-py'
