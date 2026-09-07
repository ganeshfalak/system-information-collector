import argparse
import json

from pathlib import Path

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

    parser.add_argument(
        "--out",
        metavar="PATH",
        help="Write the snapshot to a file (still prints)."
    )

    return parser


def format_text(snapshot):
    ident = snapshot.identity
    mem = snapshot.memory
    user = ident.username if ident.username else "(none)"
    join = f"{ident.join_type} ({ident.domain})" if ident.domain else ident.join_type

    lines = [
        f"=== Snapshot  {snapshot.collected_at}  schema={snapshot.schema_version}  ===",
        "IDENTITY",
        f"  hostname     {snapshot.hostname}",
        f"  user         {user}",
        f"  join         {join}",
        f"  manufacturer {ident.manufacturer}",
        f"  model        {ident.model}",
        f"  serial       {ident.serial}",
        "",
        "OS",
        f"  {snapshot.os.name}  {snapshot.os.version}",
        f"  uptime       {format_uptime(snapshot.uptime_seconds)}",
        "",
        "HARDWARE",
        f"  cpu          {snapshot.cpu.name} ({snapshot.cpu.cores} cores)",
        f"  ram          {format_gib(mem.available_bytes)} / {format_gib(mem.total_bytes)} available",
        "",
        "STORAGE",
    ]

    for disk in snapshot.disks:
        pct = percent_free(disk.total_bytes, disk.free_bytes)
        lines.append(
            f"  {disk.name}  {format_gib(disk.total_bytes)}  "
            f"{format_gib(disk.free_bytes)} free  ({pct}%)"
        )

    lines.append("")
    lines.append("NETWORK")
    for adapter in snapshot.network:
        lines.append(f"  {adapter.name}  {adapter.ipv4}")

    if snapshot.errors:
        lines.append("")
        lines.append("errors:")
        for message in snapshot.errors:
            lines.append(f"  {message}")

    return "\n".join(lines)

def format_json(snapshot):

    return json.dumps(snapshot.to_dict(), indent=2)


def main():
    parser = build_parser()
    args = parser.parse_args()
    snapshot = build_snapshot()
    output = []

    if args.json:
        output = format_json(snapshot)
    else:
        output = format_text(snapshot)

    print(output)

    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")

    return 1 if snapshot.errors else 0
