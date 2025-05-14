import os, torch
from core.runner import register_plugin
from core.schemas import VideoPayload, ExecutionResult
from moviepy.editor import VideoFileClip
from openai import OpenAI
from whisper import load_model
from dotenv import load_dotenv

load_dotenv()  

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@register_plugin("video")
def video_plugin(payload: dict) -> ExecutionResult:
    data = VideoPayload(**payload)
    outputs = {}
    if "audio" in data.actions:
        outputs["audio"] = extract_audio(data.input_path, data.audio_format)
    if "summary" in data.actions:
        transcript = get_transcript(data.input_path)
        outputs["summary"] = summarize_text(transcript, data.summary_length)
    return ExecutionResult(success=True, outputs=outputs)

def extract_audio(path: str, fmt: str) -> str:
    clip = VideoFileClip(path)
    out = os.path.splitext(path)[0] + f".{fmt}"
    clip.audio.write_audiofile(out)
    return os.path.abspath(out)

def get_transcript(path: str) -> str:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = load_model("base", device=device)
    result = model.transcribe(path, fp16=(device=='cuda'))
    return result.get("text", "")

def summarize_text(text: str, length: str) -> str:
    if not text:
        return "No transcript available."
    prompt = (
        "아래 비디오 대본을 요약해 주세요.\n"
        f"길이: {'짧게' if length=='short' else '상세하게'}\n\n"
        f"{text}"
    )
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()
