#!/usr/bin/env python3
"""
transcribe.py
-------------
CLI utility to transcribe (or translate) audio/video files using OpenAI's Whisper model.

Usage:
    python transcribe.py path/to/audio.mp3

Additional options:
    -m / --model      : Whisper model size (tiny, base, small, medium, large, large-v2).
    -o / --output     : Path for the resulting text file. Defaults to <input>_transcribe.txt.
    --language        : Language code spoken in the audio (e.g., 'en', 'fr'). Leave empty to auto-detect.
    --task            : 'transcribe' (default) or 'translate' (into English).

The script prints a short preview of the transcript and writes the full text to the specified output file.

Dependencies are declared in requirements.txt. Ensure the FFMPEG binary is installed on your system because Whisper relies on it for audio decoding.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import whisper  # type: ignore
except ModuleNotFoundError as exc:
    sys.exit(
        "❌ 'whisper' library not found. Install dependencies first with:\n"
        "   pip install -r requirements.txt\n"
    )

import shutil  # placed after successful import check


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="transcribe",
        description="Transcribe or translate audio/video files using Whisper.",
    )
    parser.add_argument("input", help="Path to the audio/video file to process.")
    parser.add_argument(
        "-m",
        "--model",
        default="small",
        help="Whisper model size to load (tiny, base, small, medium, large, large-v2). Default: small.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Destination path for the transcription text. Defaults to <input>_<task>.txt.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Spoken language ISO code (e.g. 'en', 'de'). Leave empty for auto-detection.",
    )
    parser.add_argument(
        "--task",
        choices=["transcribe", "translate"],
        default="transcribe",
        help="Whether to transcribe (retain language) or translate to English.",
    )
    return parser.parse_args(argv)


def resolve_output_path(input_path: Path, provided: Optional[str], task: str) -> Path:
    """Determine where to save the transcription."""
    if provided:
        return Path(provided).expanduser().resolve()

    # Save alongside the input file, replacing its stem.
    return input_path.with_name(f"{input_path.stem}_{task}.txt")


def main(argv: Optional[list[str]] = None) -> None:
    if sys.version_info >= (3, 12):
        sys.exit(
            "❌ PyTorch/Whisper wheels are not yet available for Python 3.12. "
            "Please run this tool under Python 3.8—3.11 (e.g. 3.11.8). "
            "Consider using pyenv:\n"
            "   pyenv install 3.11.8 && pyenv local 3.11.8"
        )

    args = parse_args(argv)

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        sys.exit(f"❌ File not found: {input_path}")

    print(f"👉 Loading Whisper model '{args.model}'… This may take a while on first run.")
    model = whisper.load_model(args.model)

    print("🎧 Transcribing…")
    # The whisper library handles slicing/chunking internally for longer inputs.
    result = model.transcribe(
        str(input_path),
        task=args.task,
        language=args.language,
        fp16=False  # Use fp32 for compatibility on CPU-only machines.
    )

    text: str = result["text"].strip()

    output_path = resolve_output_path(input_path, args.output, args.task)
    output_path.write_text(text, encoding="utf-8")

    print(f"✅ Done! Transcript saved to: {output_path}")
    print("\n--- Transcript preview (first 1,000 chars) ---")
    preview = text[:1000] + ("…" if len(text) > 1000 else "")
    print(preview)

    # Basic environment sanity-check.
    if shutil.which("ffmpeg") is None:
        print("⚠️  FFmpeg executable not found in PATH. Whisper might fail to load the audio."
              "\n    👉 Install it, e.g. 'brew install ffmpeg' (macOS) or from https://ffmpeg.org/download.html",
              file=sys.stderr)


if __name__ == "__main__":
    main() 