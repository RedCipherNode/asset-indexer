import tempfile
import unittest
from pathlib import Path

from asset_indexer.file_scanner import scan_directory


class FileScannerTests(unittest.TestCase):
    def test_scan_directory_returns_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)

            (root_path / "notes.txt").write_text("hello", encoding="utf-8")
            (root_path / "nested").mkdir()
            (root_path / "nested" / "data.json").write_text(
                "{}",
                encoding="utf-8",
            )

            file_records = scan_directory(root_path)

            scanned_paths = {
                file_record.path.relative_to(root_path)
                for file_record in file_records
            }

            self.assertEqual(
                scanned_paths,
                {
                    Path("notes.txt"),
                    Path("nested/data.json"),
                },
            )

    def test_scan_directory_excludes_default_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)

            (root_path / "keep.txt").write_text("keep", encoding="utf-8")

            excluded_path = root_path / "__pycache__"
            excluded_path.mkdir()
            (excluded_path / "cached.pyc").write_bytes(b"cache")

            file_records = scan_directory(root_path)

            scanned_paths = {
                file_record.path.relative_to(root_path)
                for file_record in file_records
            }

            self.assertEqual(scanned_paths, {Path("keep.txt")})

    def test_scan_directory_excludes_custom_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)

            (root_path / "keep.txt").write_text("keep", encoding="utf-8")

            build_path = root_path / "build"
            build_path.mkdir()
            (build_path / "artifact.bin").write_bytes(b"artifact")

            file_records = scan_directory(
                root_path=root_path,
                excluded_directories=["build"],
            )

            scanned_paths = {
                file_record.path.relative_to(root_path)
                for file_record in file_records
            }

            self.assertEqual(scanned_paths, {Path("keep.txt")})


if __name__ == "__main__":
    unittest.main()