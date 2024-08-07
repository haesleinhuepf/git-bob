def test_remove_outer_markdown():
    from git_bob._utilities import remove_outer_markdown
    assert remove_outer_markdown("""```python
bla
```""") == "bla"

def test_split_content_and_summary():
    from git_bob._utilities import split_content_and_summary
    content, summary = split_content_and_summary("""blabla
                                                 
                                                 summary""")

    assert content.strip() == "blabla"
    assert summary == "summary"

    content, summary = split_content_and_summary("""blabla

                                                     summary
                                                     """)

    assert content.strip() == "blabla"
    assert summary == "summary"
