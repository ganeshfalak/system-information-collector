# System Information Collector

A Python CLI that takes a one-shot snapshot of **Windows**:
OS, CPU, memory, disks, network (IPv4), hostname, and uptime.

It talks to Windows through PowerShell / CIM. You can develop in Windows or WSL;
collection always targets Windows (`powershell.exe`).

No third-party packages. Standard library only.

Text is meant to be readable (GiB, percent free, `Xd Xh`). JSON keeps raw
**bytes** and **seconds**, plus `schema_version` and `collected_at`.

## Status

Collectors are live. Schema version is **2**. If one collector fails, the rest
still print, failures show up in `errors`, and the process exits with code `1`.

## Setup

Use a separate venv on each OS. They are not interchangeable.

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

## Usage

```text
python -m sysinfo_collector          # readable text
python -m sysinfo_collector --json   # same snapshot as JSON
python -m sysinfo_collector --help
```

| Exit code | Meaning |
| --- | --- |
| 0 | Every collector succeeded (`errors` is `[]`) |
| 1 | At least one collector failed (a partial snapshot was still printed) |

`--help` exits 0.

## Sample text

```text
=== Snapshot  2026-09-07T14:22:00-04:00  schema=2  ===
 hostname  EXAMPLE-PC
 os        Microsoft Windows 11  10.0.22631
 cpu       Example CPU (8) cores
 ram       8.0 GiB / 16.0 GiB available
 uptime    1d 0h
 disk C:   238.4 GiB  111.8 GiB free  (47%)
 network   Ethernet:  192.168.1.10
```

If a collector fails, an `errors:` block is appended, for example:

```text
 errors:
  disk: boom
```

## Sample JSON

```json
{
  "schema_version": 2,
  "collected_at": "2026-09-07T14:22:00-04:00",
  "hostname": "EXAMPLE-PC",
  "os": {
    "name": "Microsoft Windows 11",
    "version": "10.0.22631"
  },
  "cpu": {
    "name": "Example CPU",
    "cores": 8
  },
  "memory": {
    "total_bytes": 17179869184,
    "available_bytes": 8589934592
  },
  "disks": [
    {
      "name": "C:",
      "total_bytes": 256000000000,
      "free_bytes": 120000000000
    }
  ],
  "network": [
    {
      "name": "Ethernet",
      "ipv4": "192.168.1.10"
    }
  ],
  "uptime_seconds": 86400,
  "errors": []
}
```

`--json` is the same snapshot as text, not a different collection pass.
`collected_at` is ISO-8601 with a timezone offset. Memory and disk sizes in JSON
are **bytes** (the memory collector converts CIM kilobytes). Text converts those
bytes to GiB. MAC addresses are not collected.

## Layout

- `sysinfo_collector/__main__.py` — `python -m` entry
- `sysinfo_collector/cli.py` — flags, text/JSON, exit code
- `sysinfo_collector/orchestrator.py` — run collectors, record errors
- `sysinfo_collector/snapshot.py` — portable dataclass schema
- `sysinfo_collector/collectors/windows/` — CIM via `powershell.exe`
