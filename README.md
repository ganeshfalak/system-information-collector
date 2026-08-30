# System Information Collector

A Python CLI that takes a snapshot of this Windows machine (OS, CPU, memory, disk, network, hostname, uptime).

## Status

OS and hostname comes from CIM; memory is still placeholder.

## How to run

The program collects **Windows** info. You can run/develop from Windows or WSL.

### Windows

```text
python -m venv .venv-win
.venv-win\Scripts\activate
python -m sysinfo_collector
```

### WSL

```text
python3 -m venv .venv-wsl
source .venv-wsl/bin/activate
python -m sysinfo_collector
```
