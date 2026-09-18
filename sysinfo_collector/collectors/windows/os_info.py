import json

from ...snapshot import OsInfo
from .powershell import run_powershell

PRODUCT_TYPES = {
    1: "Workstation",
    2: "DomainController",
    3: "Server",
}

def collect_os():

    script = (
        "Get-CimInstance Win32_OperatingSystem | "
        "Select-Object Caption, Version, BuildNumber, OSArchitecture, ProductType, " 
        "@{Name='LastBoot';Expression={$_.LastBootUpTime.ToString('s')}} | "
        "ConvertTo-Json -Compress"
    )

    data = json.loads(run_powershell(script))

    try:
        product_type = PRODUCT_TYPES.get(int(data.get("ProductType")), "")
    except (TypeError, ValueError):
        product_type = ""

    return OsInfo(
        name=data["Caption"],
        version=data["Version"],
        build=str(data.get("BuildNumber") or ""),
        architecture=str(data.get("OSArchitecture") or ""),
        product_type=product_type,
        display_version="",
        ubr="",
        last_boot=str(data.get("LastBoot") or ""),
    )