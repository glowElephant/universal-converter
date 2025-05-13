from core.runner import register_plugin
from core.schemas import AudioPayload, ExecutionResult
import os

@register_plugin("audio")
def audio_plugin(payload: dict) -> ExecutionResult:
    """로컬 오디오 파일을 변환 및 요약하는 플러그인"""
    data = AudioPayload(**payload)
    outputs: dict[str, str] = {}

    # 1) 포맷 변환
    if "convert" in data.actions:
        outputs["converted"] = convert_format(data.input_path, data.target_format)

    # 2) 자동 요약
    if "summary" in data.actions:
        # 오디오 → 텍스트 변환 (Whisper) → 요약
        transcript = transcribe_audio(data.input_path)
        outputs["summary"] = summarize_text(transcript, data.summary_length)

    return ExecutionResult(success=True, outputs=outputs)


def convert_format(file_path: str, fmt: str) -> str:
    """
    FFmpeg를 사용해 오디오 파일을 지정 포맷으로 변환하고, 경로를 반환합니다.
    """
    base, _ = os.path.splitext(file_path)
    output = f"{base}.{fmt}"
    # TODO: ffmpeg-python 로 변환 구현
    # e.g.
    # import ffmpeg
    # ffmpeg.input(file_path).output(output, **kwargs).run()
    raise NotImplementedError


def transcribe_audio(file_path: str) -> str:
    """
    Whisper를 사용해 오디오를 텍스트로 전사합니다.
    """
    # TODO: whisper.load_model -> transcribe
    raise NotImplementedError


def summarize_text(text: str, length: str) -> str:
    """
    OpenAI GPT-4 API를 호출해 텍스트를 요약합니다.
    """
    # TODO: OpenAI ChatCompletion 호출
    raise NotImplementedError
