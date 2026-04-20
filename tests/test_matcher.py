import unittest
import re
import tempfile
from pathlib import Path
from stargrep.matcher import get_match_spans, search_file

class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.test_dir.name) / "test.txt"
        
        content = (
            "Line 1: The quick brown fox\n"
            "Line 2: jumps over the\n"
            "Line 3: lazy dog.\n"
            "Line 4: Hello World\n"
            "Line 5: Python is great.\n"
        )
        self.test_file.write_text(content, encoding='utf-8')

    def tearDown(self):
        self.test_dir.cleanup()

    def test_get_match_spans(self):
        pattern = re.compile(r"o")
        spans = get_match_spans(pattern, "foo bar baz")
        self.assertEqual(spans, [(1, 2), (2, 3)])

    def test_search_file_basic(self):
        pattern = re.compile(r"Hello")
        results = list(search_file(self.test_file, pattern, invert_match=False, context_size=0))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "match")
        self.assertEqual(results[0][1], 4)
        self.assertIn("Hello World", results[0][2])

    def test_search_file_invert(self):
        pattern = re.compile(r"Line")
        # All lines have "Line", so nothing should match with invert
        results = list(search_file(self.test_file, pattern, invert_match=True, context_size=0))
        self.assertEqual(len(results), 0)
        
        pattern2 = re.compile(r"dog")
        # Line 3 has dog. Invert should yield 1, 2, 4, 5
        results2 = list(search_file(self.test_file, pattern2, invert_match=True, context_size=0))
        self.assertEqual(len(results2), 4)

    def test_search_file_context(self):
        pattern = re.compile(r"lazy")
        # Should match line 3. Context 1 should yield line 2, line 3, line 4
        results = list(search_file(self.test_file, pattern, invert_match=False, context_size=1))
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], ("context", 2, "Line 2: jumps over the\n", []))
        self.assertEqual(results[1][0], "match")
        self.assertEqual(results[1][1], 3)
        self.assertEqual(results[2], ("context", 4, "Line 4: Hello World\n", []))

    def test_search_file_overlapping_context(self):
        # Line 1: The quick brown fox
        # Line 2: jumps over the
        # Line 3: lazy dog.
        pattern = re.compile(r"fox|dog")
        # Matches line 1 and 3. Context 1.
        # Should yield:
        # Match L1
        # Context L2 (after context for L1, before context for L3)
        # Match L3
        # Context L4 (after context for L3)
        results = list(search_file(self.test_file, pattern, invert_match=False, context_size=1))
        
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0][0], "match")
        self.assertEqual(results[0][1], 1)
        
        self.assertEqual(results[1][0], "context")
        self.assertEqual(results[1][1], 2)
        
        self.assertEqual(results[2][0], "match")
        self.assertEqual(results[2][1], 3)
        
        self.assertEqual(results[3][0], "context")
        self.assertEqual(results[3][1], 4)

if __name__ == '__main__':
    unittest.main()
