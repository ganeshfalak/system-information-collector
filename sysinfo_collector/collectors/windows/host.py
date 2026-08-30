import json

from .powershell import run_powershell

def collect_hostname():

    script = (
        "Get-CimInstance Win32_ComputerSystem | "
        "Select-Object Name | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    return data["Name"]