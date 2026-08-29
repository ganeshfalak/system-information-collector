import argparse

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

def main():
    parser = build_parser()

    args = parser.parse_args()
    print("System Information Collector")