from pydantic import BaseModel
from typing import Any, List

class YouTubePayload(BaseModel):
    url: str
    actions: List[str]
    video_quality: str
    audio_format: str
    summary_length: str

class ExecutionResult(BaseModel):
    success: bool
    outputs: Any
