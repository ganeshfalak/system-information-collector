import json

from ...snapshot import MemoryInfo
from .powershell import run_powershell

def collect_memory():

    script = (
        "Get-CimInstance Win32_OperatingSystem | "
        "Select-Object TotalVisibleMemorySize, FreePhysicalMemory | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    return MemoryInfo(
        total_bytes=int(data["TotalVisibleMemorySize"]) * 1024,
        available_bytes=int(data["FreePhysicalMemory"]) * 1024,
    )
