import argparse
import json

from .collectors.windows.cpu import collect_cpu
from .collectors.windows.disk import collect_disk
from .collectors.windows.host import collect_hostname
from .collectors.windows.memory import collect_memory
from .collectors.windows.os_info import collect_os
from .collectors.windows.network import collect_network
from .collectors.windows.uptime import collect_uptime
from .snapshot import CpuInfo, MemoryInfo, OsInfo, Snapshot


def build_parser():
    parser = argparse.ArgumentParser(
        prog="sysinfo_collector",
        description="Collect a snapshot of this Windows machine.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of text.",
    )

    return parser


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

def try_collect(errors, name, func, fallback):
    try:
        return func()
    except Exception as exc:
        errors.append(f"{name}: {exc}")
        return fallback

def format_text(snapshot):

    lines = [
        "System Information Collector",
        f" hostname: {snapshot.hostname}",
        f" cpu: {snapshot.cpu.name} ({snapshot.cpu.cores} cores)",
        f" os: {snapshot.os.name} {snapshot.os.version}",
        f" uptime_seconds: {snapshot.uptime_seconds}",
        f" memory_total_bytes: {snapshot.memory.total_bytes}",
        f" memory_available_bytes: {snapshot.memory.available_bytes}",
        
    ]

    for disk in snapshot.disks:
        lines.append(
            f" disk {disk.name}: {disk.total_bytes} total, {disk.free_bytes} free"
        )

    for adapter in snapshot.network:
        lines.append(f" network {adapter.name}: {adapter.ipv4}")

    if snapshot.errors:
        lines.append(" errors:")

        for message in snapshot.errors:
            lines.append(f"  {message}")

    return "\n".join(lines)

def format_json(snapshot):

    return json.dumps(snapshot.to_dict(), indent=2)


def main():
    parser = build_parser()

    args = parser.parse_args()

    snapshot = build_snapshot()

    if args.json:
        print(format_json(snapshot))
    else:
        print(format_text(snapshot))
