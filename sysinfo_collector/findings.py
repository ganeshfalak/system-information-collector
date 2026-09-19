from .snapshot import Finding

GIB = 1024 ** 3
FIVE_GIB = 5 * GIB
TEN_GIB = 10 * GIB
FOURTEEN_DAYS = 14 * 86400

GENERIC_SERIALS = {
    "",
    "0",
    "to be filled by o.e.m.",
    "default string",
    "none",
    "n/a",
}

def _percent_free(total_bytes, free_bytes):
    if total_bytes <= 0:
        return 0
    return int(round(100 * free_bytes / total_bytes))

def evaluate_findings(snapshot):
    findings = []

    for disk in snapshot.disks:
        pct = _percent_free(disk.total_bytes, disk.free_bytes)
        critical = disk.free_bytes < FIVE_GIB or pct < 5
        if critical:
            findings.append(
                Finding(
                    severity="critical",
                    code="disk_critical",
                    message=f"disk {disk.name} {disk.free_bytes / GIB:.1f} GiB free ({pct}%)",
                )
            )
        elif disk.free_bytes < TEN_GIB:
            findings.append(
                Finding(
                    severity="warning",
                    code="disk_low",
                    message=f"disk {disk.name} {disk.free_bytes / GIB:.1f} GiB free ({pct}%)",
                )
            )

    if not snapshot.network:
        findings.append(
            Finding(
                severity="warning",
                code="no_ipv4",
                message="no IPv4 adaptors reported",
            )
        )

    if snapshot.uptime_seconds > FOURTEEN_DAYS:
        days = snapshot.uptime_seconds // 86400
        findings.append(
            Finding(
                severity="info",
                code="long_uptime",
                message=f"uptime {days}d",
            )
        )

    serial = (snapshot.identity.serial or "").strip().lower()

    if serial in GENERIC_SERIALS:
        findings.append(
            Finding(
                severity="info",
                code="serial_generic",
                message="serial looks generic or empty",
            )
        )

    order = {"critical": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: order.get(f.severity, 9))

    return findings
