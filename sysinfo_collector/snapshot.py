from dataclasses import asdict, dataclass

@dataclass
class OsInfo:
    name: str
    version: str

@dataclass
class MemoryInfo:
    total_bytes: int
    available_bytes: int

@dataclass
class CpuInfo:
    name: str
    cores: int

@dataclass
class DiskInfo:
    name: str
    total_bytes: int
    free_bytes: int

@dataclass
class Snapshot:
    hostname: str
    os: OsInfo
    cpu: CpuInfo
    memory: MemoryInfo
    disks: list[DiskInfo]

    def to_dict(self):
        return asdict(self)

