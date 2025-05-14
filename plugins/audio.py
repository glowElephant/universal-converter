import os, torch
from core.runner import register_plugin
from core.schemas import AudioPayload, ExecutionResult
from whisper import load_model
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@register_plugin("audio")
def audio_plugin(payload: dict) -> ExecutionResult:
    data = AudioPayload(**payload)
    outputs = {}
    if "convert" in data.actions:
        outputs["converted"] = convert_format(data.input_path, data.target_format)
    if "summary" in data.actions:
        transcript = transcribe_audio(data.input_path)
        outputs["summary"] = summarize_text(transcript, data.summary_length)
    return ExecutionResult(success=True, outputs=outputs)

def convert_format(path: str, fmt: str) -> str:
    base, _ = os.path.splitext(path)
    out = f"{base}.{fmt}"
    os.system(f'ffmpeg -i "{path}" "{out}"')
    return os.path.abspath(out)

def transcribe_audio(path: str) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model("base", device=device)
    result = model.transcribe(path, fp16=(device=="cuda"))
    return result.get("text", "")

def summarize_text(text: str, length: str) -> str:
    if not text:
        return "No transcript available."
    prompt = (
        "아래 오디오 전사 내용을 요약해 주세요.\n"
        f"길이: {'짧게' if length=='short' else '상세하게'}\n\n"
        f"{text}"
    )
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
    )
    return resp.choices[0].message.content.strip()
