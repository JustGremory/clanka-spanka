# /// script
# dependencies = ["numpy", "soundfile", "yt-dlp", "imageio-ffmpeg"]
# ///
"""Builds the hit sound from the cartoon whip clip the user picked.

Run: uv run tools/make_sound.py
Source: "Whip (Crack) - Sound Effect | ProSounds", https://www.youtube.com/watch?v=-EeXrcGEa88
Output: resourcepack/assets/clanka_spanka/sounds/whip.ogg (mono Ogg Vorbis, trimmed, loudness-matched
to vanilla's sweep attack so it is not drowned out by the normal hit sounds).
"""
import subprocess
import tempfile
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import soundfile as sf
import yt_dlp

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "resourcepack" / "assets" / "clanka_spanka" / "sounds" / "whip.ogg"
URL = "https://www.youtube.com/watch?v=-EeXrcGEa88"
RATE = 48000
PRE_ROLL = 0.01  # seconds kept before the whip starts, so it lands on the hit
TAIL = 0.15  # fade-out length
TARGET_RMS_DB = -10.0  # vanilla entity/player/attack/sweep1.ogg measures about -9 dB over its active part
CEILING = 0.95


def download(workdir: Path) -> np.ndarray:
    options = {"format": "bestaudio", "outtmpl": str(workdir / "clip.%(ext)s"), "quiet": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(options) as ydl:
        source = Path(ydl.prepare_filename(ydl.extract_info(URL)))
    wav = workdir / "clip.wav"
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(source), "-ac", "1", "-ar", str(RATE), str(wav)], check=True)
    audio, _ = sf.read(wav)
    return audio


def active_span(audio: np.ndarray) -> tuple[int, int]:
    window = int(RATE * 0.02)
    levels = np.array([np.sqrt(np.mean(audio[i:i + window] ** 2)) for i in range(0, len(audio) - window, window)])
    loud = np.where(levels > 0.01 * levels.max())[0]  # within 40 dB of the loudest window
    return loud[0] * window, (loud[-1] + 1) * window


def master(audio: np.ndarray) -> np.ndarray:
    start, end = active_span(audio)
    clip = audio[max(0, start - int(PRE_ROLL * RATE)):end].copy()
    fade = int(TAIL * RATE)
    clip[-fade:] *= np.linspace(1.0, 0.0, fade)
    body_start, body_end = active_span(clip)
    rms = np.sqrt(np.mean(clip[body_start:body_end] ** 2))
    gained = clip * (10 ** (TARGET_RMS_DB / 20) / rms)
    return (CEILING * np.tanh(gained / CEILING)).astype(np.float32)  # soft limiter keeps peaks under the ceiling


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        sound = master(download(Path(tmp)))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sf.write(OUT, sound, RATE, format="OGG", subtype="VORBIS")
    start, end = active_span(sound)
    body = sound[start:end]
    print(f"wrote {OUT}: {len(sound) / RATE:.2f}s, peak {np.abs(sound).max():.2f}, "
          f"active RMS {20 * np.log10(np.sqrt(np.mean(body ** 2))):.1f} dB")


if __name__ == "__main__":
    main()
