from pathlib import Path

from asset_indexer.models import FileRecord


def scan_directory(root_path: Path) -> list[FileRecord]:
    if not root_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {root_path}")

    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_path}")

    file_records: list[FileRecord] = []

    for path in root_path.rglob("*"):
        if not path.is_file():
            continue

        try:
            file_records.append(
                FileRecord(
                    path=path,
                    size_bytes=path.stat().st_size,
                )
            )
        except OSError:
            continue

    return file_records