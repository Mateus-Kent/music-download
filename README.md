# music-download

Script em Python para baixar playlists e vídeos do YouTube em áudio (MP3, M4A, etc.) ou vídeo (MP4, MKV, etc.).

## Requisitos

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) — necessário para conversão de áudio

### Instalando o ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (via Chocolatey)
choco install ffmpeg
```

## Instalação

```bash
# Clone ou baixe o repositório
cd music-download

# Instale as dependências Python
pip install -r requirements.txt
```

## Uso

```bash
python3 download_playlist.py [URL] [opções]
```

### Exemplos

```bash
# Baixar playlist como MP3 (192 kbps)
python3 download_playlist.py "https://youtube.com/playlist?list=..." --audio

# Baixar playlist como vídeo MP4
python3 download_playlist.py "https://youtube.com/playlist?list=..."

# Definir pasta de destino e qualidade do áudio
python3 download_playlist.py "URL" --audio --output ~/Musicas --quality 320

# Baixar em formato M4A
python3 download_playlist.py "URL" --format m4a

# Baixar vídeo em MKV
python3 download_playlist.py "URL" --format mkv
```

## Opções

| Opção | Descrição | Padrão |
|---|---|---|
| `url` | URL da playlist ou vídeo | obrigatório |
| `-o`, `--output` | Pasta de destino dos arquivos | `./downloads` |
| `--audio` | Baixar somente o áudio | — |
| `--format` | Formato de saída (ver tabela abaixo) | `mp4` / `mp3` |
| `--quality` | Qualidade do áudio em kbps | `192` |

### Formatos suportados

| Tipo | Formatos |
|---|---|
| Áudio | `mp3`, `m4a`, `opus`, `wav`, `flac` |
| Vídeo | `mp4`, `mkv`, `webm` |

> Ao usar `--format` com um formato de áudio, o modo `--audio` é ativado automaticamente.

## Estrutura dos arquivos baixados

Os arquivos são salvos com o seguinte padrão de nome:

```
downloads/
├── 01 - Nome da música.mp3
├── 02 - Nome da música.mp3
└── ...
```

## Dependências

| Pacote | Descrição |
|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Motor de download do YouTube |
