# System Information Collector

Local, read-only **Windows** snapshot: identity, OS, CPU, memory, disks, network, uptime, plus a short findings list.

One collection pass. **Text** is for people (GiB, `%` free, `Xd Xh`). **JSON** is the full contract (bytes, seconds, every field). Standard library only — no pip packages.

CIM runs through `powershell.exe`, so the data is always the **Windows** machine even if you launch Python from WSL.

## Requirements

- Python 3.10+ (`list[str]` syntax)
- Windows, or WSL with `powershell.exe` on `PATH`
- Permission to run `Get-CimInstance` (normal local user is enough for these classes)

Not collected: MAC addresses, process lists, event logs, registry reboot keys, uploads.

## Setup

Use a **separate** virtualenv per OS; a Windows venv will not run under WSL and vice versa.

```text
# Windows
python -m venv .venv-win
.venv-win\Scripts\activate

# WSL
python3 -m venv .venv-wsl
source .venv-wsl/bin/activate
```

No `pip install`. Run from the repo root so `python -m sysinfo_collector` can see the package.

## Usage

```text
python -m sysinfo_collector
python -m sysinfo_collector --json
python -m sysinfo_collector --out snapshot.txt
python -m sysinfo_collector --json --out snapshot.json
python -m sysinfo_collector --copy
```

| Flag | Effect |
| --- | --- |
| *(none)* | Print ticket-style text |
| `--json` | Print the same snapshot as JSON |
| `--out PATH` | Also write that blob to a file |
| `--copy` | Also copy that blob to the clipboard via `clip.exe` |
| `-h` / `--help` | Argparse help; exit `0` |

`--out` and `--copy` use **whatever was printed** (text or JSON). Clipboard failure prints a warning on stderr and does not change the exit code.

On Windows you can double-click `collect.cmd` (uses `py -3` then `python`, passes `--copy`, then `pause`).

| Exit | Meaning |
| ---: | --- |
| `0` | Every collector succeeded (`errors` is `[]`) |
| `1` | At least one collector failed; a **partial** snapshot was still printed |

Findings (disk low, generic serial, …) do **not** change the exit code.

## Example

Text (fake host). `FINDINGS` is a curated view; `(none)` means no rules fired.

```text
=== Snapshot  2026-09-19T14:22:00-04:00  schema=2  ===
FINDINGS
  (none)

IDENTITY
  hostname     EXAMPLE-PC
  user         EXAMPLE\jsmith
  join         Workgroup (WORKGROUP)
  manufacturer Example Vendor
  model        Example Model
  serial       ABC1234

OS
  Microsoft Windows 11  10.0.22631  64-bit
  product      Workstation
  build        22631
  last boot    2026-09-18T10:00:00
  uptime       1d 0h

HARDWARE
  cpu          Example CPU (8 cores / 16 logical)
  ram          8.0 GiB / 16.0 GiB available

STORAGE
  C:  NTFS  238.4 GiB  111.8 GiB free  (47%)

NETWORK
  Ethernet  192.168.1.10
    gateway  192.168.1.1
    dns      192.168.1.1, 8.8.8.8
```

If a collector raises, that topic is filled with a placeholder and an `errors:` line is appended (`disk: boom`). IDENTITY text omits `bios_version` and `domain_role`; they are in JSON. Adapters without a gateway omit those extra lines.

JSON is the same snapshot (`schema_version` 2). Sizes are **bytes** (memory is converted from CIM kilobytes). `collected_at` is ISO-8601 with offset. `display_version` and `ubr` are reserved and currently `""`.

```json
{
  "schema_version": 2,
  "collected_at": "2026-09-19T14:22:00-04:00",
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
  "os": {
    "name": "Microsoft Windows 11",
    "version": "10.0.22631",
    "build": "22631",
    "architecture": "64-bit",
    "product_type": "Workstation",
    "display_version": "",
    "ubr": "",
    "last_boot": "2026-09-18T10:00:00"
  },
  "cpu": {
    "name": "Example CPU",
    "cores": 8,
    "logical_processors": 16
  },
  "memory": {
    "total_bytes": 17179869184,
    "available_bytes": 8589934592
  },
  "disks": [
    {
      "name": "C:",
      "total_bytes": 256000000000,
      "free_bytes": 120000000000,
      "file_system": "NTFS"
    }
  ],
  "network": [
    {
      "name": "Ethernet",
      "ipv4": "192.168.1.10",
      "gateway": "192.168.1.1",
      "dns": ["192.168.1.1", "8.8.8.8"]
    }
  ],
  "uptime_seconds": 86400,
  "errors": [],
  "findings": []
}
```

A finding object looks like `{"severity": "warning", "code": "disk_low", "message": "disk C: 8.0 GiB free (9%)"}`.

## Findings

Evaluated in `findings.py` from the finished snapshot. No extra CIM.

| severity | code | When |
| --- | --- | --- |
| critical | `disk_critical` | any local disk free &lt; 5 GiB **or** free % &lt; 5 |
| warning | `disk_low` | free &lt; 10 GiB and not already critical |
| warning | `no_ipv4` | `network` is empty |
| info | `long_uptime` | uptime &gt; 14 days |
| info | `serial_generic` | serial empty / `0` / OEM placeholder strings |

Text marks: `!` critical/warning, `i` info.

## How it works

```text
python -m sysinfo_collector
  → __main__.py          entry, sys.exit
  → cli.py               flags, format, --out / --copy
  → orchestrator.py      run each collector, catch failures
  → collectors/windows   Get-CimInstance via powershell.exe
  → snapshot.py          dataclasses (schema 2)
  → findings.py          rules on the finished snapshot
  → text or JSON         two views of the same object
```

Each collector either returns a value or raises. The orchestrator records `"{name}: {exc}"` and uses a placeholder so the rest of the snapshot still prints. Collectors never print; formatters never call CIM.

## Layout

| Path | Role |
| --- | --- |
| `collect.cmd` | Windows double-click helper (`--copy`) |
| `sysinfo_collector/__main__.py` | `python -m` entry |
| `sysinfo_collector/cli.py` | argparse, text/JSON, file, clipboard |
| `sysinfo_collector/orchestrator.py` | `try_collect`, assemble `Snapshot` |
| `sysinfo_collector/snapshot.py` | schema |
| `sysinfo_collector/findings.py` | severity rules |
| `sysinfo_collector/collectors/windows/` | CIM helpers and collectors |

## Limitations

- Windows-only collection (portable field names, no Linux collectors).
- Each collector starts its own `powershell.exe` (noticeable latency; not a second data source).
- `clip.exe` is Windows; `--copy` from a stripped environment warns and continues.
- Not an agent, monitor, or remoting tool (`-ComputerName` is out of scope).
