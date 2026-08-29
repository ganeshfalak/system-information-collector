import argparse
import json

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

def fake_snapshot():

    return {
        "hostname": "fake-pc",
        "os": {
            "name": "Windows",
            "version": "11",
        },
        "memory": {
            "total_bytes": 17179869184,
        },
    }

def format_text(snapshot):
    os_info = snapshot["os"]

    lines = [
        "System Information Collector (placeholder)",
        f" hostname: {snapshot['hostname']}",
        f" os: {os_info['name']} {os_info['version']}",
        f" memory_total_bytes: {snapshot['memory']['total_bytes']}",
    ]

    return "\n".join(lines)

def format_json(snapshot):

    return json.dumps(snapshot, indent=2)


def main():
    parser = build_parser()

    args = parser.parse_args()

    snapshot = fake_snapshot()

    if args.json:
        print(format_json(snapshot))
    else:
        print(format_text(snapshot))


    print("System Information Collector")