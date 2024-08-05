def test_log():
    from git_bob._logger import Log
    log = Log()
    log.clear()
    log.log("Hello")
    assert log.get() == ["Hello"]
    log.log("World")
    assert log.get() == ["Hello", "World"]
