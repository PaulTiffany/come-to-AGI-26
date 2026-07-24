"""Render the BGI Bellman film narration with pinned local Piper voices."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from datetime import datetime, timezone
import wave
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as stream:
        return stream.getnframes() / stream.getframerate()


def timestamp(seconds: float, separator: str) -> str:
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{milliseconds:03d}"


def render_segment(
    python: Path,
    model_dir: Path,
    voice: dict[str, Any],
    text: str,
    output: Path,
) -> None:
    model = model_dir / str(voice["model"])
    config = model.with_suffix(model.suffix + ".json")
    if not model.is_file() or not config.is_file():
        raise FileNotFoundError(f"missing local Piper model or config: {model.name}")
    actual = sha256(model)
    if actual != voice["sha256"]:
        raise RuntimeError(f"model hash mismatch for {model.name}: {actual}")
    subprocess.run(
        [
            str(python), "-m", "piper", "-m", str(model), "-c", str(config),
            "-f", str(output), "--length-scale", str(voice["length_scale"]),
            "--sentence-silence", "0.12",
        ],
        input=text,
        text=True,
        check=True,
    )


def assemble_master(segments: list[dict[str, Any]], output: Path, total: float) -> None:
    with wave.open(str(Path(segments[0]["file"])), "rb") as first:
        params = first.getparams()
    total_frames = round(total * params.framerate)
    master = bytearray(total_frames * params.sampwidth * params.nchannels)
    for segment in segments:
        with wave.open(str(Path(segment["file"])), "rb") as stream:
            current = (stream.getnchannels(), stream.getsampwidth(), stream.getframerate())
            expected = (params.nchannels, params.sampwidth, params.framerate)
            if current != expected:
                raise RuntimeError(f"incompatible WAV parameters: {segment['file']}")
            audio = stream.readframes(stream.getnframes())
        offset = round(float(segment["start"]) * params.framerate) * params.sampwidth * params.nchannels
        end = offset + len(audio)
        if end > len(master):
            raise RuntimeError(f"segment {segment['id']} exceeds the 90-second master")
        master[offset:end] = audio
    with wave.open(str(output), "wb") as target:
        target.setparams(params)
        target.writeframes(bytes(master))


def write_captions(segments: list[dict[str, Any]], srt: Path, vtt: Path) -> None:
    srt_blocks: list[str] = []
    vtt_blocks = ["WEBVTT\n"]
    for index, segment in enumerate(segments, 1):
        start = float(segment["start"])
        end = start + float(segment["duration"])
        label = f"{segment['speaker']}: {segment['text']}"
        srt_blocks.append(
            f"{index}\n{timestamp(start, ',')} --> {timestamp(end, ',')}\n{label}\n"
        )
        vtt_blocks.append(
            f"{timestamp(start, '.')} --> {timestamp(end, '.')}\n{label}\n"
        )
    srt.write_text("\n".join(srt_blocks), encoding="utf-8")
    vtt.write_text("\n".join(vtt_blocks), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--piper-python", required=True, type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    root = here.parent
    script_path = here / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    silent_video = root / "media" / "bellman-shadow-pricing.mp4"
    output_video = root / "media" / "bellman-shadow-pricing-narrated.mp4"
    audio_dir = here / "audio"
    segment_dir = audio_dir / "segments"
    caption_dir = here / "captions"
    segment_dir.mkdir(parents=True, exist_ok=True)
    caption_dir.mkdir(parents=True, exist_ok=True)

    rendered: list[dict[str, Any]] = []
    for item in script["segments"]:
        voice = script["voices"][item["speaker"]]
        output = segment_dir / f"{item['id']}-{item['speaker'].lower()}.wav"
        render_segment(args.piper_python, args.model_dir, voice, item["spoken_text"], output)
        duration = wav_duration(output)
        rendered.append({**item, "file": str(output), "duration": duration, "sha256": sha256(output)})

    for current, following in zip(rendered, rendered[1:]):
        if float(current["start"]) + float(current["duration"]) > float(following["start"]):
            raise RuntimeError(f"segments {current['id']} and {following['id']} overlap")
    if float(rendered[-1]["start"]) + float(rendered[-1]["duration"]) > 84.8:
        raise RuntimeError("narration must finish before the contact-card hold")

    master = audio_dir / "bellman-shadow-pricing-narration.wav"
    assemble_master(rendered, master, float(script["duration_seconds"]))
    normalized = audio_dir / "bellman-shadow-pricing-narration-normalized.wav"
    subprocess.run(
        [
            args.ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(master),
            "-af", "loudnorm=I=-16:TP=-2:LRA=11", "-ar", "22050", "-ac", "1",
            "-c:a", "pcm_s16le", "-t", "90", str(normalized),
        ],
        check=True,
    )
    normalized.replace(master)
    srt = caption_dir / "bellman-shadow-pricing-narrated.srt"
    vtt = caption_dir / "bellman-shadow-pricing-narrated.vtt"
    write_captions(rendered, srt, vtt)
    subprocess.run(
        [
            args.ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent_video), "-i", str(master), "-i", str(srt),
            "-map", "0:v:0", "-map", "1:a:0", "-map", "2:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
            "-metadata:s:a:0", "language=eng", "-metadata:s:s:0", "language=eng",
            "-movflags", "+faststart", "-t", "90", str(output_video),
        ],
        check=True,
    )

    receipt = {
        "schema": "bgi-open-build.offline-narration.v1",
        "render_timestamp": datetime.now(timezone.utc).isoformat(),
        "source_commit": args.source_commit,
        "python_version": sys.version.split()[0],
        "ffmpeg_version": subprocess.run(
            [args.ffmpeg, "-version"], check=True, capture_output=True, text=True
        ).stdout.splitlines()[0],
        "engine": {
            "name": "Piper",
            "version": importlib.metadata.version("piper-tts"),
            "source": "https://github.com/OHF-Voice/piper1-gpl",
            "license": "GPL-3.0",
            "redistributed": False,
        },
        "voices": script["voices"],
        "silent_video": {"file": "../media/bellman-shadow-pricing.mp4", "sha256": sha256(silent_video)},
        "script": {"file": "script.json", "sha256": sha256(script_path)},
        "segments": [
            {
                "id": row["id"], "speaker": row["speaker"], "start": row["start"],
                "duration": round(float(row["duration"]), 3), "text": row["text"],
                "spoken_text": row["spoken_text"],
                "file": f"audio/segments/{Path(row['file']).name}", "sha256": row["sha256"],
            }
            for row in rendered
        ],
        "audio_master": {"file": "audio/bellman-shadow-pricing-narration.wav", "sha256": sha256(master)},
        "captions": {
            "srt": {"file": "captions/bellman-shadow-pricing-narrated.srt", "sha256": sha256(srt)},
            "vtt": {"file": "captions/bellman-shadow-pricing-narrated.vtt", "sha256": sha256(vtt)},
        },
        "narrated_video": {
            "file": "../media/bellman-shadow-pricing-narrated.mp4",
            "sha256": sha256(output_video),
            "duration_seconds": 90.0, "video_codec": "h264", "width": 1920,

            "height": 1080, "frame_rate": "30/1", "pixel_format": "yuv420p",
            "audio_codec": "aac", "audio_sample_rate": 22050, "audio_channels": 1,
            "caption_codec": "mov_text",
        },
        "audio_normalization": "EBU R128 loudnorm target: -16 LUFS integrated, -2 dBTP, LRA 11",
        "mix": "locked silent H.264 video stream copied unchanged; normalized Piper WAV encoded as AAC 192 kbps; mov_text captions embedded",
        "review": {
            "timing": "all sentence segments non-overlapping; narration ends before 84.8-second contact hold",
            "pronunciation": "FabricPC -> Fabric P C; backprop -> back prop; decimals spoken digit-by-digit",
        },
        "duration_seconds": 90.0,
    }
    (here / "narration_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(f"rendered {len(rendered)} sentence segments")
    print(f"narration master: {master}")
    print(f"narrated film: {output_video}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
