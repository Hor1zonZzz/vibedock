# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VibehHacks is a Python code analysis tool that analyzes third-party package imports and usage in Python projects. It provides detailed statistics, reports, and exports for understanding dependencies.

## Core Architecture

### Module Structure
- `vibehacks/cli.py`: Command-line interface using Click
- `vibehacks/analyzer.py`: Core analysis engine (`ImportAnalyzer` class)
- `vibehacks/reporter.py`: Report generation (`AnalysisReporter` class)

### Key Components

**ImportAnalyzer** (`analyzer.py:13`):
- Analyzes Python AST to extract import statements and usage patterns
- Distinguishes between third-party packages, stdlib, and project modules
- Tracks functions, classes, modules, and their usage frequencies
- Main methods: `analyze_project()`, `analyze_imports()`, `analyze_usage()`

**AnalysisReporter** (`reporter.py:17`):
- Generates console reports using Rich library for formatting
- Exports data to JSON and CSV formats
- Main methods: `print_detailed_report()`, `export_to_json()`, `export_to_csv()`

## Common Development Commands

### Installation and Setup
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]
```

### Running the Tool
```bash
# Basic analysis
python -m vibehacks.cli analyze /path/to/project

# With exports
python -m vibehacks.cli analyze . --output-json report.json --output-csv ./reports

# Specific package analysis
python -m vibehacks.cli analyze . --package pandas

# Using the installed command
vibehacks analyze /path/to/project
```

### Testing
```bash
# Run tests (if pytest is configured)
pytest

# Run with coverage
pytest --cov=vibehacks
```

### Development Notes

**Package Detection Logic** (`analyzer.py:76-88`):
- Third-party packages are detected by excluding stdlib modules and project modules
- Project modules are currently hardcoded to exclude 'vibehacks' - update this for other projects

**AST Analysis** (`analyzer.py:110-136`, `analyzer.py:166-208`):
- Uses AST walking to find import statements and usage patterns
- Handles both `import` and `from...import` statements
- Tracks aliases and maps them to original names for usage counting

**Ignore Patterns** (`analyzer.py:18-22`):
- Automatically skips common directories like `__pycache__`, `.git`, `venv`, `build`, etc.
- Only processes `.py` files

**Report Generation**:
- Console output uses Rich library for colored tables and panels
- JSON export converts sets to lists for serialization
- CSV export uses pandas for structured data output

## Dependencies

Core runtime dependencies:
- `click>=8.0.0`: CLI framework
- `rich>=13.0.0`: Console formatting and tables
- `pandas>=2.0.0`: Data processing and CSV export
- `ast-tools>=0.1.0`: AST analysis enhancement
- `matplotlib>=3.7.0`: Visualization support
- `seaborn>=0.12.0`: Statistical plotting

Development dependencies:
- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=4.0.0`: Coverage reporting