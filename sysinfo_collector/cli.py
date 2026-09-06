import argparse
import json

from .orchestrator import build_snapshot


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
