#!/usr/bin/env python3
import asyncio
import webbrowser
import logging
from egs_api import EpicGames


async def main():
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Open browser for login
    login_url = "https://www.epicgames.com/id/login?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Fapi%2Fredirect%3FclientId%3D34a02cf8f4414e29b15921876da36f9a%26responseType%3Dcode"
    try:
        webbrowser.open(login_url)
    except:
        print(f"\nPlease go to {login_url}\n")

    print("Please enter the 'authorizationCode' value from the JSON response")
    sid = input().strip().replace('"', '')
    egs = EpicGames()
    print(f"\nUsing Auth Code: {sid}\n")

    if await egs.auth_code(None, sid):
        print("Successfully authenticated")
    else:
        print("Authentication failed")
        return

    try:
        await egs.login()
    except Exception as e:
        print(f"\nLogin failed: {e}\n")
        return

    details = await egs.account_details()
    print(f"\nAccount details: {details}\n")

    user_details = egs.user_details()
    account_id = user_details.account_id if user_details.account_id else ""
    info = await egs.account_ids_details([account_id])
    print(f"\nAccount info: {info}\n")

    manifest = None

    try:
        """
        some data from the EGS catalog
        Stylized Character Kit: Casual 01
        app_id: Stylizedc5eba030d95dV1
        id: c65f5de5e8234af6b3742fa40357ef14
        CatalogAssetName	"Stylizedc5eba030d95dV1"
        CatalogItemId	"c5eba030d95d4bc293e91818a87167e2"
        """
        manifest = await egs.asset_manifest(item_id="c5eba030d95d4bc293e91818a87167e2", namespace="ue", app="Stylizedc5eba030d95dV1")
        print(f"\nStylized Character Manifest: {manifest}\n")
    except Exception as e:
        print(f"\nFailed to get EGS asset manifest: {e}\n")
    """
    // trying to get the manifest using FAB
    // for "Stylized Character Kit: Casual 01"
    //DO NOT USE THIS, IT IS NOT WORKING
    try:
        manifest = await egs.fab_asset_manifest("Stylizedc5eba030d95dV1", "ue", "c5eba030d95d4bc293e91818a87167e2", None)
        print(f"\nStylized Character Manifest: {manifest}\n")
    except Exception as e:
        print(f"\nFailed to get FAB asset manifest: {e}\n")

    try:
        manifest = await egs.fab_asset_manifest("c5eba030d95d4bc293e91818a87167e2", "ue", "c5eba030d95d4bc293e91818a87167e2", None)
        print(f"\nStylized Character Manifest: {manifest}\n")
    except Exception as e:
        print(f"\nFailed to get FAB asset manifest: {e}\n")
    """


if __name__ == "__main__":
    asyncio.run(main())
