import argparse
import json


from .collectors.windows.os_info import collect_os
from .collectors.windows.host import collect_hostname
from .snapshot import MemoryInfo, Snapshot


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
        os=collect_os(),
        memory=MemoryInfo(total_bytes=17179869198)
    )


def format_text(snapshot):

    lines = [
        "System Information Collector",
        f" hostname: {snapshot.hostname}",
        f" os: {snapshot.os.name} {snapshot.os.version}",
        f" memory_total_bytes: {snapshot.memory.total_bytes}",
    ]

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
