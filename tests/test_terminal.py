import pytest
from git_bob._terminal import TimeoutHandler
from git_bob._log import Log

def test_timeout_handler_logs():
    log = Log()
    handler = TimeoutHandler(timeout=1, log=log)
    
    # Simulate timeout
    handler._handle_timeout(None, None)
    
    # Check if log entries were printed
    captured = capsys.readouterr()
    assert "Summary:" in captured.out
    assert "Log entries:" in captured.out
