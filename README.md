# Asset Indexer

A local-first Python CLI for scanning directories, analyzing file metadata, and generating reusable inventory reports.

## Features

- Recursive directory scanning
- Total file count and size summary
- Extension breakdown
- Largest file analysis
- JSON manifest export
- Markdown report export
- Default directory exclusions
- Custom directory exclusions
- Configurable largest-file limit
- Unit test coverage with `unittest`

## Requirements

- Python 3.10 or newer

## Quick Start

Run from the project root:

```powershell
$env:PYTHONPATH = "src"
python -m asset_indexer "." --output-dir output
```

## Usage

```powershell
python -m asset_indexer DIRECTORY [OPTIONS]
```

### Scan a Directory

```powershell
python -m asset_indexer "D:\Projects"
```

### Choose an Output Directory

```powershell
python -m asset_indexer "." --output-dir output
```

### Exclude Additional Directories

```powershell
python -m asset_indexer "." --exclude build dist examples
```

### Limit Large Files

Control how many files appear in the largest-files section:

```powershell
python -m asset_indexer "." --largest-limit 3
```

## Default Exclusion

The scanner ignores these directory names by default:

```powershell
.git
__pycache__
.venv
venv
node_modules
output
```

## Generated Files

The selected output directory contains:

```powershell
output/
├── manifest.json
└── report.md
```

## Manifest

manifest.json contains machine-readable scan data:

scanned root path
total file count
total size in bytes
extension statistics
largest files

## Report

report.md contains a human-readable Markdown summary:

scan overview
top extensions
largest files

## Testing

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Project structure

```powershell
'asset-indexer/
├── docs/
├── examples/
├── output/
├── src/
│   └── asset_indexer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── file_analyzer.py
│       ├── file_scanner.py
│       ├── models.py
│       └── report_writer.py
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
`
```

## Development Status

v0.1.0 — Core scanning, analysis, report export, exclusion support, and automated tests are implemented.

## License

MIT