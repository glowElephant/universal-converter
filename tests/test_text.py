import os
import pytest
from plugins.text import text_plugin
from core.schemas import ExecutionResult

@pytest.fixture(autouse=True)
def patch_text_helpers(monkeypatch, tmp_path):
    # Change working directory to temp path
    monkeypatch.chdir(tmp_path)
    import plugins.text as pt
    # Stub summarize_text_from_file to return fixed summary
    monkeypatch.setattr(pt, 'summarize_text_from_file', lambda path, length: 'fake summary')
    # Stub text_to_speech to create dummy audio file
    def fake_tts(path, fmt):
        fn = f"output.{fmt}"
        open(fn, 'wb').close()
        return str(tmp_path / fn)
    monkeypatch.setattr(pt, 'text_to_speech', fake_tts)
    # Stub text_to_pdf to create dummy pdf file
    monkeypatch.setattr(pt, 'text_to_pdf', lambda path: str(tmp_path / 'output.pdf'))
    open(str(tmp_path / 'output.pdf'), 'wb').close()
    # Stub text_to_image to create dummy image file
    monkeypatch.setattr(pt, 'text_to_image', lambda path: str(tmp_path / 'output.png'))
    open(str(tmp_path / 'output.png'), 'wb').close()
    yield

@pytest.mark.parametrize("actions,expected_keys,expected_files", [
    (['summarize'], ['summary'], []),
    (['tts'], ['audio'], ['output.mp3']),
    (['to-pdf'], ['pdf'], ['output.pdf']),
    (['to-image'], ['image'], ['output.png']),
    (['summarize','tts','to-pdf','to-image'], ['summary','audio','pdf','image'], ['output.mp3','output.pdf','output.png']),
])
def test_text_plugin(actions, expected_keys, expected_files):
    payload = {
        'input_path': 'input.txt',
        'actions': actions,
        'summary_length': 'short',
        'tts_format': 'mp3'
    }
    result: ExecutionResult = text_plugin(payload)
    assert result.success
    # Check output keys
    assert sorted(result.outputs.keys()) == sorted(expected_keys)
    # Check generated files for file-based outputs
    for key in ['audio','pdf','image']:
        if key in result.outputs:
            path = result.outputs[key]
            assert os.path.isfile(path)
