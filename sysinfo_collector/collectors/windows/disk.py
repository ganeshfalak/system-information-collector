import json

from ...snapshot import DiskInfo
from .powershell import run_powershell

def collect_disk():

    script = (
        "Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | "
        "Select-Object DeviceID, Size, FreeSpace | "
        "ConvertTo-Json -Compress"
    )

    raw = run_powershell(script)

    if not raw:
        return []

    data = json.loads(raw)

    if not isinstance(data, list):
        data = [data]

    disks = []
    for item in data:
        size = item.get("Size")
        free = item.get("FreeSpace")

        if size is None or free is None:
            continue

        disks.append(
            DiskInfo(
                name=item["DeviceID"],
                total_bytes=int(size),
                free_bytes=int(free),
            )
        )

    return disks

