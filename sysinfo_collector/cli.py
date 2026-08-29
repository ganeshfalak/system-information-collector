import argparse
import json

from .snapshot import fake_snapshot

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
        "System Information Collector (placeholder)",
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

    snapshot = fake_snapshot()

    if args.json:
        print(format_json(snapshot))
    else:
        print(format_text(snapshot))
