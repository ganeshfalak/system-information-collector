import json

from ...snapshot import NetworkInfo
from .powershell import run_powershell


def _as_list(value):
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def collect_network():

    script = (
        "Get-CimInstance Win32_NetworkAdapterConfiguration "
        "-Filter 'IPEnabled=TRUE' | "
        "Select-Object Description, IPAddress, DefaultIPGateway, DNSServerSearchOrder | "
        "ConvertTo-Json -Compress"
    )

    raw = run_powershell(script)

    if not raw:
        return []

    data = json.loads(raw)

    if not isinstance(data, list):
        data = [data]

    adapters = []
    
    for item in data:

        addresses = item.get("IPAddress") or []

        if isinstance(addresses, str):
            addresses = [addresses]
            
        ipv4 = [a for a in addresses if a and ":" not in a]

        if not ipv4:
            continue

        gateways = _as_list(item.get("DefaultIPGateway"))
        dns = [d for d in _as_list(item.get("DNSServerSearchOrder")) if d]

        adapters.append(
            NetworkInfo(
                name=item["Description"],
                ipv4=ipv4[0],
                gateway=gateways[0] if gateways else "",
                dns=dns,
            )
        )
    return adapters