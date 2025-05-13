import os
import pytest
from plugins.image import image_plugin
from core.schemas import ExecutionResult

@pytest.fixture(autouse=True)
def patch_image_helpers(monkeypatch, tmp_path):
    # Change working directory
    monkeypatch.chdir(tmp_path)
    import plugins.image as pi
    # Stub OCR to return fixed text
    monkeypatch.setattr(pi, 'perform_ocr', lambda path: 'extracted text')
    # Stub PDF conversion to create dummy file
    def fake_to_pdf(path):
        fn = 'output.pdf'
        open(fn, 'wb').close()
        return str(tmp_path / fn)
    monkeypatch.setattr(pi, 'convert_to_pdf', fake_to_pdf)
    # Stub DOCX conversion to create dummy file
    def fake_to_docx(path):
        fn = 'output.docx'
        open(fn, 'wb').close()
        return str(tmp_path / fn)
    monkeypatch.setattr(pi, 'convert_to_docx', fake_to_docx)
    # Stub format conversion to create dummy file
    def fake_convert(path, fmt):
        fn = f"converted.{fmt}"
        open(fn, 'wb').close()
        return str(tmp_path / fn)
    monkeypatch.setattr(pi, 'convert_format', fake_convert)
    yield

@pytest.mark.parametrize("actions,expected_keys,expected_files", [
    (['ocr'], ['text'], []),
    (['to-pdf'], ['pdf'], ['output.pdf']),
    (['to-docx'], ['docx'], ['output.docx']),
    (['convert'], ['converted'], ['converted.png']),  # assume target_format default 'png'
    (['ocr','to-pdf','to-docx','convert'], ['text','pdf','docx','converted'], ['output.pdf','output.docx','converted.png']),
])
def test_image_plugin(actions, expected_keys, expected_files):
    # Prepare payload
    payload = {
        'input_path': 'input.jpg',
        'actions': actions,
        'target_format': 'png'
    }
    result: ExecutionResult = image_plugin(payload)
    assert result.success
    # Check keys
    assert sorted(result.outputs.keys()) == sorted(expected_keys)
    # Check file existence for file-based outputs
    for key in ['pdf','docx','converted']:
        if key in result.outputs:
            path = result.outputs[key]
            assert os.path.isfile(path)
