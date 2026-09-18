import json

from ...snapshot import CpuInfo
from .powershell import run_powershell

def collect_cpu():

    script = (
        "Get-CimInstance Win32_Processor | "
        "Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    if isinstance(data, list):
        data = data[0]

    try:
        logical = int(data.get("NumberOfLogicalProcessors") or 0)
    except (TypeError, ValueError):
        logical = 0

    return CpuInfo(
        name=data["Name"].strip(),
        cores=int(data["NumberOfCores"]),
        logical_processors=logical,
    )