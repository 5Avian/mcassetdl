#!/usr/bin/env python3

import json
from pathlib import Path
from urllib.request import urlopen
from sys import exit
from os import makedirs

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
ASSETS_URL = "https://resources.download.minecraft.net"
ASSETS_PATH = Path("assets")

def main():
    with urlopen(MANIFEST_URL) as res:
        manifest = json.load(res)
    version_id = input("for which version should assets be downloaded? ")
    version_meta = next((version for version in manifest["versions"] if version["id"] == version_id), None)
    if not version_meta:
        exit(f"could not find version {version_id} in manifest")
    with urlopen(version_meta["url"]) as res:
        version = json.load(res)
    asset_index_id = version["assetIndex"]["id"]
    data_path = ASSETS_PATH / asset_index_id
    if data_path.exists():
        exit(f"assets for index {asset_index_id} already exist, please delete them first")
    with urlopen(version["assetIndex"]["url"]) as res:
        asset_index = json.load(res)
    for key, object in asset_index["objects"].items():
        path = data_path / key
        makedirs(path.parent, exist_ok=True)
        hash = object["hash"]
        url = f"{ASSETS_URL}/{hash[:2]}/{hash}"
        with urlopen(url) as res:
            with path.open("wb") as file:
                file.write(res.read())
    print(f"successfully downloaded assets for index {asset_index_id}")

if __name__ == "__main__":
    main()
