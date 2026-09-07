import argparse
import json

from .orchestrator import build_snapshot

GIB = 1024 ** 3

def format_gib(num_bytes):
    return f"{num_bytes / GIB:.1f} GiB"

def percent_free(total_bytes, free_bytes):
    if total_bytes <= 0:
        return 0
    return int(round(100 * free_bytes / total_bytes))

def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    return f"{days}d {hours}h"

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
    mem = snapshot.memory

    lines = [
        f"=== Snapshot  {snapshot.collected_at}  schema={snapshot.schema_version}  ===",
        f" hostname  {snapshot.hostname}",
        f" os        {snapshot.os.name}  {snapshot.os.version}",
        f" cpu       {snapshot.cpu.name} ({snapshot.cpu.cores}) cores",
        f" ram       {format_gib(mem.available_bytes)} / {format_gib(mem.total_bytes)} available",
        f" uptime    {format_uptime(snapshot.uptime_seconds)}",
    ]

    for disk in snapshot.disks:
        pct = percent_free(disk.total_bytes, disk.free_bytes)

        lines.append(
            f" disk {disk.name}   {format_gib(disk.total_bytes)}  "
            f"{format_gib(disk.free_bytes)} free  ({pct}%)"
        )

    for adapter in snapshot.network:
        lines.append(f" network   {adapter.name}:  {adapter.ipv4}")

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

    return 1 if snapshot.errors else 0
