import os
import pytest
from plugins.youtube import extract_audio

class DummyYDL:
    def __init__(self, opts):
        self.opts = opts

    def extract_info(self, url, download):
        # Simulate extraction by creating a dummy audio file
        audio_id = 'audio123'
        ext = self.opts.get('postprocessors', [{}])[0].get('preferredcodec', 'mp3')
        filename = f"{audio_id}.{ext}"
        with open(filename, 'wb') as f:
            f.write(b"dummy audio content")
        return {'id': audio_id}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

@pytest.fixture(autouse=True)
def patch_yt_dlp(monkeypatch):
    # Patch YoutubeDL to use DummyYDL
    monkeypatch.setattr('plugins.youtube.YoutubeDL', DummyYDL)
    yield
    # Cleanup created file
    try:
        os.remove('audio123.mp3')
    except FileNotFoundError:
        pass

def test_extract_audio_creates_file(tmp_path):
    # Change working directory to tmp_path
    os.chdir(tmp_path)
    output_path = extract_audio('https://youtu.be/dummy', 'mp3')
    assert os.path.isfile(output_path)
    assert output_path.endswith('.mp3')
