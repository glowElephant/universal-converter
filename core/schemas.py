from pydantic import BaseModel
from typing import List, Any

class YouTubePayload(BaseModel):
    url: str
    actions: List[str]
    video_quality: str
    audio_format: str
    summary_length: str

class VideoPayload(BaseModel):
    input_path: str
    actions: List[str]     # ['audio', 'summary']
    audio_format: str = "mp3"
    summary_length: str = "short"

class AudioPayload(BaseModel):
    input_path: str
    actions: List[str]     # ['convert', 'summary']
    target_format: str = "mp3"
    summary_length: str = "short"

class ExecutionResult(BaseModel):
    success: bool
    outputs: Any