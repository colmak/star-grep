import unittest
import os
import tempfile
from pathlib import Path
from walker import is_binary, walk_paths

class TestWalker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)
        
        self.text_file = self.test_dir_path / "test.txt"
        self.text_file.write_text("Hello World", encoding='utf-8')
        
        self.bin_file = self.test_dir_path / "test.bin"
        self.bin_file.write_bytes(b"Hello \x00 World")
        
        self.sub_dir = self.test_dir_path / "subdir"
        self.sub_dir.mkdir()
        self.sub_text_file = self.sub_dir / "sub_test.txt"
        self.sub_text_file.write_text("Subdir Hello", encoding='utf-8')

    def tearDown(self):
        self.test_dir.cleanup()

    def test_is_binary(self):
        self.assertFalse(is_binary(self.text_file))
        self.assertTrue(is_binary(self.bin_file))

    def test_walk_paths_non_recursive(self):
        paths = list(walk_paths([str(self.test_dir_path)], recursive=False))
        # It's a directory and recursive is False, so it should be skipped
        # and print an error message (we don't catch stdout here but it shouldn't yield)
        self.assertEqual(len(paths), 0)

        # Passing the file directly
        paths = list(walk_paths([str(self.text_file)], recursive=False))
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], self.text_file)

    def test_walk_paths_recursive(self):
        paths = list(walk_paths([str(self.test_dir_path)], recursive=True))
        # Should yield text files, but binary should be skipped
        self.assertIn(self.text_file, paths)
        self.assertIn(self.sub_text_file, paths)
        self.assertNotIn(self.bin_file, paths)
        self.assertEqual(len(paths), 2)

if __name__ == '__main__':
    unittest.main()
