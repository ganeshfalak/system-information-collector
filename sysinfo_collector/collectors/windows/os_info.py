import json

from ...snapshot import OsInfo
from .powershell import run_powershell

def collect_os():

    script = (
        "Get-CimInstance Win32_OperatingSystem | "
        "Select-Object Caption, Version | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    return OsInfo(
        name=data['Caption'],
        version=data['Version'],
    )