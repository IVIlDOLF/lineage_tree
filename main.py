import time
import httpx
import json
import re


def device_name_numeric_key(device: dict) -> tuple[int, str]:
    name = device["device_name"].strip()
    match = re.match(r"(\d+)", name)
    if match:
        return int(match.group(1)), name.lower()
    return (10**9, name.lower())


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

            # print(f"oem: {oem_name}, model: {device_model}, name: {device_name}")

            devices_dict.setdefault(oem_name, []).append(
                {
                    "device_name": device_name,
                    "device_model": device_model,
                }
            )

    for devices in devices_dict.values():
        devices.sort(key=device_name_numeric_key)

    devices_sorted = dict(sorted(devices_dict.items()))

    with open("lineage_oems_tree.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(devices_sorted, indent=2, sort_keys=False, ensure_ascii=False))


# create_oems_tree()


def get_device_info(device_name: str):
    with httpx.Client(timeout=10.0) as client:
        # device_name = "zippo"
        resp = client.get(f"https://download.lineageos.org/api/v2/devices/{device_name}/builds")
        resp.raise_for_status()
        device_info_raw = resp.json()

    # device_info_formatted = json.dumps(
    #     device_info_raw, indent=2, sort_keys=True, ensure_ascii=False
    # )

    # print("device_info_raw:", device_info_raw)

    # with open("lineage_device_info.json", "w", encoding="utf-8") as f:
    #     f.write(device_info_formatted)

    # print("device_info_raw[0]:", device_info_raw[0])

    device_info_dict = {}

    for device_build_dict in device_info_raw:
        device_build_version = device_build_dict["version"]
        # print(f"device_build_dict version: {device_build_version}")

        if device_build_version == "22.2":
            device_build_arr = device_build_dict["files"]

            for curr_device_build in device_build_arr:
                device_build_filename = curr_device_build["filename"]

                if "lineage" in device_build_filename:
                    # print(device_build_filename)

                    device_version_lineageos = device_build_dict["version"]
                    device_info_dict["version_lineageos"] = device_version_lineageos

                    device_info_dict["support_lineage_22.2"] = True

                    device_info_dict.update(curr_device_build)

    if not device_info_dict:
        device_info_dict["support_lineage_22.2"] = False
        print(f"exception device_info_dict with device_name: {device_name}")
        # raise Exception("device_info_dict empty")

    # print("device_info_dict:", device_info_dict)

    return device_info_dict


# get_device_info("pdx214")


def create_full_lineage_tree():
    with open("lineage_oems_tree.json", "r", encoding="utf-8") as f:
        oems_data = json.load(f)

    # print("oems_data json:", oems_data)

    for oem, device_list in oems_data.items():
        for device_info_dict in device_list:
            device_name = device_info_dict["device_name"]
            device_model = device_info_dict["device_model"]

            print("device_name:", device_name)
            print("device_model:", device_model)

            device_build_info_dict = get_device_info(device_model)

            device_info_dict.update(device_build_info_dict)
            time.sleep(2)

    # print("oems_data modified:", oems_data)

    with open("lineage_oems_tree_full.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(oems_data, indent=2, sort_keys=False, ensure_ascii=False))


# create_full_lineage_tree()
