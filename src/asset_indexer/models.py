from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileRecord:
    path: Path
    size_bytes: int


@dataclass(frozen=True)
class ExtensionStat:
    extension: str
    file_count: int


@dataclass(frozen=True)
class AssetStats:
    total_files: int
    total_size_bytes: int
    extension_stats: list[ExtensionStat]
    largest_files: list[FileRecord]