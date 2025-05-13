import os
import glob
import pytest
from plugins.youtube import get_transcript

class DummyYDL:
    def __init__(self, opts):
        self.opts = opts

    def extract_info(self, url, download):
        # Simulate creation of a .vtt subtitle file
        video_id = 'vid123'
        vtt_filename = f"{video_id}.en.vtt"
        with open(vtt_filename, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n안녕하세요\n\n")
            f.write("00:00:01.000 --> 00:00:02.000\n테스트입니다\n")
        return {'id': video_id}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

@pytest.fixture(autouse=True)
def patch_yt_dlp(monkeypatch, tmp_path):
    # Patch YoutubeDL to use DummyYDL and change working directory
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('PWD', str(tmp_path))
    monkeypatch.setattr('plugins.youtube.YoutubeDL', DummyYDL)
    yield
    # Cleanup any .vtt files
    for f in glob.glob(str(tmp_path / 'vid123*.vtt')):
        try:
            os.remove(f)
        except FileNotFoundError:
            pass


def test_get_transcript_from_vtt():
    text = get_transcript('https://youtu.be/dummy')
    assert '안녕하세요' in text
    assert '테스트입니다' in text
