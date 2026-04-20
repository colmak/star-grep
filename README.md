# star-grep

`star-grep` is a powerful, Python-based alternative to the standard `grep` command. It supports regular expressions natively, highlights output using ANSI colors, easily searches recursively, and efficiently skips binary files.

## Features

- **Regex Support**: Pass any Python-compatible regex. 
- **Recursive Search (`-r`)**: Rapidly traverse directories.
- **Binary File Skipping**: Smartly avoids spamming your terminal with binary output.
- **Visual Clarity**: Bold red highlighted text, purple filenames, and green line numbers for instant legibility. Auto-disables color when piped or optionally via `--no-color`.
- **Match Inversion (`-v`)**: Print lines that do *not* match.
- **Context Output (`-C N`)**: See `N` lines of context before and after matching lines.
- **Case Insensitive (`-i`)**: Match easily without worrying about casing.
- **Counting (`--count`)**: Get a simple summary of occurrences per file.

## Installation

Instead of running a flat script, `star-grep` is a true Python package.

```bash
# We recommend using a virtualenv or pipx
pip install .
```

## Usage

Once installed, the `star-grep` command will be available natively in your terminal!

```bash
# Basic file search
star-grep "pattern" file.txt

# Recursive case-insensitive search
star-grep -ri "TODO" src/

# Search and show 3 lines of context
star-grep -C 3 "def main" *.py

# Invert match (all lines NOT containing pattern)
star-grep -v "^#" config.txt
```

## Testing

A test suite is included utilizing Python's built-in `unittest` framework.

```bash
# Run all tests
python3 -m unittest discover tests
```
