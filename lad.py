import json
import httpx

from pathlib import Path


url = "https://mirrorbits.lineageos.org/full/pdx214/20251114/lineage-23.0-20251114-nightly-pdx214-signed.zip"


def download_lineage_zip():
    dest_path = Path("lineage_zip/test.zip")
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    chunck_cnt = 0

    with httpx.stream("GET", url, follow_redirects=True) as resp:
        resp.raise_for_status()
        with dest_path.open("wb") as f:
            for chunk in resp.iter_bytes(chunk_size=4 * 1024 * 1024):
                if chunk:
                    chunck_cnt += 1
                    # print(f"Gather chuck data: {chunck_cnt}")
                    f.write(chunk)

    print(f"Gather chuck data: {chunck_cnt}")
    print("Done downloading")


# download_lineage_zip()


with open("lineage_oems_tree.json", "r", encoding="utf-8") as f:
    oems_data = json.load(f)
