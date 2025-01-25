import pytest

@pytest.mark.manual
def test_anthropic():
    from git_bob._endpoints import prompt_anthropic
    assert "ok" in str(prompt_anthropic("Answer with ok!")).lower()

@pytest.mark.manual
def test_openai():
    from git_bob._endpoints import prompt_openai
    assert "ok" in str(prompt_openai("Answer with ok!")).lower()

@pytest.mark.manual
def test_google():
    from git_bob._endpoints import prompt_googleai
    assert "ok" in str(prompt_googleai("Answer with ok!")).lower()

@pytest.mark.manual
def test_mistral():
    from git_bob._endpoints import prompt_mistral
    assert "ok" in str(prompt_mistral("Answer with ok!")).lower()

@pytest.mark.manual
def test_azure():
    from git_bob._endpoints import prompt_azure
    assert "ok" in str(prompt_azure("Answer with ok!", model="gpt-4o-mini")).lower()

@pytest.mark.manual
def test_deepseek():
    from git_bob._endpoints import prompt_deepseek
    assert "ok" in str(prompt_deepseek("Answer with ok!")).lower()
