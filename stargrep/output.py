import sys
import re

# ANSI Escape Sequences
COLOR_RESET = "\033[0m"
COLOR_FILENAME = "\033[35m"    # Purple
COLOR_LINE_NUM = "\033[32m"    # Green
COLOR_MATCH = "\033[1;31m"     # Bold Red
COLOR_CONTEXT_SEP = "\033[36m" # Cyan (optional, for '--')

def highlight_match(line: str, match_spans: list[tuple[int, int]], use_color: bool) -> str:
    """Highlights match spans in a line using bold red."""
    if not use_color or not match_spans:
        return line
        
    result = []
    last_idx = 0
    # Process spans in order (they should already be sorted and non-overlapping)
    for start, end in match_spans:
        result.append(line[last_idx:start])
        result.append(f"{COLOR_MATCH}{line[start:end]}{COLOR_RESET}")
        last_idx = end
    result.append(line[last_idx:])
    return "".join(result)

def format_line(filename: str, line_num: int, content: str, use_color: bool, is_context: bool = False) -> str:
    """Formats a single match or context line."""
    content = content.rstrip('\r\n')
    sep = "-" if is_context else ":"
    
    if not use_color:
        return f"{filename}{sep}{line_num}{sep}{content}"
        
    colored_fname = f"{COLOR_FILENAME}{filename}{COLOR_RESET}"
    colored_lnum = f"{COLOR_LINE_NUM}{line_num}{COLOR_RESET}"
    
    return f"{colored_fname}{sep}{colored_lnum}{sep}{content}"

def print_separator(use_color: bool):
    """Prints the '--' separator between context blocks."""
    sep = "--"
    if use_color:
        sep = f"{COLOR_CONTEXT_SEP}{sep}{COLOR_RESET}"
    print(sep)
