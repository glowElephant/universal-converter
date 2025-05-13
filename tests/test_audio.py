import os
import pytest
from plugins.audio import audio_plugin
from core.schemas import ExecutionResult

@pytest.fixture(autouse=True)
def patch_audio_helpers(monkeypatch, tmp_path):
    # Change working directory to temp path
    monkeypatch.chdir(tmp_path)
    import plugins.audio as pa
    # Stub convert_format to create a dummy converted file
    def fake_convert(path, fmt):
        filename = f"converted.{fmt}"
        open(filename, 'wb').close()
        return str(tmp_path / filename)
    monkeypatch.setattr(pa, 'convert_format', fake_convert)
    # Stub transcribe_audio to return fixed transcript
    monkeypatch.setattr(pa, 'transcribe_audio', lambda path: "dummy transcription")
    # Stub summarize_text to return fixed summary
    monkeypatch.setattr(pa, 'summarize_text', lambda text, length: "fake summary")
    yield

@pytest.mark.parametrize("actions,expected_keys", [
    (['convert'], ['converted']),
    (['summary'], ['summary']),
    (['convert', 'summary'], ['converted', 'summary']),
])
def test_audio_plugin_actions(tmp_path, actions, expected_keys):
    # Prepare payload for audio_plugin
    payload = {
        'input_path': 'input.wav',
        'actions': actions,
        'target_format': 'mp3',
        'summary_length': 'short'
    }
    result: ExecutionResult = audio_plugin(payload)
    assert result.success
    # Check output keys
    assert sorted(result.outputs.keys()) == sorted(expected_keys)
    # If convert, the converted file must exist
    if 'converted' in expected_keys:
        out_path = result.outputs['converted']
        assert os.path.isfile(out_path)
        assert out_path.endswith('.mp3')
    # If summary, check summary text
    if 'summary' in expected_keys:
        assert result.outputs['summary'] == 'fake summary'
