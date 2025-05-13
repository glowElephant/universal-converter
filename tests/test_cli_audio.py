import os
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def patch_audio_plugins(monkeypatch, tmp_path):
    # 작업 디렉터리를 임시 폴더로 변경
    monkeypatch.chdir(tmp_path)
    import plugins.audio as pa
    # Stub convert_format to return dummy path
    monkeypatch.setattr(pa, 'convert_format', lambda path, fmt: 'converted.mp3')
    # Stub transcribe_audio to return dummy text
    monkeypatch.setattr(pa, 'transcribe_audio', lambda path: 'dummy transcription')
    # Stub summarize_text to return dummy summary
    monkeypatch.setattr(pa, 'summarize_text', lambda text, length: 'fake summary')
    yield

@pytest.mark.parametrize("args,expected", [
    (["audio", "--input-path", "file.wav", "--actions", "convert"], ['converted.mp3']),
    (["audio", "--input-path", "file.wav", "--actions", "summary"], ['fake summary']),
    (["audio", "--input-path", "file.wav", "--actions", "convert", "--actions", "summary"], ['converted.mp3', 'fake summary']),
])
def test_cli_audio_pipeline(args, expected):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    for exp in expected:
        assert exp in result.stdout
