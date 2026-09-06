from .powershell import run_powershell

def collect_uptime():

    script = (
        "[int]((Get-Date) - "
        "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime)"
        ".TotalSeconds"
    )

    return int(run_powershell(script))

