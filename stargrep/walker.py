import os
from pathlib import Path
from typing import Iterator

def is_binary(filepath: Path) -> bool:
    """
    Heuristically checks if a file is binary by looking for a null byte
    in the first 1024 bytes.
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        # If we can't open it (e.g. permission error, broken symlink), treat as binary/skip
        return True

def walk_paths(paths: list[str], recursive: bool) -> Iterator[Path]:
    """
    Iterates over the given paths. If recursive is True, it walks through
    directories. Yields Path objects for files that are not binary.
    """
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"star-grep: {p}: No such file or directory")
            continue

        if path.is_file():
            if not is_binary(path):
                yield path
        elif path.is_dir():
            if not recursive:
                print(f"star-grep: {p}: Is a directory")
                continue
            
            # Recursive traversal
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.is_file() and not file_path.is_symlink() and not is_binary(file_path):
                        yield file_path
