# System Information Collector

A Python CLI that takes a snapshot of this Windows machine (OS, CPU, memory, disk, network, hostname, uptime).

## Status

Very early, Right now it only prints a placeholder line.

## How to run

From this folder, once per machine:

```text
python -m venv .venv
.venv\Scripts\activate

python -m sysinfo_collector