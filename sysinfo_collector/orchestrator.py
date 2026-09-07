from .collectors.windows.cpu import collect_cpu
from .collectors.windows.disk import collect_disk
from .collectors.windows.host import collect_hostname
from .collectors.windows.memory import collect_memory
from .collectors.windows.os_info import collect_os
from .collectors.windows.network import collect_network
from .collectors.windows.uptime import collect_uptime
from .collectors.windows.identity import collect_identity
from .snapshot import CpuInfo, MemoryInfo, OsInfo, IdentityInfo, Snapshot

from datetime import datetime

def try_collect(errors, name, func, fallback):
    try:
        return func()
    except Exception as exc:
        errors.append(f"{name}: {exc}")
        return fallback

def build_snapshot():
    errors = []

    return Snapshot(
        schema_version=2,
        collected_at=datetime.now().astimezone().replace(microsecond=0).isoformat(),
        hostname=try_collect(errors, "hostname", collect_hostname, ""),
        identity=try_collect(errors, "identity", collect_identity, IdentityInfo(
            username="",
            domain="",
            part_of_domain=False,
            join_type="Unknown",
            manufacturer="",
            model="",
            serial="",
            bios_version="",
            domain_role="",
        )),
        cpu=try_collect(errors, "cpu", collect_cpu, CpuInfo(name="", cores=0)),
        os=try_collect(errors, "os", collect_os, OsInfo(name="", version="")),
        memory=try_collect(errors, "memory", collect_memory, MemoryInfo(total_bytes=0, available_bytes=0)),
        disks=try_collect(errors, "disk", collect_disk, []),
        network=try_collect(errors, "network", collect_network, []),
        uptime_seconds=try_collect(errors, "uptime", collect_uptime, 0),
        errors=errors,
    )
