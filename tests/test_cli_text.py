import os
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def patch_text_plugins(monkeypatch, tmp_path):
    # Change working directory to temp path
    monkeypatch.chdir(tmp_path)
    import plugins.text as pt
    # Stub summarize_text_from_file
    monkeypatch.setattr(pt, 'summarize_text_from_file', lambda path, length: 'fake summary')
    # Stub text_to_speech
    monkeypatch.setattr(pt, 'text_to_speech', lambda path, fmt: 'output.mp3')
    # Stub text_to_pdf
    monkeypatch.setattr(pt, 'text_to_pdf', lambda path: 'output.pdf')
    # Stub text_to_image
    monkeypatch.setattr(pt, 'text_to_image', lambda path: 'output.png')
    yield

@pytest.mark.parametrize("args,expected", [
    (["text", "--input-path", "file.txt", "--actions", "summarize"], ['fake summary']),
    (["text", "--input-path", "file.txt", "--actions", "tts"], ['output.mp3']),
    (["text", "--input-path", "file.txt", "--actions", "to-pdf"], ['output.pdf']),
    (["text", "--input-path", "file.txt", "--actions", "to-image"], ['output.png']),
    (["text", "--input-path", "file.txt", "--actions", "summarize", "--actions", "tts", "--actions", "to-pdf", "--actions", "to-image"],
     ['fake summary', 'output.mp3', 'output.pdf', 'output.png']),
])
def test_cli_text_pipeline(args, expected):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    for exp in expected:
        assert exp in result.stdout
