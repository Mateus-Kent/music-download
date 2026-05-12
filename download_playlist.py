#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Baixa playlists do YouTube em formato de áudio (MP3) ou vídeo (MP4).
"""

import argparse
import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Erro: yt-dlp não está instalado.")
    print("Execute: pip install yt-dlp")
    sys.exit(1)

AUDIO_FORMATS = {"mp3", "m4a", "opus", "wav", "flac"}
VIDEO_FORMATS = {"mp4", "mkv", "webm"}


def progress_hook(d):
    if d["status"] == "finished":
        print()
        return

    if d["status"] != "downloading":
        return

    percent = d.get("_percent_str", "?%").strip()
    speed = d.get("_speed_str", "?").strip()
    eta = d.get("_eta_str", "?").strip()
    filename = os.path.basename(d.get("filename", ""))
    print(f"\r  [{percent}] {filename} — velocidade: {speed} — ETA: {eta}", end="", flush=True)


def build_audio_options(outtmpl: str, quality: str, fmt: str) -> dict:
    return {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "progress_hooks": [progress_hook],
        "ignoreerrors": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": fmt,
                "preferredquality": quality,
            }
        ],
    }


def build_video_options(outtmpl: str, fmt: str) -> dict:
    return {
        "format": f"bestvideo[ext={fmt}]+bestaudio/best[ext={fmt}]/best",
        "outtmpl": outtmpl,
        "progress_hooks": [progress_hook],
        "ignoreerrors": True,
        "merge_output_format": fmt,
    }


def build_options(output_dir: str, audio_only: bool, quality: str, fmt: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    outtmpl = os.path.join(output_dir, "%(playlist_index)s - %(title)s.%(ext)s")

    if audio_only:
        return build_audio_options(outtmpl, quality, fmt)
    return build_video_options(outtmpl, fmt)


def resolve_format(fmt: str, audio_only: bool) -> tuple[str, bool]:
    if fmt in AUDIO_FORMATS:
        return fmt, True
    if fmt in VIDEO_FORMATS:
        return fmt, False

    print(f"Formato inválido: {fmt}")
    print(f"  Áudio : {', '.join(AUDIO_FORMATS)}")
    print(f"  Vídeo : {', '.join(VIDEO_FORMATS)}")
    sys.exit(1)


def download(url: str, options: dict):
    print(f"\nIniciando download: {url}\n")
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info:
            print("Erro: não foi possível obter informações da URL.")
            sys.exit(1)

        title = info.get("title") or info.get("id", "desconhecido")
        count = len(info.get("entries", [info])) if "entries" in info else 1
        print(f"Playlist/vídeo : {title}")
        print(f"Total de itens : {count}\n")

        ydl.download([url])

    print("\nDownload concluído!")


def main():
    parser = argparse.ArgumentParser(
        description="Baixa playlists (ou vídeos) do YouTube.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("url", help="URL da playlist ou vídeo do YouTube")
    parser.add_argument(
        "-o", "--output",
        default="downloads",
        help="Pasta de destino (padrão: ./downloads)",
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Baixar somente o áudio (MP3)",
    )
    parser.add_argument(
        "--format",
        default=None,
        dest="fmt",
        help=(
            "Formato de saída.\n"
            "  Áudio : mp3, m4a, opus, wav  (padrão: mp3)\n"
            "  Vídeo : mp4, mkv, webm       (padrão: mp4)"
        ),
    )
    parser.add_argument(
        "--quality",
        default="192",
        help="Qualidade do áudio em kbps (padrão: 192, ex: 128, 256, 320)",
    )

    args = parser.parse_args()

    default_fmt = "mp3" if args.audio else "mp4"
    fmt = (args.fmt or default_fmt).lower()
    fmt, audio_only = resolve_format(fmt, args.audio)

    options = build_options(args.output, audio_only, args.quality, fmt)
    download(args.url, options)


if __name__ == "__main__":
    main()
