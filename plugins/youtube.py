from core.runner import register_plugin
from core.schemas import YouTubePayload, ExecutionResult
from yt_dlp import YoutubeDL
import os
import glob
import openai  # import globally for testing

@register_plugin("youtube")
def youtube_plugin(payload: dict) -> ExecutionResult:
    """YouTube URL로부터 비디오/오디오/요약 기능을 실행하는 플러그인"""
    data = YouTubePayload(**payload)
    outputs: dict[str, str] = {}

    # 1) 비디오 다운로드
    if "video" in data.actions:
        outputs["video"] = download_video(data.url, data.video_quality)

    # 2) 오디오 추출
    if "audio" in data.actions:
        outputs["audio"] = extract_audio(data.url, data.audio_format)

    # 3) 자동 요약
    if "summary" in data.actions:
        transcript = get_transcript(data.url)
        outputs["summary"] = summarize_text(transcript, data.summary_length)

    return ExecutionResult(success=True, outputs=outputs)


def download_video(url: str, quality: str) -> str:
    """
    yt-dlp를 사용하여 지정 해상도의 비디오(MP4) 파일을 다운로드하고 반환합니다.
    """
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    filename = f"{info['id']}.mp4"
    return os.path.abspath(filename)


def extract_audio(url: str, fmt: str) -> str:
    """
    yt-dlp를 사용하여 지정 포맷의 오디오 파일을 추출하고 반환합니다.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': fmt,
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    filename = f"{info['id']}.{fmt}"
    return os.path.abspath(filename)


def get_transcript(url: str) -> str:
    """
    YouTube 자막(.vtt) 추출 및 Whisper fallback 처리를 통해 전체 대본 텍스트 반환
    """
    # 자막 시도
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'vtt',
        'skip_download': True,
        'outtmpl': '%(id)s',
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    video_id = info['id']
    vtt_files = glob.glob(f"{video_id}*.vtt")
    transcript = []
    if vtt_files:
        for vtt in vtt_files:
            with open(vtt, 'r', encoding='utf-8') as f:
                for line in f:
                    if '-->' in line or line.strip().isdigit() or line.startswith('WEBVTT') or not line.strip():
                        continue
                    transcript.append(line.strip())
            try:
                os.remove(vtt)
            except OSError:
                pass
        return ' '.join(transcript)
    # VTT 없으면 Whisper fallback
    from whisper import load_model  # lazy import to avoid global import issues
    audio_path = extract_audio(url, 'wav')
    model = load_model("base")
    result = model.transcribe(audio_path)
    try:
        os.remove(audio_path)
    except OSError:
        pass
    return result.get('text', '')


def summarize_text(text: str, length: str) -> str:
    """
    OpenAI GPT-4 API를 호출하여 짧게/자세하게 요약한 텍스트를 반환합니다.
    """
    prompt = (
        f"다음 내용을 {'짧게' if length == 'short' else '자세하게'} 요약해줘:\n\n{text}"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
