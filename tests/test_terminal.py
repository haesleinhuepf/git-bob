import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
sys.path.append('..')
from _terminal import handle_timeout

class TestTerminal(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_timeout_prints_log(self, mock_stdout):
        mock_log = MagicMock()
        mock_log.getvalue.return_value = "Test log output"
        
        handle_timeout(mock_log)
        
        self.assertIn("Test log output", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
