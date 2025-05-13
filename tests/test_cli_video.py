import os
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def patch_video_plugins(monkeypatch, tmp_path):
    # 작업 디렉터리를 임시 폴더로 변경
    monkeypatch.chdir(tmp_path)
    # plugins.video의 헬퍼 함수들 스텁
    import plugins.video as pv
    monkeypatch.setattr(pv, 'extract_audio', lambda path, fmt: 'audio.mp3')
    monkeypatch.setattr(pv, 'get_transcript', lambda path: 'dummy transcript')
    monkeypatch.setattr(pv, 'summarize_text', lambda text, length: 'summary text')
    yield

@pytest.mark.parametrize("args,expected", [
    (["video", "--input-path", "dummy.mp4", "--actions", "audio"], ['audio.mp3']),
    (["video", "--input-path", "dummy.mp4", "--actions", "summary"], ['summary text']),
    (["video", "--input-path", "dummy.mp4", "--actions", "audio", "--actions", "summary"], ['audio.mp3', 'summary text']),
])
def test_cli_video_pipeline(args, expected):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    for exp in expected:
        assert exp in result.stdout
