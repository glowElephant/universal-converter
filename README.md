# Universal File Converter

다양한 파일(YouTube 영상, 로컬 비디오/오디오/이미지/텍스트)을 변환·처리·요약하는 툴입니다.

---

## 🚀 주요 기능

* **YouTube**

  * 영상 다운로드
  * 오디오 추출
  * 자막(transcript) 생성 및 GPT 기반 요약

* **Video**

  * 로컬 비디오 → 오디오 추출
  * Whisper 기반 전사(transcription)
  * GPT 기반 요약

* **Audio**

  * 포맷 변환 (mp3, wav, flac)
  * Whisper 전사
  * GPT 요약

* **Image**

  * OCR (한국어·영어 지원)
  * PDF / DOCX 변환
  * 이미지 포맷 변환 (png, jpeg, webp)

* **Text**

  * GPT 요약
  * TTS (gTTS)
  * PDF 변환 (FPDF + Malgun Gothic)
  * 이미지 변환 (Pillow + TrueType)

* **실행 환경**

  * CLI (Typer)
  * Web UI (Streamlit)

---

## 📋 사전 준비

1. **Python 3.8+**
2. **FFmpeg** (비디오/오디오 처리)
3. **Tesseract-OCR** (이미지 OCR)
4. **OpenAI API Key**

---

## 🛠️ 설치 가이드

### 1. 저장소 클론 & 가상환경 설정

```bash
git clone https://github.com/your-org/universal-converter.git
cd universal-converter

# 가상환경 생성
python3 -m venv .venv

# Windows CMD
.\.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate
```

### 2. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들고, 아래 내용을 입력하세요:

```ini
OPENAI_API_KEY=sk-...
```

---

## ⚙️ 시스템 의존성

### FFmpeg

* **macOS (Homebrew)**

  ```bash
  brew install ffmpeg
  ```
* **Ubuntu / Debian**

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
* **Windows**

  1. [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) 에서 static build 다운로드
  2. 압축 해제 후 `bin/` 폴더 경로를 시스템 PATH에 추가
  3. 설치 확인:

     ```bash
     ffmpeg -version
     ```

### Tesseract-OCR

* **macOS (Homebrew)**

  ```bash
  brew install tesseract
  ```
* **Ubuntu / Debian**

  ```bash
  sudo apt update
  sudo apt install tesseract-ocr
  ```
* **Windows (Chocolatey 예시)**

  ```powershell
  choco install tesseract -y
  refreshenv
  tesseract --version
  ```
* **한국어 지원 추가**

  1. [https://github.com/tesseract-ocr/tessdata](https://github.com/tesseract-ocr/tessdata) 에서 `kor.traineddata` 다운로드
  2. `C:\Program Files\Tesseract-OCR\tessdata\` 폴더에 복사

---

## 💻 사용법

### 1. CLI (Typer)

```bash
python cli.py [명령어] [옵션]
```

#### YouTube 예제

```bash
python cli.py youtube \
  --url https://youtu.be/VIDEO_ID \
  --actions video --actions audio --actions summary \
  --video_quality 720p \
  --audio_format mp3 \
  --summary_length short
```

#### Video 예제

```bash
python cli.py video \
  --input-path ./examples/sample.mp4 \
  --actions audio --actions summary \
  --audio_format wav \
  --summary_length detailed
```

#### Audio 예제

```bash
python cli.py audio \
  --input-path ./examples/sample.mp3 \
  --actions convert --actions summary \
  --target_format wav \
  --summary_length short
```

#### Image 예제

```bash
python cli.py image \
  --input-path ./examples/invoice.jpg \
  --actions ocr --actions to-pdf --actions to-docx --actions convert \
  --target_format png
```

#### Text 예제

```bash
python cli.py text \
  --input-path ./examples/notes.txt \
  --actions summarize --actions tts --actions to-pdf --actions to-image \
  --summary_length detailed \
  --tts_format mp3
```

### 2. Web UI (Streamlit)

```bash
streamlit run app.py --server.maxUploadSize=1024
```

1. 브라우저에서 `http://localhost:8501` 접속
2. **YouTube | Video | Audio | Image | Text** 탭 선택
3. URL 입력 또는 파일 업로드 → 실행 → 결과 확인 및 다운로드

---

## ✅ 테스트

```bash
pytest
```

38개의 유닛·통합 테스트가 모두 통과해야 합니다.

---