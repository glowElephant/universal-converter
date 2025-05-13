import typer
from core.runner import run_plugin

app = typer.Typer(help="Universal File Converter CLI")

@app.command()
def youtube(
    url: str = typer.Option(..., help="YouTube video URL"),
    actions: list[str] = typer.Option(..., "--actions", help="Select one or more: video, audio, summary"),
    video_quality: str = typer.Option("720p", help="Video resolution, e.g. 1080p, 720p"),
    audio_format: str = typer.Option("mp3", help="Audio format, e.g. mp3, wav, flac"),
    summary_length: str = typer.Option("short", help="Summary length: short or detailed"),
):
    """YouTube URL로부터 비디오 다운로드, 오디오 추출, 자동 요약을 수행"""
    payload = {
        "url": url,
        "actions": actions,
        "video_quality": video_quality,
        "audio_format": audio_format,
        "summary_length": summary_length,
    }
    result = run_plugin("youtube", payload)
    if result.success:
        typer.echo("✅ YouTube 작업 완료:")
        for name, path in result.outputs.items():
            typer.echo(f"  - {name}: {path}")
    else:
        typer.secho(f"❌ 오류 발생: {result.outputs}", fg=typer.colors.RED)

# 추가 탭(플러그인) 스켈레톤 예시
# @app.command()
# def video(...):
#     """Video 파일로부터 음성 추출 및 요약"""
#     ...

# @app.command()
# def audio(...):
#     """Audio 파일 포맷 변환 및 요약"""
#     ...

# @app.command()
# def image(...):
#     """Image 파일 OCR 및 문서 변환"""
#     ...

# @app.command()
# def text(...):
#     """Text 파일 요약, TTS, PDF/이미지 변환"""
#     ...


def main():
    app()


if __name__ == "__main__":
    main()
