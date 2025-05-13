import os
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def patch_image_plugins(monkeypatch, tmp_path):
    # Change working directory
    monkeypatch.chdir(tmp_path)
    import plugins.image as pi
    # Stub perform_ocr
    monkeypatch.setattr(pi, 'perform_ocr', lambda path: 'extracted text')
    # Stub convert_to_pdf
    monkeypatch.setattr(pi, 'convert_to_pdf', lambda path: 'output.pdf')
    # Stub convert_to_docx
    monkeypatch.setattr(pi, 'convert_to_docx', lambda path: 'output.docx')
    # Stub convert_format
    monkeypatch.setattr(pi, 'convert_format', lambda path, fmt: f'converted.{fmt}')
    yield

@pytest.mark.parametrize("args,expected", [
    (["image", "--input-path", "file.jpg", "--actions", "ocr"], ['extracted text']),
    (["image", "--input-path", "file.jpg", "--actions", "to-pdf"], ['output.pdf']),
    (["image", "--input-path", "file.jpg", "--actions", "to-docx"], ['output.docx']),
    (["image", "--input-path", "file.jpg", "--actions", "convert", "--target-format", "webp"], ['converted.webp']),
    (["image", "--input-path", "file.jpg", "--actions", "ocr", "--actions", "to-pdf", "--actions", "to-docx", "--actions", "convert", "--target-format", "png"], 
     ['extracted text', 'output.pdf', 'output.docx', 'converted.png']),
])
def test_cli_image_pipeline(args, expected):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    for exp in expected:
        assert exp in result.stdout
