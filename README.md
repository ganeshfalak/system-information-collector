# System Information Collector

A Python CLI that takes a one-shot snapshot of **Windows**:
OS, CPU, memory, disks, network (IPv4), hostname, and uptime.

It talks to Windows through PowerShell / CIM. You can develop in Windows or WSL;
collection always targets Windows (`powershell.exe`).

No third-party packages. Standard library only.

## Status

v1 collectors are live. If one collector fails, the rest still print, failures
show up in `errors`, and the process exits with code `1`.

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
python -m sysinfo_collector --json   # same data as JSON
python -m sysinfo_collector --help
```

| Exit code | Meaning |
| --- | --- |
| 0 | Every collector succeeded (`errors` is `[]`) |
| 1 | At least one collector failed (a partial snapshot was still printed) |

`--help` exits 0.

## Sample text

```text
System Information Collector
 hostname: EXAMPLE-PC
 cpu: Example CPU (8 cores)
 os: Microsoft Windows 11 10.0.22631
 uptime_seconds: 86400
 memory_total_bytes: 17179869184
 memory_available_bytes: 8589934592
 disk C:: 256000000000 total, 120000000000 free
 network Ethernet: 192.168.1.10
```

If a collector fails, an `errors:` block is appended, for example:

```text
 errors:
  disk: boom
```

## Sample JSON

```json
{
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

`--json` is the same snapshot as text, not a different collection pass. Memory is in
**bytes** (CIM kilobytes are converted in the memory collector). MAC addresses are
not collected.

## Layout

- `sysinfo_collector/__main__.py` — `python -m` entry
- `sysinfo_collector/cli.py` — flags, text/JSON, exit code
- `sysinfo_collector/orchestrator.py` — run collectors, record errors
- `sysinfo_collector/snapshot.py` — portable dataclass schema
- `sysinfo_collector/collectors/windows/` — CIM via `powershell.exe`
