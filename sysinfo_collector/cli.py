import argparse

def build_parser():
    parser = argparse.ArgumentParser(
        prog="sysinfo_collector",
        description="Collect a snapshot of this Windows machine.",
    )

    return parser

def main():
    parser = build_parser()
    parser.parse_args()
    print("System Information Collector")