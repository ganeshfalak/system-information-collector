import json

from ...snapshot import DiskInfo
from .powershell import run_powershell

def collect_disk():

    script = (
        "Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | "
        "Select-Object DeviceID, Size, FreeSpace | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    if not isinstance(data, list):
        data = [data]

    disks = []

    for item in data:
        disks.append(
            DiskInfo(
                name=item["DeviceID"],
                total_bytes=int(item["Size"]),
                free_bytes=int(item["FreeSpace"]),
            )
        )

    return disks

