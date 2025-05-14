import os
from core.runner import register_plugin
from core.schemas import TextPayload, ExecutionResult
from openai import OpenAI
from fpdf import FPDF
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()  
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@register_plugin("text")
def text_plugin(payload: dict) -> ExecutionResult:
    data = TextPayload(**payload)
    outputs = {}
    if "summarize" in data.actions:
        outputs["summary"] = summarize_text_from_file(data.input_path, data.summary_length)
    if "tts" in data.actions:
        outputs["audio"] = text_to_speech(data.input_path, data.tts_format)
    if "to-pdf" in data.actions:
        outputs["pdf"] = text_to_pdf(data.input_path)
    if "to-image" in data.actions:
        outputs["image"] = text_to_image(data.input_path)
    return ExecutionResult(success=True, outputs=outputs)

def summarize_text_from_file(path: str, length: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text:
        return "No transcript available."
    prompt = (
        "아래 텍스트를 요약해 주세요.\n"
        f"길이: {'짧게' if length=='short' else '상세하게'}\n\n"
        f"{text}"
    )
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()

def text_to_speech(path: str, fmt: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    tts = gTTS(text, lang="ko")
    out = os.path.splitext(path)[0] + f".{fmt}"
    tts.save(out)
    return os.path.abspath(out)

def text_to_pdf(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for ln in lines:
        pdf.cell(0, 10, ln.strip(), ln=True)
    out = os.path.splitext(path)[0] + ".pdf"
    pdf.output(out)
    return os.path.abspath(out)

def text_to_image(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    font = ImageFont.load_default()
    width = max(font.getsize(l)[0] for l in lines) + 20
    height = sum(font.getsize(l)[1]+5 for l in lines) + 20
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    y = 10
    for l in lines:
        draw.text((10, y), l, font=font, fill="black")
        y += font.getsize(l)[1] + 5
    out = os.path.splitext(path)[0] + ".png"
    img.save(out)
    return os.path.abspath(out)
