# System: star-grep

<metadata>
project_name: star-grep
description: Python-based CLI search utility resembling grep.
core_technologies: ["Python 3.9+", "argparse", "re", "pathlib"]
installation_method: "pip install ."
entry_point: "star-grep via stargrep.cli.main"
</metadata>

## Core Capabilities
- Native Python regex parsing.
- Recursive directory traversal with auto-detection/skipping of binary files (heuristic: searches first 1024 bytes for \x00).
- Context window support (before/after matching lines).
- Invert matching (exclude lines matching pattern).
- ANSI color highlighted output (Match: Bold Red, File: Purple, Line: Green). Overridable.

## CLI Interface Reference
Command structure: `star-grep [OPTIONS] PATTERN [PATHS ...]`

### Positional Arguments
- `pattern`: Regular expression string to search for.
- `paths`: One or more file or directory paths to execute the search against.

### Optional Flags
- `-i`, `--ignore-case`: Enable case-insensitive matching (`re.IGNORECASE`).
- `-v`, `--invert-match`: Select non-matching lines exclusively.
- `-r`, `--recursive`: Walk directories recursively.
- `--no-color`: Disable all ANSI color sequence outputs.
- `--count`: Suppress standard output; print only a count of matching lines per file `<filepath>:<count>`.
- `-C N`, `--context N`: Print `N` lines of context before and after each matched block. Separates non-contiguous match blocks with `--`.

## Internal Architecture
<architecture>
stargrep/cli.py: Maps argparse inputs to logic workflow. Handles stdout streams.
stargrep/matcher.py: Core streaming engine. Yields matching lines and context buffers using collections.deque state tracking.
stargrep/walker.py: File system iterative parser. Handles os.walk and binary file filtering natively.
stargrep/output.py: Formatting module wrapping payload in terminal-compliant ANSI sequences.
</architecture>

## Testing
Module tested via standard library `unittest`.
Execution command: `python3 -m unittest discover tests`
Coverage: 13/13 passing tests. Evaluates binary detection, context buffering mechanisms, output formatting, and regex compilations.
