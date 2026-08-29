from dataclasses import asdict, dataclass

@dataclass
class OsInfo:
    name: str
    version: str

@dataclass
class MemoryInfo:
    total_bytes: int

@dataclass
class Snapshot:
    hostname: str
    os: OsInfo
    memory: MemoryInfo

    def to_dict(self):
        return asdict(self)

def fake_snapshot():

    return Snapshot(
        hostname="fake-pc",
        os=OsInfo(name="Windows", version="11"),
        memory=MemoryInfo(total_bytes=17179869184),
    )