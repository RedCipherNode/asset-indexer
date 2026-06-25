import argparse
from pathlib import Path

from asset_indexer.file_analyzer import analyze_files
from asset_indexer.file_scanner import scan_directory
from asset_indexer.report_writer import write_manifest, write_markdown_report


def format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asset-indexer",
        description="Scan a directory and analyze its files.",
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan recursively.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory for generated manifest and report files.",
    )

    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        metavar="DIRECTORY",
        help="Additional directory names to exclude from scanning.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    try:
        file_records = scan_directory(
            root_path=args.directory,
            excluded_directories=args.exclude,
)
    except (FileNotFoundError, NotADirectoryError) as error:
        parser.error(str(error))
        return

    asset_stats = analyze_files(file_records)

    print(f"Scanned directory: {args.directory.resolve()}")
    print(f"Found files: {asset_stats.total_files}")
    print(f"Total size: {format_size(asset_stats.total_size_bytes)}")

    print("\nTop extensions:")
    for extension_stat in asset_stats.extension_stats[:10]:
        print(f"  {extension_stat.extension}: {extension_stat.file_count}")

    print("\nLargest files:")
    for file_record in asset_stats.largest_files:
        relative_path = file_record.path.relative_to(args.directory)
        print(f"  {format_size(file_record.size_bytes)}  {relative_path}")

    manifest_path = args.output_dir / "manifest.json"
    report_path = args.output_dir / "report.md"

    write_manifest(
        output_path=manifest_path,
        root_path=args.directory,
        asset_stats=asset_stats,
    )

    write_markdown_report(
        output_path=report_path,
        root_path=args.directory,
        asset_stats=asset_stats,
    )

    print(f"\nManifest written to: {manifest_path.resolve()}")
    print(f"Report written to: {report_path.resolve()}")