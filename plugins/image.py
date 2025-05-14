import os, glob
from core.runner import register_plugin
from core.schemas import ImagePayload, ExecutionResult
from PIL import Image
import pytesseract
import img2pdf
from docx import Document

@register_plugin("image")
def image_plugin(payload: dict) -> ExecutionResult:
    data = ImagePayload(**payload)
    outputs = {}
    if "ocr" in data.actions:
        outputs["text"] = perform_ocr(data.input_path)
    if "to-pdf" in data.actions:
        outputs["pdf"] = convert_to_pdf(data.input_path)
    if "to-docx" in data.actions:
        outputs["docx"] = convert_to_docx(data.input_path)
    if "convert" in data.actions:
        outputs["converted"] = convert_format(data.input_path, data.target_format)
    return ExecutionResult(success=True, outputs=outputs)

def perform_ocr(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img, lang="eng+kor")

def convert_to_pdf(path: str) -> str:
    out = os.path.splitext(path)[0] + ".pdf"
    with open(out, "wb") as f:
        f.write(img2pdf.convert(path))
    return os.path.abspath(out)

def convert_to_docx(path: str) -> str:
    text = perform_ocr(path)
    doc = Document()
    doc.add_paragraph(text)
    out = os.path.splitext(path)[0] + ".docx"
    doc.save(out)
    return os.path.abspath(out)

def convert_format(path: str, fmt: str) -> str:
    img = Image.open(path)
    out = os.path.splitext(path)[0] + f".{fmt}"
    img.save(out, fmt.upper())
    return os.path.abspath(out)
