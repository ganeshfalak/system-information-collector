import json

from ...snapshot import CpuInfo
from .powershell import run_powershell

def collect_cpu():

    script = (
        "Get-CimInstance Win32_Processor | "
        "Select-Object Name, NumberOfCores | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    return CpuInfo(
        name=data["Name"].strip(),
        cores=int(data["NumberOfCores"]),
    )