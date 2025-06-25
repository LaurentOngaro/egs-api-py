#!/usr/bin/env python3
import asyncio
import webbrowser
import logging
from egs_api import EpicGames, EpicAsset


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

    print(f"\n*****\nGetting account details\n*****\n")
    details = await egs.account_details()
    print(f"\nAccount details: {details}\n")

    print(f"\n*****\nGetting user details\n*****\n")
    user_details = egs.user_details()
    account_id = user_details.account_id if user_details.account_id else ""
    info = await egs.account_ids_details([account_id])
    print(f"\nAccount info: {info}\n")

    print(f"\n*****All items of Fab library\n*****\n")
    try:
        items = await egs.fab_library_items(account_id=account_id)
        print(f"\nFab library items: {items}\n")
    except Exception as e:
        print(f"\nFailed to get fab library items: {e}\n")
    """
    Exemple of a full data set from the EGS catalog API for "Unreal.js"
    fab url: https://www.fab.com/listings/9fa01ca3-2d5a-4bfa-a1c2-5a41e82eb196

    "id": "be751eedc4a14cc09e39945bc5a531c4"
    , "catalogItemId": "d90f92a8b9aa491da359666fa05b7cbb"
    , "namespace": "ue"
    , "title": "Unreal.js"
    , "recurrence": "ONCE"
    , "currencyCode": "USD"
    , "priceValue": 0
    , "keyImages": [{"type": "Screenshot" , "url": "https://cdn1.epicgames.com/ue/item/UnrealJSScreenshot01-1920x1080-0de33736653a1c908944e2f45c90a534.png" , "md5": "0de33736653a1c908944e2f45c90a534" , "width": 1920, "height": 1080, "size": 390693, "uploadedDate": "2016-05-26T14:26:31.994Z"}, {"type": "Screenshot" , "url": "https://cdn1.epicgames.com/ue/item/UnrealJSScreenshot1-1920x1080-2c0284b1c0f590b90c5457e1381b0c93.png" , "md5": "2c0284b1c0f590b90c5457e1381b0c93" , "width": 1920, "height": 1080, "size": 933171, "uploadedDate": "2016-05-26T14:26:36.288Z"}, {"type": "Thumbnail" , "url": "https://cdn1.epicgames.com/ue/item/UnrealJS_Thumb-288x288-9966133f072a1c9812c81cf1e3bd4ec3.png" , "md5": "9966133f072a1c9812c81cf1e3bd4ec3" , "width": 288, "height": 288, "size": 11167, "uploadedDate": "2016-05-26T14:25:21.061Z"}, {"type": "Featured" , "url": "https://cdn1.epicgames.com/ue/item/UnrealJS_Featured-476x246-8f909f896a43427df3ede8eb8f471933.png" , "md5": "8f909f896a43427df3ede8eb8f471933" , "width": 476, "height": 246, "size": 11202, "uploadedDate": "2016-05-26T14:25:34.195Z"}, {"type": "NewFeatured" , "url": "https://cdn1.epicgames.com/ue/item/UnrealJS_FeaturedNew-894x488-69cb77d78e9190f2d8aa7afe21e5fd1b.png" , "md5": "69cb77d78e9190f2d8aa7afe21e5fd1b" , "width": 894, "height": 488, "size": 14021, "uploadedDate": "2016-05-26T14:25:31.652Z"}]
    , "viewableDate": "2016-09-01T00:00:00.000Z"
    , "effectiveDate": "2016-09-01T00:00:00.000Z"
    , "seller": {"id": "o-5310866e1f49cc9230934e0fa67baa" , "noAi": true, "owner": "00b8a74277dc4fa0b049292075c5da7d" , "status": "ACTIVE" , "financeCheckExempted": true, "name": "NCSOFT Corporation" , "supportEmail": "unrealjs-support@ncsoft.com" , "website": "http://global.ncsoft.com/global/" , "facebook": "" , "twitter": "" , "blog": "" , "otherLink": ""}
    , "description": "Javascript runtime built for UnrealEngine"
    , "technicalDetails": "<p><strong>Modules</strong>:</p><ul><li>V8 (Runtime)</li><li>JavascriptUMG (Runtime)</li><li>JavascriptHttp (Runtime)</li><li>JavascriptWebSocket (Runtime)</li><li>JavascriptEditor (Editor)</li><li>JavascriptConsole (Editor)</li></ul><p><strong>Features</strong>:</p><ul><li>Powered by latest V8 (ES6)</li><li>CommonJS modules</li><li>Full access to the whole UnrealEngine API</li><li>Free to subclass existing classes including blueprint</li><li>Web-dev like UMG (Jade, pseudo-css, pseudo-angular.js, React)</li><li>Live reload &lt;br /&gt;\u2022 Communicate with outer world: REST(http), websocket, process(pipe), arraybuffer, etc.</li><li>Bridge API for editor extension</li><li>Auto-completion for Visual Studio Code (auto-generated *.d.ts)</li><li>Debugging within Visual Studio, Visual Studio Code, WebStorm, V8 Inspector and all IDE which supports V8 protocol</li><li>Profiling supported by V8</li><li>Dedicated JavaScript console on UnrealEditor</li><li>(Full) access to existing JavaScript libraries via npm, bower, etc.</li></ul><p><strong>Platforms Tested</strong>: Windows, Mac</p><p><strong>Intended Platforms</strong>: Windows, Mac</p><p><strong>Documentation</strong>: <a href=\"https://github.com/ncsoft/Unreal.js/wiki\" rel=\"noreferrer noopener\">https://github.com/ncsoft/Unreal.js/wiki</a></p><p><strong>Example Project</strong>: <a href=\"https://drive.google.com/file/d/0B8EsJUQpOkucRVJna3dEczJHN2M\" rel=\"noreferrer noopener\">https://drive.google.com/file/d/0B8EsJUQpOkucRVJna3dEczJHN2M</a></p>"
    , "longDescription": "<p><strong>Preview</strong>:\u00a0<a href=\"https://www.youtube.com/watch?v=QDEy71oiHOg\" rel=\"noreferrer noopener\">https://www.youtube.com/watch?v=QDEy71oiHOg</a></p><p><strong>Unreal.js is a plug-in which brings V8-powered JavaScript into Unreal Engine 4.</strong></p>"
    , "isFeatured": false
    , "isCatalogItem": false
    , "categories": [{"path": "assets/codeplugins" , "name": "Code Plugins"}]
    , "bundle": false
    , "releaseInfo": [
        {"id": "94b6402e31e34ad78ac7c7a19b4348d9" , "appId": "UnrealJS_4.11" , "compatibleApps": ["UE_4.11"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2016-05-18T00:00:00.000Z" , "versionTitle": "UnrealJS_4.11"}, {"id": "5790ba8b29c645349f7750ae8e98b679" , "appId": "UnrealJS_4.12" , "compatibleApps": ["UE_4.12"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2016-08-09T00:00:00.000Z" , "versionTitle": "UnrealJS_4.12"}, {"id": "3347d8d592c343c3942f59a347b4fbc2" , "appId": "UnrealJS_4.13" , "compatibleApps": ["UE_4.13"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2016-09-02T00:00:00.000Z" , "versionTitle": "UnrealJS_4.13"}, {"id": "7a658a3d50d04a12aed416249605ea39" , "appId": "UnrealJS_4.14" , "compatibleApps": ["UE_4.14"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2016-11-26T00:00:00.000Z" , "versionTitle": "UnrealJS_4.14"}
      , {"id": "2dbd2e9fd70c4272a1275fa1b35ecacf" , "appId": "UnrealJS_4.15" , "compatibleApps": ["UE_4.15"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2017-04-18T00:00:00.000Z" , "versionTitle": "UnrealJS_4.15"}
      , {"id": "437bdaba4182483c80de7cf59af851cb" , "appId": "UnrealJS_4.16" , "compatibleApps": ["UE_4.16"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2017-09-06T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.16"}
      , {"id": "e61079b2da394364800e4033e0fde4d3" , "appId": "UnrealJS_4.17" , "compatibleApps": ["UE_4.17"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2017-09-07T15:46:23.172Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.17"}
      , {"id": "d260e37707fc4117afcdcdbda636d339" , "appId": "UnrealJS_4.18" , "compatibleApps": ["UE_4.18"] , "platform": ["Mac" , "Windows"] , "dateAdded": "2017-10-31T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.18"}
      , {"id": "82550c81144d4a2db6d5643cc0f38112" , "appId": "UnrealJS_4.19" , "compatibleApps": ["UE_4.19"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2018-03-21T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.19"}
      , {"id": "eac38fcc676b4fb0947192b215fc5150" , "appId": "UnrealJS_4.20" , "compatibleApps": ["UE_4.20"] , "platform": ["Windows" , "Mac"] , "dateAdded": "2018-08-25T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.20"}
      , {"id": "9f6cc5d76fd94190ad14c7bba678b20b" , "appId": "UnrealJS_4.21" , "compatibleApps": ["UE_4.21"] , "platform": ["Mac" , "Windows"] , "dateAdded": "2018-12-01T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.21"}
      , {"id": "38aebbd1c5ae4439b6f3f6dde8ff861c" , "appId": "UnrealJS_4.22" , "compatibleApps": ["UE_4.22"] , "platform": ["Windows" , "Mac" , "iOS" , "Linux" , "Android"] , "dateAdded": "2019-04-04T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.22"}
      , {"id": "99162109fca5461a8edff3e8ef63b67f" , "appId": "UnrealJS_4.23" , "compatibleApps": ["UE_4.23"] , "platform": ["Windows" , "Linux" , "Android"] , "dateAdded": "2019-11-07T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_423"}
      , {"id": "f7b13b29c406490e8d51d56c971ebee8" , "appId": "UnrealJS_4.24" , "compatibleApps": ["UE_4.24"] , "platform": ["Windows" , "Linux" , "Android" , "iOS" , "Mac"] , "dateAdded": "2020-02-04T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.24"}
      , {"id": "665cb1f17807478da6188c752348a1ea" , "appId": "UnrealJS_4.25" , "compatibleApps": ["UE_4.25"] , "platform": ["Linux" , "Mac" , "iOS" , "Android" , "Windows"] , "dateAdded": "2020-05-15T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.25"}
      , {"id": "bf128497fe684b28bc05966008bc0e9c" , "appId": "UnrealJS_4.26" , "compatibleApps": ["UE_4.26"] , "platform": ["Android" , "iOS" , "Linux" , "Mac" , "Windows"] , "dateAdded": "2020-12-30T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.26"}
      , {"id": "ea9d15fbede84b3a97a77f86e5cc1814" , "appId": "UnrealJS_4.27" , "compatibleApps": ["UE_4.27"] , "platform": ["Windows" , "Mac" , "iOS" , "Linux" , "Android"] , "dateAdded": "2021-11-23T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_4.27"}
      , {"id": "4ef50e414c2a4db0a4d8f96e585edf4c" , "appId": "UnrealJS_5.0" , "compatibleApps": ["UE_5.0"] , "platform": ["Windows" , "Mac" , "Android" , "iOS" , "Linux"] , "dateAdded": "2022-04-08T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_5.0"}
      , {"id": "c476184812ff438289bbb84c9a57df74" , "appId": "UnrealJS_5.1" , "compatibleApps": ["UE_5.1"] , "platform": ["Android" , "iOS" , "Linux" , "Mac" , "Windows"] , "dateAdded": "2023-03-16T00:00:00.000Z" , "releaseNote": "" , "versionTitle": "UnrealJS_5.1"}
    ]
    , "platforms": [{"key": "windows" , "value": "Windows 64-bit"}, {"key": "apple" , "value": "MacOS"}, {"key": "mobile" , "value": "iOS"}, {"key": "linux" , "value": "Linux"}, {"key": "android" , "value": "Android"}]
    , "compatibleApps": ["4.11" , "4.12" , "4.13" , "4.14" , "4.15" , "4.16" , "4.17" , "4.18" , "4.19" , "4.20" , "4.21" , "4.22" , "4.23" , "4.24" , "4.25" , "4.26" , "4.27" , "5.0" , "5.1"]
    , "urlSlug": "unrealjs"
    , "purchaseLimit": 1, "tax": 0, "tags": [3122, 26645, 1339]
    , "commentRatingId": "d90f92a8b9aa491da359666fa05b7cbb"
    , "ratingId": "be751eedc4a14cc09e39945bc5a531c4"
    , "klass": ""
    , "isNew": false, "free": true, "discounted": false, "featured": "https://cdn1.epicgames.com/ue/item/UnrealJS_Featured-476x246-8f909f896a43427df3ede8eb8f471933.png"
    , "thumbnail": "https://cdn1.epicgames.com/ue/item/UnrealJS_Thumb-288x288-9966133f072a1c9812c81cf1e3bd4ec3.png"
    , "learnThumbnail": "https://cdn1.epicgames.com/ue/item/UnrealJS_Featured-476x246-8f909f896a43427df3ede8eb8f471933.png"
    , "headerImage": "https://cdn1.epicgames.com/ue/item/UnrealJSScreenshot01-1920x1080-0de33736653a1c908944e2f45c90a534.png"
    , "status": "ACTIVE"
    , "price": "$0.00"
    , "discount": null, "discountPrice": null, "ownedCount": 0, "canPurchase": true, "owned": false, "rating": {"targetId": "be751eedc4a14cc09e39945bc5a531c4"
    , "averageRating": 4.46, "rating5": 63, "rating4": 5, "rating3": 1, "rating2": 1, "rating1": 8, "legacyRatingNum": 62, "rating5Percent": 80.77, "rating4Percent": 6.41, "rating3Percent": 1.28, "rating2Percent": 1.28, "rating1Percent": 10.26, "total": 78}
    , "app_name": "UnrealJS_5.1"
    """
    asset = EpicAsset(
        app_name="UnrealJS_5.1",
        label_name="",  # unused
        build_version="",  # unused
        catalog_item_id="d90f92a8b9aa491da359666fa05b7cbb",
        namespace="ue",
        asset_id="be751eedc4a14cc09e39945bc5a531c4",
    )
    print(f"\n*****\nGetting asset info\n*****\n")
    try:
        infos = await egs.asset_info(asset)
        print(f"\n{asset.app_name} Infos: {infos}\n")
    except Exception as e:
        print(f"\nFailed to get EGS asset infos: {e}\n")

    print(f"\n*****\nGetting an asset manifest\n*****\n")
    manifest = None
    try:

        manifest = await egs.asset_manifest(item_id=asset.catalog_item_id, namespace=asset.namespace, app=asset.app_name)
        print(f"\n{asset.app_name} EGS Manifest: {manifest}\n")
    except Exception as e:
        print(f"\nFailed to get EGS asset manifest: {e}\n")

    # trying to get the manifest using FAB for "UnrealJS_5.1","
    # !! DOES NOT WORK, raise a 403 error due to captcha !!
    # CHECK: what is the artifact_id? where to get it?
    artifact_id = "9fa01ca3-2d5a-4bfa-a1c2-5a41e82eb196"  # get from the url of the asset in FAB
    try:
        manifest = await egs.fab_asset_manifest(artifact_id=artifact_id, namespace=asset.namespace, asset_id=asset.asset_id, platform="Windows")
        print(f"\n{asset.app_name} FAB Manifest: {manifest}\n")
    except Exception as e:
        print(f"\nFailed to get FAB asset manifest: {e}\n")

    await egs.close()  # Close the session


if __name__ == "__main__":
    asyncio.run(main())

    print("\nDone.\n")
