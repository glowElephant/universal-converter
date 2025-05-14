from pydantic import BaseModel
from typing import List, Any, Optional

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

class ImagePayload(BaseModel):
    input_path: str
    actions: List[str]     # ['ocr', 'to-pdf', 'to-docx', 'convert']
    target_format: Optional[str] = None  # For format conversion

class TextPayload(BaseModel):
    input_path: str
    actions: List[str]     # ['summarize', 'tts', 'to-pdf', 'to-image']
    summary_length: Optional[str] = "short"
    tts_format: Optional[str] = "mp3"

class ExecutionResult(BaseModel):
    success: bool
    outputs: Any
