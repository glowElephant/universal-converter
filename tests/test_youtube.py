import os
import pytest
from plugins.youtube import download_video
from yt_dlp import YoutubeDL

class DummyInfo:
    def __init__(self, video_id):
        self.id = video_id
        self.ext = 'mp4'

class DummyYDL:
    def __init__(self, opts):
        self.opts = opts
    def extract_info(self, url, download):
        # Simulate extraction by creating a dummy file
        video_id = 'test123'
        filename = f"{video_id}.mp4"
        with open(filename, 'wb') as f:
            f.write(b"dummy video content")
        return {'id': video_id}
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

@ pytest.fixture(autouse=True)
def patch_yt_dlp(monkeypatch):
    # Patch YoutubeDL to use DummyYDL
    monkeypatch.setattr('plugins.youtube.YoutubeDL', DummyYDL)
    yield
    # Cleanup created file
    try:
        os.remove('test123.mp4')
    except FileNotFoundError:
        pass


def test_download_video_creates_file(tmp_path):
    url = 'https://youtu.be/dummy'
    # Change working directory to tmp_path
    os.chdir(tmp_path)
    output_path = download_video(url, '720p')
    # Check file exists
    assert os.path.isfile(output_path)
    assert output_path.endswith('.mp4')
