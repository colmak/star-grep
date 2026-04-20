import re
from pathlib import Path
from collections import deque
from typing import Iterator, Tuple

def get_match_spans(pattern: re.Pattern, text: str) -> list[tuple[int, int]]:
    """Returns a list of (start, end) index pairs for all matches in the text."""
    return [match.span() for match in pattern.finditer(text)]

def search_file(
    file_path: Path, 
    pattern: re.Pattern, 
    invert_match: bool, 
    context_size: int
) -> Iterator[Tuple[str, int, str, list[tuple[int, int]]]]:
    """
    Reads a file line by line and yields matched or context lines.
    Yields tuples of (type, line_num, content, match_spans).
    Types can be: 'match', 'context', or 'separator'.
    """
    # Deque to hold (line_num, line_text) for before-context
    before_buffer = deque(maxlen=context_size)
    after_counter = 0
    last_printed_line_num = 0
    
    try:
        # Using utf-8, replace errors to avoid crashing on mis-sniffed semi-binary files
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f, start=1):
                # Check for match
                is_match = False
                spans = []
                
                if invert_match:
                    is_match = not bool(pattern.search(line))
                else:
                    spans = get_match_spans(pattern, line)
                    is_match = bool(spans)
                    
                if is_match:
                    # We found a match. 
                    # 1. Print separator if there's a gap
                    first_line_to_print = before_buffer[0][0] if before_buffer else i
                    if last_printed_line_num > 0 and first_line_to_print > last_printed_line_num + 1:
                        yield ("separator", 0, "", [])
                        
                    # 2. Flush before_buffer as context lines
                    for ctx_num, ctx_line in before_buffer:
                        yield ("context", ctx_num, ctx_line, [])
                    before_buffer.clear()
                    
                    # 3. Yield the matched line
                    yield ("match", i, line, spans)
                    last_printed_line_num = i
                    
                    # 4. Set after_counter
                    after_counter = context_size
                    
                else:
                    # Not a matched line
                    if after_counter > 0:
                        # Yield as after-context
                        yield ("context", i, line, [])
                        last_printed_line_num = i
                        after_counter -= 1
                    else:
                        # Add to before-context buffer if we have context_size > 0
                        if context_size > 0:
                            before_buffer.append((i, line))
                            
    except Exception as e:
        # Ignore files we can't read for any other reason (permissions, etc)
        pass
