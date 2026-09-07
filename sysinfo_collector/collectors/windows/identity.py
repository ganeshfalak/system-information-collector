import json

from ...snapshot import IdentityInfo
from .powershell import run_powershell

DOMAIN_ROLES = {
    0: "Standalone workstation",
    1: "Member workstation",
    2: "Standalone server",
    3: "Member server",
    4: "Backup DC",
    5: "Primary DC",
}

def _text(value):
    if value is None:
        return ""
    return str(value).strip()

def collect_identity():

    cs_script = (
        "Get-CimInstance Win32_ComputerSystem | "
        "Select-Object UserName, Domain, PartOfDomain, DomainRole, "
        "Manufacturer, Model | "
        "ConvertTo-Json -Compress"
    )

    bios_script = (
        "Get-CimInstance Win32_BIOS | "
        "Select-Object SerialNumber, SMBIOSBIOSVersion | "
        "ConvertTo-Json -Compress"
    )

    cs = json.loads(run_powershell(cs_script))
    bios_raw = run_powershell(bios_script)
    bios = json.loads(bios_raw) if bios_raw else {}

    part_of_domain = bool(cs.get("PartOfDomain"))
    if cs.get("PartOfDomain") is None:
        join_type = "Unknown"
    elif part_of_domain:
        join_type = "Domain"
    else: 
        join_type = "Workgroup"

    role = cs.get("DomainRole")

    try:
        domain_role = DOMAIN_ROLES.get(int(role), "")
    except (TypeError, ValueError):
        domain_role = ""

    return IdentityInfo(
        username=_text(cs.get("UserName")),
        domain=_text(cs.get("Domain")),
        part_of_domain=part_of_domain,
        join_type=join_type,
        manufacturer=_text(cs.get("Manufacturer")),
        model=_text(cs.get("Model")),
        serial=_text(bios.get("SerialNumber")),
        bios_version=_text(bios.get("SMBIOSBIOSVersion")),
        domain_role=domain_role,
    )