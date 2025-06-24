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

    manifest = await egs.fab_asset_manifest("KiteDemo473", "89efe5924d3d467c839449ab6ab52e7f", "28166226c38a4ff3aa28bbe87dcbbe5b", None)
    print(f"\nKite Demo Manifest: {manifest}\n")

    if manifest:
        for man in manifest:
            for url in man.distribution_point_base_urls:
                print(f"\nTrying to get download manifest from {url}\n")
                try:
                    dm = await egs.fab_download_manifest(man, url)
                    print(f"\nGot download manifest from {url}\n")
                    print(f"\nExpected Hash: {man.manifest_hash}\n")
                    download_hash = dm.custom_field("DownloadedManifestHash") or ""
                    print(f"\nDownload Hash: {download_hash}\n")
                except Exception as e:
                    pass


if __name__ == "__main__":
    asyncio.run(main())
