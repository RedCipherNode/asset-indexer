import argparse
from pathlib import Path

from asset_indexer.file_scanner import scan_directory


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asset_indexer",
        description="Scan a directory and count its files.",
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan recursively.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    try:
        file_records = scan_directory(args.directory)
    except (FileNotFoundError, NotADirectoryError) as error:
        parser.error(str(error))
        return

    print(f"Scanned directory: {args.directory.resolve()}")
    print(f"Found files: {len(file_records)}")