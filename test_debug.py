import re
from pathlib import Path
from matcher import search_file

p = Path("test_debug.txt")
p.write_text("Line 1\nLine 2\nLine 3 dog\nLine 4\nLine 5\n")
pattern = re.compile(r"dog")
print(list(search_file(p, pattern, True, 0)))
