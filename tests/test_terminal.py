import pytest
from unittest.mock import patch, MagicMock
from your_module import terminal  # Replace 'your_module' with the actual module name

def test_log_printed_on_timeout():
    mock_logger = MagicMock()
    
    with patch('your_module.terminal.logger', mock_logger):
        with pytest.raises(TimeoutError):
            terminal.run_with_timeout(1)  # Assuming a function that simulates timeout
    
    mock_logger.info.assert_called()  # Check if log was printed

def test_log_printed_on_normal_execution():
    mock_logger = MagicMock()
    
    with patch('your_module.terminal.logger', mock_logger):
        terminal.run_normally()  # Assuming a function for normal execution
    
    mock_logger.info.assert_called()  # Check if log was printed
