# cli.py (프로젝트 최상단에 덮어쓰기)
import os
import typer
from core.runner import run_plugin

# 플러그인 등록(import) — register_plugin() 실행을 위해
import plugins.youtube
import plugins.video
import plugins.audio
import plugins.image
import plugins.text

app = typer.Typer(help="Universal File Converter CLI", add_completion=False, no_args_is_help=False)

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    url:     str            = typer.Option(None, "--url",            help="YouTube video URL"),
    actions: list[str]      = typer.Option(None, "--actions",        help="Select one or more: video, audio, summary"),
    video_quality: str      = typer.Option("720p", "--video-quality",  help="Video resolution"),
    audio_format:  str      = typer.Option("mp3",  "--audio-format",   help="Audio format"),
    summary_length:str      = typer.Option("short","--summary-length",help="Summary length: short or detailed"),
):
    """
    YouTube URL로부터 비디오 다운로드, 오디오 추출, 자동 요약 수행
    (서브커맨드 없이 호출될 때 실행됩니다)
    """
    # --- 서브커맨드(video/audio/image/text)가 지정된 경우, 여기서 빠져나갑니다 ---
    if ctx.invoked_subcommand:
        return

    if not url or not actions:
        typer.secho("❌ You must pass --url and at least one --actions", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    payload = {
        "url":            url,
        "actions":        actions,
        "video_quality":  video_quality,
        "audio_format":   audio_format,
        "summary_length": summary_length,
    }
    result = run_plugin("youtube", payload)
    if result.success:
        for name, path in result.outputs.items():
            typer.echo(f"{name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command("video")
def video(
    input_path: str = typer.Option(..., help="Path to local video file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: audio, summary"),
    audio_format: str = typer.Option("mp3", help="Audio format, e.g. mp3, wav"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
):
    """
    로컬 비디오 파일로부터 오디오 추출 및 자동 요약 수행
    """
    payload = {
        "input_path":     input_path,
        "actions":        actions,
        "audio_format":   audio_format,
        "summary_length": summary_length,
    }
    result = run_plugin("video", payload)
    if result.success:
        for name, path in result.outputs.items():
            typer.echo(f"{name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command("audio")
def audio(
    input_path: str = typer.Option(..., help="Path to local audio file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: convert, summary"),
    target_format: str = typer.Option("mp3", help="Target audio format, e.g. mp3, wav, flac"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
):
    """
    로컬 오디오 파일의 포맷 변환 및 자동 요약 수행
    """
    payload = {
        "input_path":     input_path,
        "actions":        actions,
        "target_format":  target_format,
        "summary_length": summary_length,
    }
    result = run_plugin("audio", payload)
    if result.success:
        for name, path in result.outputs.items():
            typer.echo(f"{name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command("image")
def image(
    input_path: str = typer.Option(..., help="Path to local image file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: ocr, to-pdf, to-docx, convert"),
    target_format: str = typer.Option("png", help="Target image format, e.g. png, jpeg, webp"),
):
    """
    로컬 이미지 파일의 OCR, 문서 변환, 포맷 변환 수행
    """
    payload = {
        "input_path":    input_path,
        "actions":       actions,
        "target_format": target_format,
    }
    result = run_plugin("image", payload)
    if result.success:
        for name, path in result.outputs.items():
            typer.echo(f"{name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command("text")
def text(
    input_path: str = typer.Option(..., help="Path to local text file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: summarize, tts, to-pdf, to-image"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
    tts_format: str = typer.Option("mp3", help="TTS audio format, e.g. mp3, wav"),
):
    """
    로컬 텍스트 파일로부터 요약, TTS, PDF/이미지 변환 수행
    """
    payload = {
        "input_path":     input_path,
        "actions":        actions,
        "summary_length": summary_length,
        "tts_format":     tts_format,
    }
    result = run_plugin("text", payload)
    if result.success:
        for name, path in result.outputs.items():
            typer.echo(f"{name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

def main():
    app()

if __name__ == "__main__":
    main()
