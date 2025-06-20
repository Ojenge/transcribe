# TranscribeAI

A simple command-line utility to convert audio or video files into text using [OpenAI Whisper](https://github.com/openai/whisper).

---

## 1. Installation

1. **Clone / open** this repository.
2. Ensure **Python 3.8 – 3.11** is installed. (Whisper/PyTorch wheels are not yet released for Python 3.12.)
3. (macOS) Install FFmpeg via Homebrew if you don't have it:
   ```bash
   brew install ffmpeg
   ```
4. Create a virtual environment (recommended) with a supported Python version and install dependencies:
   ```bash
   # Example using pyenv – feel free to use any version manager
   brew install pyenv               # macOS
   pyenv install 3.11.8             # install a compatible Python
   pyenv local 3.11.8               # set it for this project

   python3 -m venv .venv            # create virtual-env
   source .venv/bin/activate
   pip install -r requirements.txt  # install deps
   ```

> **Note:** The first run will download the chosen Whisper model which can be several hundred megabytes. Subsequent runs will reuse the cached model.

---

## 2. Usage

```bash
python transcribe.py <audio_or_video_file> [options]
```

### Common options

| Flag | Description | Default |
|------|-------------|---------|
| `-m, --model` | Whisper model size to use (`tiny`, `base`, `small`, `medium`, `large`, `large-v2`) | `small` |
| `-o, --output` | Path for the resulting text file | `<input>_transcribe.txt` |
| `--language` | ISO-639 language code of the speech (leave blank for auto-detect) | autodetect |
| `--task` | `transcribe` or `translate` (translate into English) | `transcribe` |

### Examples

1. **Basic transcription**
   ```bash
   python transcribe.py "PCS Presentation.mp3"
   ```
2. **Use the medium model for higher accuracy**
   ```bash
   python transcribe.py meeting.wav -m medium
   ```
3. **Translate Spanish audio into English**
   ```bash
   python transcribe.py interview_es.mp4 --task translate --language es
   ```

---

## 3. Output
The script writes the full transcript to the specified text file and prints the first 1,000 characters to the console for a quick preview.

---

## 4. License
MIT 
