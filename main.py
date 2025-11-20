import httpx
import json


def create_oems_tree():
    with httpx.Client(timeout=10.0) as client:
        resp = client.get("https://download.lineageos.org/api/v2/oems")
        resp.raise_for_status()
        devices_list = resp.json()
 
        devices_dict = {}

        for devices_info in devices_list:
            oem_name = devices_info["name"]
            for device_info in devices_info["devices"]:
                device_model = device_info["model"]
                device_name = device_info["name"]
                print(f"oem: {oem_name}, model: {device_model}, name: {device_name}")

                devices_dict.setdefault(oem_name, []).append(
                    {
                        "device_name": device_name,
                        "device_model": device_model,
                    }
                )


        for devices in devices_dict.values():
            devices.sort(key=lambda d: d["device_name"].lower())

        devices_sorted = dict(sorted(devices_dict.items()))

        with open("lineage_oems_tree.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(devices_sorted, indent=2, sort_keys=False, ensure_ascii=False))


create_oems_tree()

