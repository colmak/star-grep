import unittest
from stargrep.output import highlight_match, format_line, COLOR_RESET, COLOR_FILENAME, COLOR_LINE_NUM, COLOR_MATCH

class TestOutput(unittest.TestCase):
    def test_highlight_match_no_color(self):
        line = "hello world"
        result = highlight_match(line, [(0, 5)], use_color=False)
        self.assertEqual(result, "hello world")

    def test_highlight_match_with_color(self):
        line = "hello world"
        result = highlight_match(line, [(0, 5)], use_color=True)
        # Expected: MATCH hello RESET  world
        expected = f"{COLOR_MATCH}hello{COLOR_RESET} world"
        self.assertEqual(result, expected)

    def test_highlight_match_multiple(self):
        line = "hello hello"
        result = highlight_match(line, [(0, 5), (6, 11)], use_color=True)
        expected = f"{COLOR_MATCH}hello{COLOR_RESET} {COLOR_MATCH}hello{COLOR_RESET}"
        self.assertEqual(result, expected)

    def test_format_line_no_color(self):
        result = format_line("test.py", 14, "import os", use_color=False, is_context=False)
        self.assertEqual(result, "test.py:14:import os")
        
        result_ctx = format_line("test.py", 14, "import os", use_color=False, is_context=True)
        self.assertEqual(result_ctx, "test.py-14-import os")

    def test_format_line_with_color(self):
        result = format_line("test.py", 14, "import os", use_color=True, is_context=False)
        expected = f"{COLOR_FILENAME}test.py{COLOR_RESET}:{COLOR_LINE_NUM}14{COLOR_RESET}:import os"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
