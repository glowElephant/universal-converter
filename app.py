from dotenv import load_dotenv
import os
import streamlit as st
from core.runner import run_plugin
import plugins.youtube
import plugins.video
import plugins.audio
import plugins.image
import plugins.text
from openai import OpenAI

import logging

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)

# .env 로드 및 OpenAI 키 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit 페이지 설정
st.set_page_config(page_title="Universal File Converter", layout="wide")
st.title("Universal File Converter")

# YouTube 탭 결과를 세션에 저장할 공간 초기화
if "yt_outputs" not in st.session_state:
    st.session_state.yt_outputs = {}

tabs = st.tabs(["YouTube", "Video", "Audio", "Image", "Text"])

# --- YouTube 탭 ---
with tabs[0]:
    st.header("YouTube Converter")
    url = st.text_input("YouTube URL")
    actions = st.multiselect(
        "Actions", ["video", "audio", "summary"], default=["video", "audio", "summary"]
    )
    video_quality = st.selectbox("Video Quality", ["1080p", "720p", "480p"], index=1)
    audio_format = st.selectbox("Audio Format", ["mp3", "wav", "flac"], index=0)
    summary_length = st.selectbox("Summary Length", ["short", "detailed"], index=0)

    if st.button("Run YouTube"):
        payload = {
            "url": url,
            "actions": actions,
            "video_quality": video_quality,
            "audio_format": audio_format,
            "summary_length": summary_length,
        }
        result = run_plugin("youtube", payload)
        if result.success:
            st.session_state.yt_outputs = result.outputs
        else:
            st.error(f"Error: {result.outputs}")

    # YouTube 탭 결과 렌더링
    for name, path in st.session_state.yt_outputs.items():
        if name == "summary":
            st.subheader("Summary")
            st.text_area("", path, height=200)
        else:
            if not path or not os.path.exists(path):
                st.warning(f"No file generated for '{name}'.")
                continue
            file_name = os.path.basename(path)
            with open(path, "rb") as f:
                st.download_button(f"Download {name}", data=f, file_name=file_name, key=f"yt_{name}")

# --- Video 탭 ---
with tabs[1]:
    st.header("Video Converter")
    video_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
    if video_file:
        st.session_state.video_path = f"temp_video_{video_file.name}"
        with open(st.session_state.video_path, "wb") as out:
            out.write(video_file.getbuffer())

    actions_v = st.multiselect("Actions", ["audio", "summary"], default=["audio"])
    audio_format_v = st.selectbox("Audio Format", ["mp3", "wav"], key="afv")
    summary_length_v = st.selectbox("Summary Length", ["short", "detailed"], key="slv")

        # 1) 실행 결과를 세션에 저장하도록 변경
    if st.button("Run Video") and video_file:
        payload = {
            "input_path": st.session_state.video_path,
            "actions": actions_v,
            "audio_format": audio_format_v,
            "summary_length": summary_length_v,
        }
        result = run_plugin("video", payload)
        if result.success:
            st.session_state.video_outputs = result.outputs
        else:
            st.error(f"Error: {result.outputs}")

    # 2) 저장된 결과를 렌더링 (파일 vs 텍스트 구분)
    if "video_outputs" in st.session_state:
        outputs = st.session_state.video_outputs

        # Summary 텍스트
        if "summary" in outputs:
            st.subheader("Summary")
            st.text_area("", outputs["summary"], height=200)

        # Audio / 기타 파일
        if "audio" in outputs:
            audio_path = outputs["audio"]
            if os.path.exists(audio_path):
                with open(audio_path, "rb") as f:
                    st.download_button("Download audio", data=f, file_name=os.path.basename(audio_path))
            else:
                st.warning("No audio file generated.")

