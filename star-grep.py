#!/usr/bin/env python3
import argparse
import re
import sys

from matcher import search_file
from walker import walk_paths
from output import highlight_match, format_line, print_separator

def main():
    parser = argparse.ArgumentParser(
        description="star-grep: A clean, powerful Python-based grep-like tool."
    )
    parser.add_argument("pattern", help="Regular expression to search for")
    parser.add_argument("paths", nargs="+", help="Files or directories to search")
    
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Ignore case distinctions")
    parser.add_argument("-v", "--invert-match", action="store_true", help="Select non-matching lines")
    parser.add_argument("-r", "--recursive", action="store_true", help="Read all files under each directory, recursively")
    parser.add_argument("--no-color", action="store_true", help="Disable color output")
    
    parser.add_argument("--count", action="store_true", help="Only print a count of matching lines per file")
    parser.add_argument("-C", "--context", type=int, default=0, help="Print NUM lines of output context")
    
    args = parser.parse_args()
    
    # 1. Compile regex
    flags = 0
    if args.ignore_case:
        flags |= re.IGNORECASE
        
    try:
        pattern = re.compile(args.pattern, flags)
    except re.error as e:
        print(f"star-grep: Invalid regular expression: {e}", file=sys.stderr)
        sys.exit(2)
        
    use_color = not args.no_color
    if not sys.stdout.isatty():
        # Automatically disable color if output is piped, unless user forces it (not supported via args but a good default)
        use_color = False
        
    # We may still want color if not --no-color and sys.stdout.isatty()
    use_color = not args.no_color and sys.stdout.isatty()
    # Actually, let's strictly follow the flag, but default to checking isatty
    if args.no_color:
        use_color = False
        
    # 2. Iterate over files
    for file_path in walk_paths(args.paths, args.recursive):
        match_count = 0
        
        for type_str, line_num, content, match_spans in search_file(
            file_path, pattern, args.invert_match, args.context
        ):
            if type_str == "match":
                match_count += 1
                
            if not args.count:
                if type_str == "separator":
                    print_separator(use_color)
                else:
                    highlighted_content = highlight_match(content, match_spans, use_color)
                    is_context = (type_str == "context")
                    formatted = format_line(str(file_path), line_num, highlighted_content, use_color, is_context)
                    print(formatted)
                    
        if args.count:
            # Format count output: filename:count
            if use_color:
                from output import COLOR_FILENAME, COLOR_RESET
                colored_fname = f"{COLOR_FILENAME}{file_path}{COLOR_RESET}"
                print(f"{colored_fname}:{match_count}")
            else:
                print(f"{file_path}:{match_count}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
