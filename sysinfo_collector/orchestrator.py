from .collectors.windows.cpu import collect_cpu
from .collectors.windows.disk import collect_disk
from .collectors.windows.host import collect_hostname
from .collectors.windows.memory import collect_memory
from .collectors.windows.os_info import collect_os
from .collectors.windows.network import collect_network
from .collectors.windows.uptime import collect_uptime
from .snapshot import CpuInfo, MemoryInfo, OsInfo, Snapshot

def try_collect(errors, name, func, fallback):
    try:
        return func()
    except Exception as exc:
        errors.append(f"{name}: {exc}")
        return fallback

def build_snapshot():
    errors = []

    return Snapshot(
        hostname=try_collect(errors, "hostname", collect_hostname, ""),
        cpu=try_collect(errors, "cpu", collect_cpu, CpuInfo(name="", cores=0)),
        os=try_collect(errors, "os", collect_os, OsInfo(name="", version="")),
        memory=try_collect(errors, "memory", collect_memory, MemoryInfo(total_bytes=0, available_bytes=0)),
        disks=try_collect(errors, "disk", collect_disk, []),
        network=try_collect(errors, "network", collect_network, []),
        uptime_seconds=try_collect(errors, "uptime", collect_uptime, 0),
        errors=errors,
    )
