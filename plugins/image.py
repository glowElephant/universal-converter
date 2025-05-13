from core.runner import register_plugin
from core.schemas import ImagePayload, ExecutionResult
import os

@register_plugin("image")
def image_plugin(payload: dict) -> ExecutionResult:
    """이미지 파일로부터 OCR, 문서 변환, 포맷 변환 기능을 수행하는 플러그인"""
    data = ImagePayload(**payload)
    outputs: dict[str, str] = {}

    # 1) OCR 텍스트 추출
    if "ocr" in data.actions:
        outputs["text"] = perform_ocr(data.input_path)

    # 2) PDF 변환
    if "to-pdf" in data.actions:
        outputs["pdf"] = convert_to_pdf(data.input_path)

    # 3) Word 변환
    if "to-docx" in data.actions:
        outputs["docx"] = convert_to_docx(data.input_path)

    # 4) 포맷 변환
    if "convert" in data.actions and data.target_format:
        outputs["converted"] = convert_format(data.input_path, data.target_format)

    return ExecutionResult(success=True, outputs=outputs)

# --- 헬퍼 함수 스텁 ---

def perform_ocr(path: str) -> str:
    # TODO: Tesseract OCR 로직
    raise NotImplementedError

def convert_to_pdf(path: str) -> str:
    # TODO: Pillow / pdf2image / reportlab 로 PDF로 변환
    raise NotImplementedError

def convert_to_docx(path: str) -> str:
    # TODO: python-docx 로 이미지 삽입 후 docx 생성
    raise NotImplementedError

def convert_format(path: str, fmt: str) -> str:
    # TODO: 이미지 포맷 변환 (Pillow)
    raise NotImplementedError
