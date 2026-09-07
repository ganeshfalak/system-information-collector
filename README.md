# System Information Collector

One command. A **Windows** snapshot you can read or pipe.

Text is for people (GiB, `%` free, `1d 0h`). JSON is for scripts (bytes, seconds, full `identity`). Same collection either way. Read-only, local, standard library only.

Works from **Windows or WSL**; CIM always runs via `powershell.exe`.

## Run

```text
python -m venv .venv-win && .venv-win\Scripts\activate   # Windows
python3 -m venv .venv-wsl && source .venv-wsl/bin/activate  # WSL

python -m sysinfo_collector
python -m sysinfo_collector --json
python -m sysinfo_collector --out snapshot.txt
python -m sysinfo_collector --json --out snapshot.json
```

Use a **separate venv** on each OS. `--out` writes the same blob that was printed.

| Exit | When |
| ---: | --- |
| `0` | every collector succeeded (`errors` is `[]`) |
| `1` | at least one collector failed (partial snapshot still printed) |

`--help` exits `0`.

## Sample

```text
=== Snapshot  2026-09-07T14:22:00-04:00  schema=2  ===
IDENTITY
  hostname     EXAMPLE-PC
  user         EXAMPLE\jsmith
  join         Workgroup (WORKGROUP)
  manufacturer Example Vendor
  model        Example Model
  serial       ABC1234

OS
  Microsoft Windows 11  10.0.22631
  uptime       1d 0h

HARDWARE
  cpu          Example CPU (8 cores)
  ram          8.0 GiB / 16.0 GiB available

STORAGE
  C:  238.4 GiB  111.8 GiB free  (47%)

NETWORK
  Ethernet  192.168.1.10
```

On failure, an `errors:` block is appended (`disk: boom`). Text IDENTITY is a **short view**. JSON also has `bios_version`, `domain_role`, and `part_of_domain`.

```json
{
  "schema_version": 2,
  "collected_at": "2026-09-07T14:22:00-04:00",
  "hostname": "EXAMPLE-PC",
  "identity": {
    "username": "EXAMPLE\\jsmith",
    "domain": "WORKGROUP",
    "part_of_domain": false,
    "join_type": "Workgroup",
    "manufacturer": "Example Vendor",
    "model": "Example Model",
    "serial": "ABC1234",
    "bios_version": "1.0.0",
    "domain_role": "Standalone workstation"
  },
  "os": { "name": "Microsoft Windows 11", "version": "10.0.22631" },
  "cpu": { "name": "Example CPU", "cores": 8 },
  "memory": { "total_bytes": 17179869184, "available_bytes": 8589934592 },
  "disks": [{ "name": "C:", "total_bytes": 256000000000, "free_bytes": 120000000000 }],
  "network": [{ "name": "Ethernet", "ipv4": "192.168.1.10" }],
  "uptime_seconds": 86400,
  "errors": []
}
```

`collected_at` is ISO-8601 with offset. JSON sizes are **bytes** (CIM memory is converted from KB). No MAC addresses, no upload.

## Layout

| Path | Role |
| --- | --- |
| `sysinfo_collector/__main__.py` | `python -m` entry, `sys.exit` |
| `sysinfo_collector/cli.py` | flags, text/JSON, `--out` |
| `sysinfo_collector/orchestrator.py` | run collectors, record `errors` |
| `sysinfo_collector/snapshot.py` | dataclass schema (`schema_version` 2) |
| `sysinfo_collector/collectors/windows/` | CIM via `powershell.exe` |
