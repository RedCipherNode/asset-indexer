import unittest
from pathlib import Path

from asset_indexer.file_analyzer import analyze_files
from asset_indexer.models import FileRecord


class FileAnalyzerTests(unittest.TestCase):
    def test_analyze_files_calculates_summary(self) -> None:
        file_records = [
            FileRecord(path=Path("alpha.py"), size_bytes=100),
            FileRecord(path=Path("beta.py"), size_bytes=200),
            FileRecord(path=Path("notes.md"), size_bytes=50),
        ]

        asset_stats = analyze_files(file_records)

        self.assertEqual(asset_stats.total_files, 3)
        self.assertEqual(asset_stats.total_size_bytes, 350)

        extension_counts = {
            extension_stat.extension: extension_stat.file_count
            for extension_stat in asset_stats.extension_stats
        }

        self.assertEqual(extension_counts[".py"], 2)
        self.assertEqual(extension_counts[".md"], 1)

    def test_analyze_files_returns_largest_files_first(self) -> None:
        file_records = [
            FileRecord(path=Path("small.txt"), size_bytes=10),
            FileRecord(path=Path("large.txt"), size_bytes=300),
            FileRecord(path=Path("medium.txt"), size_bytes=100),
        ]

        asset_stats = analyze_files(
            file_records=file_records,
            largest_file_limit=2,
        )

        self.assertEqual(
            [file_record.path for file_record in asset_stats.largest_files],
            [
                Path("large.txt"),
                Path("medium.txt"),
            ],
        )


if __name__ == "__main__":
    unittest.main()