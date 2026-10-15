import io
import sys
import unittest
from unittest.mock import patch
from src.main import execute_command, process_command_line, parse_cli_args

class TestStage2Configuration(unittest.TestCase):
    def test_cli_arguments_parsing(self):
        test_args = ["prog", "--vfs", "/path/to/vfs", "--script", "run.txt"]
        with patch.object(sys, "argv", test_args):
            parsed = parse_cli_args()
            self.assertEqual(parsed.vfs, "/path/to/vfs")
            self.assertEqual(parsed.script, "run.txt")

    def test_script_faulty_line_skipping(self):
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            should_exit = process_command_line("cd dir1 dir2", "test_vfs")
            self.assertFalse(should_exit)
            output = captured.getvalue()
            self.assertIn("cd: too many arguments", output)

    def test_command_exit_signals_termination(self):
        msg, should_exit = execute_command(["exit"])
        self.assertEqual(msg, "")
        self.assertTrue(should_exit)

if __name__ == "main":
    unittest.main()