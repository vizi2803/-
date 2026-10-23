import io
import sys
import unittest
from unittest.mock import patch
from src.main import execute_command, process_command_line, parse_cli_args
from src.vfs import VFS, load_vfs_from_directory

class TestStage2Configuration(unittest.TestCase):
    def test_cli_arguments_parsing(self):
        test_args = ["prog", "--vfs", "/path/to/vfs", "--script", "run.txt"]
        with patch.object(sys, "argv", test_args):
            parsed = parse_cli_args()
            self.assertEqual(parsed.vfs, "/path/to/vfs")
            self.assertEqual(parsed.script, "run.txt")

    def test_script_faulty_line_skipping(self):
        captured = io.StringIO()
        mock_vfs = VFS("test_vfs")
        with patch("sys.stdout", captured):
            should_exit = process_command_line("cd dir1 dir2", mock_vfs)
            self.assertFalse(should_exit)
            output = captured.getvalue()
            self.assertIn("cd: too many arguments", output)

    def test_command_exit_signals_termination(self):
        msg, should_exit = execute_command(["exit"])
        self.assertEqual(msg, "")
        self.assertTrue(should_exit)

class TestStage3VFS(unittest.TestCase):
    def test_load_vfs_non_existent_directory(self):
        vfs, err = load_vfs_from_directory("tests/non_existent_folder_xyz")
        self.assertIsNone(vfs)
        self.assertIn("does not exist", err)

    def test_load_vfs_path_is_file(self):
        vfs, err = load_vfs_from_directory("tests/test_shell.py")
        self.assertIsNone(vfs)
        self.assertIn("is not a directory", err)

    def test_load_vfs_minimal_structure(self):
        vfs, err = load_vfs_from_directory("tests/vfs_minimal")
        self.assertIsNone(err)
        self.assertIsNotNone(vfs)
        self.assertEqual(vfs.root_name, "vfs_minimal")
        self.assertTrue(vfs.node_exists(["empty.txt"]))

if __name__ == "__main__":
    unittest.main()