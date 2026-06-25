from collections.abc import Iterable
from pathlib import Path

from asset_indexer.models import FileRecord


DEFAULT_EXCLUDED_DIRECTORIES = frozenset(
    {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "output",
    }
)


def scan_directory(
    root_path: Path,
    excluded_directories: Iterable[str] = (),
) -> list[FileRecord]:
    if not root_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {root_path}")

    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_path}")

    excluded_directory_names = {
        directory_name.lower()
        for directory_name in DEFAULT_EXCLUDED_DIRECTORIES
    }

    excluded_directory_names.update(
        directory_name.lower()
        for directory_name in excluded_directories
    )

    file_records: list[FileRecord] = []

    for path in root_path.rglob("*"):
        if _is_excluded(path, root_path, excluded_directory_names):
            continue

        if not path.is_file():
            continue

        file_records.append(
            FileRecord(
                path=path,
                size_bytes=path.stat().st_size,
            )
        )

    return file_records


def _is_excluded(
    path: Path,
    root_path: Path,
    excluded_directory_names: set[str],
) -> bool:
    relative_path = path.relative_to(root_path)

    return any(
        path_part.lower() in excluded_directory_names
        for path_part in relative_path.parts[:-1]
    )