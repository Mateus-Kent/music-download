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


def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "?%").strip()
        speed = d.get("_speed_str", "?").strip()
        eta = d.get("_eta_str", "?").strip()
        filename = os.path.basename(d.get("filename", ""))
        print(f"\r  [{percent}] {filename} — velocidade: {speed} — ETA: {eta}", end="", flush=True)
    elif d["status"] == "finished":
        print()


def build_options(output_dir: str, audio_only: bool, quality: str, format_ext: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    outtmpl = os.path.join(output_dir, "%(playlist_index)s - %(title)s.%(ext)s")

    if audio_only:
        return {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "progress_hooks": [progress_hook],
            "ignoreerrors": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format_ext,
                    "preferredquality": quality,
                }
            ],
        }

    return {
        "format": f"bestvideo[ext={format_ext}]+bestaudio/best[ext={format_ext}]/best",
        "outtmpl": outtmpl,
        "progress_hooks": [progress_hook],
        "ignoreerrors": True,
        "merge_output_format": format_ext,
    }


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

    audio_only = args.audio

    if args.fmt:
        fmt = args.fmt.lower()
    else:
        fmt = "mp3" if audio_only else "mp4"

    audio_formats = {"mp3", "m4a", "opus", "wav", "flac"}
    video_formats = {"mp4", "mkv", "webm"}

    if fmt in audio_formats:
        audio_only = True
    elif fmt in video_formats:
        audio_only = False
    else:
        print(f"Formato inválido: {fmt}")
        print(f"  Áudio : {', '.join(audio_formats)}")
        print(f"  Vídeo : {', '.join(video_formats)}")
        sys.exit(1)

    options = build_options(args.output, audio_only, args.quality, fmt)
    download(args.url, options)


if __name__ == "__main__":
    main()
