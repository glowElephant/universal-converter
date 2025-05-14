import os
import io
from core.runner import register_plugin
from core.schemas import TextPayload, ExecutionResult
from openai import OpenAI
from gtts import gTTS
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@register_plugin("text")
def text_plugin(payload: dict) -> ExecutionResult:
    data = TextPayload(**payload)
    outputs = {}
    # Summarize text
    if "summarize" in data.actions:
        outputs["summary"] = summarize_text_from_file(data.input_path, data.summary_length)
    # Text-to-speech
    if "tts" in data.actions:
        outputs["audio"] = text_to_speech_from_file(data.input_path, data.tts_format)
    # Convert to PDF
    if "to-pdf" in data.actions:
        outputs["pdf"] = text_to_pdf(data.input_path)
    # Convert to Image
    if "to-image" in data.actions:
        outputs["image"] = text_to_image(data.input_path)
    return ExecutionResult(success=True, outputs=outputs)


def summarize_text_from_file(path: str, length: str) -> str:
    # Read file with UTF-8 encoding
    with open(path, encoding="utf-8") as f:
        raw_text = f.read()
    # Create prompt
    prompt = (
        "아래 내용을 요약해 주세요.\n"
        f"길이: {'짧게' if length=='short' else '상세하게'}\n\n"
        f"{raw_text}"
    )
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
    )
    return resp.choices[0].message.content.strip()


def text_to_speech_from_file(path: str, fmt: str) -> str:
    # Read text
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Generate TTS (Ko-kr assumed)
    tts = gTTS(text=text, lang="ko")
    out = os.path.splitext(path)[0] + f".{fmt}"
    tts.save(out)
    return os.path.abspath(out)


def text_to_pdf(path: str) -> str:
    # Initialize PDF with Unicode font (Arial)
    pdf = FPDF()
    pdf.add_page()
    # 한글 깨짐 방지를 위해 Malgun Gothic 사용
    font_path = r"C:\Windows\Fonts\malgun.ttf"
    pdf.add_font("MalgunGothic", "", font_path, uni=True)
    pdf.set_font("MalgunGothic", size=12)
    # Write lines
    with open(path, encoding="utf-8") as f:
        for line in f:
            pdf.multi_cell(0, 10, line.strip(), align='L')
    out = os.path.splitext(path)[0] + ".pdf"
    pdf.output(out)
    return os.path.abspath(out)


def text_to_image(path: str) -> str:
    # Read text
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # 한글 지원되는 Malgun Gothic 폰트로 경로 변경
    font_path = r"C:\Windows\Fonts\malgun.ttf"
    font = ImageFont.truetype(font_path, size=16)
    # Split lines
    lines = text.splitlines() or ['']
    # Create dummy image for text size calculations
    dummy_img = Image.new('RGB', (1, 1), color='white')
    draw_dummy = ImageDraw.Draw(dummy_img)
    # Calculate max width and line height using textbbox
    max_width = 0
    line_height = 0
    for line in lines:
        bbox = draw_dummy.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        max_width = max(max_width, width)
        line_height = max(line_height, height)
    padding = 10
    img_width = max_width + padding * 2
    img_height = line_height * len(lines) + padding * 2
    # Create final image
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)
    y = padding
    for line in lines:
        draw.text((padding, y), line, font=font, fill='black')
        y += line_height
    out = os.path.splitext(path)[0] + ".png"
    img.save(out)
    return os.path.abspath(out)
