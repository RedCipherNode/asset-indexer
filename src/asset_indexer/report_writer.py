import json
from dataclasses import asdict
from pathlib import Path

from asset_indexer.models import AssetStats, FileRecord


def write_manifest(
    output_path: Path,
    root_path: Path,
    asset_stats: AssetStats,
) -> None:
    manifest = {
        "root_path": str(root_path.resolve()),
        "total_files": asset_stats.total_files,
        "total_size_bytes": asset_stats.total_size_bytes,
        "extensions": [
            {
                "extension": extension_stat.extension,
                "file_count": extension_stat.file_count,
            }
            for extension_stat in asset_stats.extension_stats
        ],
        "largest_files": [
            _file_record_to_dict(file_record, root_path)
            for file_record in asset_stats.largest_files
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2)


def write_markdown_report(
    output_path: Path,
    root_path: Path,
    asset_stats: AssetStats,
) -> None:
    lines = [
        "# Asset Index Report",
        "",
        f"**Scanned Directory:** `{root_path.resolve()}`",
        f"**Total Files:** {asset_stats.total_files}",
        f"**Total Size:** {_format_size(asset_stats.total_size_bytes)}",
        "",
        "## Top Extensions",
        "",
        "| Extension | Files |",
        "| --- | ---: |",
    ]

    for extension_stat in asset_stats.extension_stats[:10]:
        lines.append(
            f"| {extension_stat.extension} | {extension_stat.file_count} |"
        )

    lines.extend(
        [
            "",
            "## Largest Files",
            "",
            "| Size | Path |",
            "| ---: | --- |",
        ]
    )

    for file_record in asset_stats.largest_files:
        relative_path = file_record.path.relative_to(root_path)
        lines.append(
            f"| {_format_size(file_record.size_bytes)} | `{relative_path}` |"
        )

    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _file_record_to_dict(
    file_record: FileRecord,
    root_path: Path,
) -> dict[str, str | int]:
    return {
        "path": str(file_record.path.relative_to(root_path)),
        "size_bytes": file_record.size_bytes,
    }


def _format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"