import typer
from core.runner import run_plugin
from typing import Optional

app = typer.Typer(help="Universal File Converter CLI")

@app.command()
def youtube(
    url: str = typer.Option(..., help="YouTube video URL"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: video, audio, summary"),
    video_quality: str = typer.Option("720p", help="Video resolution"),
    audio_format: str = typer.Option("mp3", help="Audio format"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
):
    """YouTube URL로부터 비디오 다운로드, 오디오 추출, 자동 요약 수행"""
    payload = {
        "url": url,
        "actions": actions,
        "video_quality": video_quality,
        "audio_format": audio_format,
        "summary_length": summary_length,
    }
    result = run_plugin("youtube", payload)
    if result.success:
        typer.echo("✅ YouTube processing complete:")
        for name, path in result.outputs.items():
            typer.echo(f"  - {name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command()
def video(
    input_path: str = typer.Option(..., help="Path to local video file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: audio, summary"),
    audio_format: str = typer.Option("mp3", help="Audio format, e.g. mp3, wav"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
):
    """로컬 비디오 파일로부터 오디오 추출 및 자동 요약 수행"""
    payload = {
        "input_path": input_path,
        "actions": actions,
        "audio_format": audio_format,
        "summary_length": summary_length,
    }
    result = run_plugin("video", payload)
    if result.success:
        typer.echo("✅ Video processing complete:")
        for name, path in result.outputs.items():
            typer.echo(f"  - {name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command()
def audio(
    input_path: str = typer.Option(..., help="Path to local audio file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: convert, summary"),
    target_format: str = typer.Option("mp3", help="Target audio format, e.g. mp3, wav, flac"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
):
    """로컬 오디오 파일의 포맷 변환 및 자동 요약 수행"""
    payload = {
        "input_path": input_path,
        "actions": actions,
        "target_format": target_format,
        "summary_length": summary_length,
    }
    result = run_plugin("audio", payload)
    if result.success:
        typer.echo("✅ Audio processing complete:")
        for name, path in result.outputs.items():
            typer.echo(f"  - {name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)

@app.command()
def image(
    input_path: str = typer.Option(..., help="Path to local image file"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: ocr, to-pdf, to-docx, convert"),
    target_format: Optional[str] = typer.Option(None, help="Target image format for conversion, e.g. png, jpeg, webp"),
):
    """로컬 이미지 파일의 OCR, 문서 변환, 포맷 변환 수행"""
    payload = {
        "input_path": input_path,
        "actions": actions,
        "target_format": target_format,
    }
    result = run_plugin("image", payload)
    if result.success:
        typer.echo("✅ Image processing complete:")
        for name, path in result.outputs.items():
            typer.echo(f"  - {name}: {path}")
    else:
        typer.secho(f"❌ Error: {result.outputs}", fg=typer.colors.RED)


def main():
    app()

if __name__ == "__main__":
    main()
