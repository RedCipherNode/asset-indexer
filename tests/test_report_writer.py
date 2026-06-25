import json
import tempfile
import unittest
from pathlib import Path

from asset_indexer.models import AssetStats, ExtensionStat, FileRecord
from asset_indexer.report_writer import write_manifest, write_markdown_report


class ReportWriterTests(unittest.TestCase):
    def create_asset_stats(self, root_path: Path) -> AssetStats:
        source_directory = root_path / "src"
        source_directory.mkdir()

        main_path = source_directory / "main.py"
        main_path.write_text("print('hello')", encoding="utf-8")

        readme_path = root_path / "README.md"
        readme_path.write_text("# Demo", encoding="utf-8")

        return AssetStats(
            total_files=2,
            total_size_bytes=300,
            extension_stats=[
                ExtensionStat(
                    extension=".py",
                    file_count=1,
                ),
                ExtensionStat(
                    extension=".md",
                    file_count=1,
                ),
            ],
            largest_files=[
                FileRecord(
                    path=main_path,
                    size_bytes=200,
                ),
                FileRecord(
                    path=readme_path,
                    size_bytes=100,
                ),
            ],
        )

    def test_write_manifest_creates_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)
            output_path = root_path / "output" / "manifest.json"

            write_manifest(
                output_path=output_path,
                root_path=root_path,
                asset_stats=self.create_asset_stats(root_path),
            )

            manifest = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual(manifest["total_files"], 2)
            self.assertEqual(manifest["total_size_bytes"], 300)
            self.assertEqual(
                manifest["extensions"],
                [
                    {
                        "extension": ".py",
                        "file_count": 1,
                    },
                    {
                        "extension": ".md",
                        "file_count": 1,
                    },
                ],
            )
            self.assertEqual(
                manifest["largest_files"][0],
                {
                    "path": "src\\main.py",
                    "size_bytes": 200,
                },
            )

    def test_write_markdown_report_creates_expected_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)
            output_path = root_path / "output" / "report.md"

            write_markdown_report(
                output_path=output_path,
                root_path=root_path,
                asset_stats=self.create_asset_stats(root_path),
            )

            report_content = output_path.read_text(encoding="utf-8")

            self.assertIn("# Asset Index Report", report_content)
            self.assertIn("**Total Files:** 2", report_content)
            self.assertIn("**Total Size:** 300.00 B", report_content)
            self.assertIn("| .py | 1 |", report_content)
            self.assertIn("`src\\main.py`", report_content)


if __name__ == "__main__":
    unittest.main()