import os
import pytest
from plugins.video import video_plugin
from core.schemas import ExecutionResult

class DummyYDL:
    def __init__(self, opts): pass
    def extract_info(self, url, download):
        # not used in video plugin
        return {'id': 'dummy'}
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

# Monkeypatch extract_audio and summarization utilities
@pytest.fixture(autouse=True)
def patch_video_helpers(monkeypatch, tmp_path):
    # ensure working dir
    monkeypatch.chdir(tmp_path)
    import plugins.video as pv
    # stub extract_audio to write dummy file
    def fake_extract_audio(path, fmt):
        fn = f"audio_fake.{fmt}"
        open(fn, 'wb').close()
        return str(tmp_path / fn)
    monkeypatch.setattr(pv, 'extract_audio', fake_extract_audio)
    # stub get_transcript to return fixed text
    monkeypatch.setattr(pv, 'get_transcript', lambda path: "dummy transcript")
    # stub summarize_text to return fixed summary
    monkeypatch.setattr(pv, 'summarize_text', lambda text, length: "fake summary")
    yield

@pytest.mark.parametrize("actions,expected", [
    (['audio'], ['audio']),
    (['summary'], ['summary']),
    (['audio', 'summary'], ['audio', 'summary']),
])
def test_video_plugin_actions(tmp_path, actions, expected):
    # prepare payload dict
    payload = {
        'input_path': 'dummy.mp4',
        'actions': actions,
        'audio_format': 'mp3',
        'summary_length': 'short'
    }
    result: ExecutionResult = video_plugin(payload)
    assert result.success
    # outputs keys
    assert sorted(list(result.outputs.keys())) == sorted(expected)
    # files exist for audio
    if 'audio' in expected:
        assert os.path.isfile(result.outputs['audio'])
    # summary should match stub
    if 'summary' in expected:
        assert result.outputs['summary'] == 'fake summary'
