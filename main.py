import httpx
import json

with httpx.Client(timeout=10.0) as client:
    resp = client.get("https://download.lineageos.org/api/v2/oems")
    resp.raise_for_status()
    data = resp.json()
    # print("data:", data)
    data_format_json = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    print("data_format_json:", data_format_json)
    with open("lineage_oems.json", "w", encoding="utf-8") as f:
        f.write(data_format_json)
    # data_oems_dict = json.loads(data)
    for devices_info in data:
        for device_info in devices_info:
            print(f"key: {device_info['model']}, val: {device_info['name']}")
