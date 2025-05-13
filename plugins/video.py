from core.runner import register_plugin
from core.schemas import VideoPayload, ExecutionResult
from plugins.youtube import extract_audio, get_transcript, summarize_text

@register_plugin("video")
def video_plugin(payload: dict) -> ExecutionResult:
    """로컬 비디오 파일로부터 오디오 추출 및 자동 요약을 수행하는 플러그인"""
    data = VideoPayload(**payload)
    outputs: dict[str, str] = {}

    # 1) 오디오 추출
    if "audio" in data.actions:
        outputs["audio"] = extract_audio(data.input_path, data.audio_format)

    # 2) 자동 요약
    if "summary" in data.actions:
        # 로컬 파일용 트랜스크립트
        transcript = get_transcript(data.input_path)
        outputs["summary"] = summarize_text(transcript, data.summary_length)

    return ExecutionResult(success=True, outputs=outputs)

# 로컬 비디오 파일 전사: Whisper 사용 (fallback 없이)
def get_transcript(file_path: str) -> str:
    from whisper import load_model
    model = load_model("base")
    result = model.transcribe(file_path)
    return result.get("text", "")
