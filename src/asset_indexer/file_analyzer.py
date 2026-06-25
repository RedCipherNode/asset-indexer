from collections import Counter

from asset_indexer.models import AssetStats, ExtensionStat, FileRecord


def analyze_files(
    file_records: list[FileRecord],
    largest_file_limit: int = 10,
) -> AssetStats:
    total_size_bytes = sum(file_record.size_bytes for file_record in file_records)

    extension_counts = Counter(
        file_record.path.suffix.lower() or "[no extension]"
        for file_record in file_records
    )

    extension_stats = [
        ExtensionStat(
            extension=extension,
            file_count=file_count,
        )
        for extension, file_count in extension_counts.most_common()
    ]

    largest_files = sorted(
        file_records,
        key=lambda file_record: file_record.size_bytes,
        reverse=True,
    )[:largest_file_limit]

    return AssetStats(
        total_files=len(file_records),
        total_size_bytes=total_size_bytes,
        extension_stats=extension_stats,
        largest_files=largest_files,
    )