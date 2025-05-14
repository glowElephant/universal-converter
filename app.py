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

    if st.button("Run Video") and video_file:
        payload = {
            "input_path": st.session_state.video_path,
            "actions": actions_v,
            "audio_format": audio_format_v,
            "summary_length": summary_length_v,
        }
        result = run_plugin("video", payload)
        if result.success:
            for name, path in result.outputs.items():
                if not path or not os.path.exists(path):
                    st.warning(f"No file generated for '{name}'.")
                    continue
                file_name = os.path.basename(path)
                with open(path, "rb") as f:
                    st.download_button(f"Download {name}", data=f, file_name=file_name)
        else:
            st.error(f"Error: {result.outputs}")

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

    if st.button("Run Audio") and audio_file:
        payload = {
            "input_path": st.session_state.audio_path,
            "actions": actions_a,
            "target_format": target_format_a,
            "summary_length": summary_length_a,
        }
        result = run_plugin("audio", payload)
        if result.success:
            for name, path in result.outputs.items():
                if not path or not os.path.exists(path):
                    st.warning(f"No file generated for '{name}'.")
                    continue
                file_name = os.path.basename(path)
                with open(path, "rb") as f:
                    st.download_button(f"Download {name}", data=f, file_name=file_name)
        else:
            st.error(f"Error: {result.outputs}")

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
        payload = {
            "input_path": st.session_state.image_path,
            "actions": actions_i,
            "target_format": target_format_i,
        }
        result = run_plugin("image", payload)
        if result.success:
            for name, path in result.outputs.items():
                if not path or not os.path.exists(path):
                    st.warning(f"No file generated for '{name}'.")
                    continue
                file_name = os.path.basename(path)
                with open(path, "rb") as f:
                    st.download_button(f"Download {name}", data=f, file_name=file_name)
        else:
            st.error(f"Error: {result.outputs}")

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
        payload = {
            "input_path": st.session_state.text_path,
            "actions": actions_t,
            "summary_length": summary_length_t,
            "tts_format": tts_format_t,
        }
        result = run_plugin("text", payload)
        if result.success:
            for name, path in result.outputs.items():
                if not path or not os.path.exists(path):
                    st.warning(f"No file generated for '{name}'.")
                    continue
                file_name = os.path.basename(path)
                with open(path, "rb") as f:
                    st.download_button(f"Download {name}", data=f, file_name=file_name)
        else:
            st.error(f"Error: {result.outputs}")
