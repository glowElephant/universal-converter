import pytest
from plugins.youtube import summarize_text

class DummyResponse:
    class Choice:
        def __init__(self, text):
            self.message = type("M", (), {"content": text})
    def __init__(self, text):
        self.choices = [DummyResponse.Choice(text)]

@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    # Patch openai.ChatCompletion.create to return DummyResponse
    class DummyChatCompletion:
        @staticmethod
        def create(model, messages):
            return DummyResponse("여기는 요약된 텍스트입니다.")
    import openai
    monkeypatch.setattr(openai, 'ChatCompletion', DummyChatCompletion)
    yield


def test_summarize_text_short():
    result = summarize_text("원본 긴 텍스트", "short")
    assert "요약된 텍스트" in result


def test_summarize_text_detailed():
    result = summarize_text("원본 긴 텍스트", "detailed")
    assert "요약된 텍스트" in result
