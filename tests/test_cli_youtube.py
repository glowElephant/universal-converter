import os
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def patch_plugins(monkeypatch, tmp_path):
    # 작업 디렉터리를 임시 폴더로 변경
    monkeypatch.chdir(tmp_path)
    # plugins.youtube의 각 함수 스텁으로 대체
    import plugins.youtube as py_youtube
    monkeypatch.setattr(py_youtube, 'download_video', lambda url, q: 'video.mp4')
    monkeypatch.setattr(py_youtube, 'extract_audio', lambda url, fmt: 'audio.mp3')
    monkeypatch.setattr(py_youtube, 'get_transcript', lambda url: 'dummy transcript')
    monkeypatch.setattr(py_youtube, 'summarize_text', lambda text, length: 'summarized text')
    yield


def test_cli_youtube_full_pipeline():
    # 단일 커맨드 앱이므로 서브명 없이 옵션만 전달
    args = [
        "--url", "https://youtu.be/dummy",
        "--actions", "video",
        "--actions", "audio",
        "--actions", "summary",
    ]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    output = result.stdout
    assert "video.mp4" in output
    assert "audio.mp3" in output
    assert "summarized text" in output