# --- Audio 탭 ---
with tabs[2]:
    st.header("Audio Converter")
    audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "flac"])
    if audio_file:
        st.session_state.audio_path = f"temp_audio_{audio_file.name}"
        with open(st.session_state.audio_path, "wb") as out:
            out.write(audio_file.getbuffer())

    actions_a = st.multiselect("Actions", ["convert", "summary"], default=["convert"])
    target_format_a = st.selectbox("Target Format", ["mp3", "wav", "flac"], key="tfa")
    summary_length_a = st.selectbox("Summary Length", ["short", "detailed"], key="sla")

        # 1) Run Audio 를 누르면 결과를 세션에 저장
    if st.button("Run Audio") and audio_file:
        payload = {
            "input_path": st.session_state.audio_path,
            "actions": actions_a,
            "target_format": target_format_a,
            "summary_length": summary_length_a,
        }
        result = run_plugin("audio", payload)
        if result.success:
            st.session_state.audio_outputs = result.outputs
        else:
            st.error(f"Error: {result.outputs}")

    # 2) 저장된 결과를 렌더링 (Summary → TextArea, 나머지 → Download Button)
    if "audio_outputs" in st.session_state:
        outputs = st.session_state.audio_outputs

        # Summary 텍스트
        if "summary" in outputs:
            st.subheader("Summary")
            st.text_area("", outputs["summary"], height=200)

        # 변환된 오디오 파일 등 다운로드 버튼
        for name, path in outputs.items():
            if name == "summary":
                continue

            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        f"Download {name}",
                        data=f,
                        file_name=os.path.basename(path),
                        key=f"dl_audio_{name}"
                    )
            else:
                st.warning(f"No file generated for '{name}'.")

# --- Image 탭 ---
with tabs[3]:
    st.header("Image Converter")
    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "webp"])
    if image_file:
        st.session_state.image_path = f"temp_image_{image_file.name}"
        with open(st.session_state.image_path, "wb") as out:
            out.write(image_file.getbuffer())

    actions_i = st.multiselect("Actions", ["ocr", "to-pdf", "to-docx", "convert"], default=["ocr"])
    target_format_i = st.selectbox("Target Format", ["png", "jpeg", "webp"], key="tfi")

    if st.button("Run Image") and image_file:
        # 1) 실행 후 결과를 세션에 저장
        payload = {
            "input_path": st.session_state.image_path,
            "actions": actions_i,
            "target_format": target_format_i,
        }
        result = run_plugin("image", payload)
        if result.success:
            st.session_state.image_outputs = result.outputs
        else:
            st.error(f"Error: {result.outputs}")

        # 2) 저장된 결과 렌더링
    if "image_outputs" in st.session_state:
        outputs = st.session_state.image_outputs

        # 2-1) OCR 결과(text) 출력 (plugin이 "text" 키를 쓰는 경우)
        if "text" in outputs:
            st.subheader("OCR Result")
            st.text_area("", outputs["text"], height=200)
        # 만약 plugin이 outputs["ocr"] 키를 쓴다면, 아래 주석을 해제하세요.
        # elif "ocr" in outputs:
        #     st.subheader("OCR Result")
        #     st.text_area("", outputs["ocr"], height=200)

        # 2-2) 나머지 파일들 다운로드 버튼
        for name, path in outputs.items():
            if name in ("text", "ocr"):
                # 이미 텍스트로 처리했으니 건너뜁니다
                continue

            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        f"Download {name}",
                        data=f,
                        file_name=os.path.basename(path),
                        key=f"dl_image_{name}"
                    )
            else:
                st.warning(f"No file generated for '{name}'.")

# --- Text 탭 ---
with tabs[4]:
    st.header("Text Converter")
    text_file = st.file_uploader("Upload Text File", type=["txt", "md"])
    if text_file:
        st.session_state.text_path = f"temp_text_{text_file.name}"
        with open(st.session_state.text_path, "wb") as out:
            out.write(text_file.getbuffer())

    actions_t = st.multiselect(
        "Actions", ["summarize", "tts", "to-pdf", "to-image"], default=["summarize"]
    )
    summary_length_t = st.selectbox("Summary Length", ["short", "detailed"], key="slt")
    tts_format_t = st.selectbox("TTS Format", ["mp3", "wav"], key="tft")

    if st.button("Run Text") and text_file:
        # 1) 실행 후 결과를 세션에 저장
        payload = {
            "input_path": st.session_state.text_path,
            "actions": actions_t,
            "summary_length": summary_length_t,
            "tts_format": tts_format_t,
        }
        result = run_plugin("text", payload)
        if result.success:
            st.session_state.text_outputs = result.outputs
        else:
            st.error(f"Error: {result.outputs}")

        # 2) 저장된 결과 렌더링
    if "text_outputs" in st.session_state:
        outputs = st.session_state.text_outputs

        # summary 키로 바뀌었으니 여기서 잡아줍니다
        if "summary" in outputs:
            st.subheader("Summary")
            st.text_area("", outputs["summary"], height=200)

        # 나머지(‘audio’, ‘pdf’, ‘image’) 파일 다운로드
        for name, path in outputs.items():
            if name == "summary":
                continue
            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        f"Download {name}",
                        data=f,
                        file_name=os.path.basename(path),
                        key=f"dl_text_{name}"
                    )
            else:
                st.warning(f"No file generated for '{name}'.")
