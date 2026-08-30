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
class Snapshot:
    hostname: str
    os: OsInfo
    cpu: CpuInfo
    memory: MemoryInfo

    def to_dict(self):
        return asdict(self)

