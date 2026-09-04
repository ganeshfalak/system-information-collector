import argparse
import json

from .collectors.windows.cpu import collect_cpu
from .collectors.windows.disk import collect_disk
from .collectors.windows.host import collect_hostname
from .collectors.windows.memory import collect_memory
from .collectors.windows.os_info import collect_os
from .collectors.windows.network import collect_network
from .snapshot import Snapshot


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

    return Snapshot(
        hostname=collect_hostname(),
        cpu=collect_cpu(),
        os=collect_os(),
        memory=collect_memory(),
        disks=collect_disk(),
        network=collect_network(),
    )


def format_text(snapshot):

    lines = [
        "System Information Collector",
        f" hostname: {snapshot.hostname}",
        f" cpu: {snapshot.cpu.name} ({snapshot.cpu.cores} cores)",
        f" os: {snapshot.os.name} {snapshot.os.version}",
        f" memory_total_bytes: {snapshot.memory.total_bytes}",
        f" memory_available_bytes: {snapshot.memory.available_bytes}",
    ]

    for disk in snapshot.disks:
        lines.append(
            f" disk {disk.name}: {disk.total_bytes} total, {disk.free_bytes} free"
        )

    for adapter in snapshot.network:
        lines.append(f" network {adapter.name}: {adapter.ipv4}")

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
