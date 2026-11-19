"""Transcribe un video o audio en tu computadora, gratis, con Whisper (faster-whisper).

Recurso gratis de @alfredits.ia · alfredits.github.io/comunidad/texto/

Crea dos archivos al lado del video:
  - <nombre>.srt          subtítulos por frases (sirven en CapCut, Premiere o YouTube)
  - <nombre>.palabras.json cada palabra con su tiempo exacto (para karaoke y cortes)

Uso:
  python transcribir.py mi-video.mp4
  python transcribir.py mi-video.mp4 --idioma es --modelo large-v3-turbo

Necesita FFmpeg y el paquete faster-whisper (pip install faster-whisper).
Si tienes tarjeta NVIDIA la usa; si no, funciona en el procesador (más lento).
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path


def activar_cuda_windows():
    """En Windows, las DLL de NVIDIA instaladas con pip no se encuentran solas."""
    if os.name != "nt":
        return
    import site
    for sp in site.getsitepackages():
        nvidia = Path(sp) / "nvidia"
        if nvidia.is_dir():
            for carpeta in nvidia.glob("*/bin"):
                os.add_dll_directory(str(carpeta))
                os.environ["PATH"] = str(carpeta) + os.pathsep + os.environ["PATH"]


def extraer_audio(video, destino):
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(destino)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def leer_wav(ruta):
    import numpy as np
    with wave.open(str(ruta), "rb") as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return pcm.astype(np.float32) / 32768.0


def cargar_modelo(nombre):
    from faster_whisper import WhisperModel
    try:
        return WhisperModel(nombre, device="cuda", compute_type="int8_float16"), "la tarjeta de video"
    except Exception:
        return WhisperModel(nombre, device="cpu", compute_type="int8"), "el procesador"


def tiempo_srt(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    seg, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{seg:02d},{ms:03d}"


def main():
    ap = argparse.ArgumentParser(description="Transcribe gratis en tu computadora con Whisper")
    ap.add_argument("archivo", type=Path, help="video o audio")
    ap.add_argument("--idioma", default=None, help="código de idioma, por ejemplo es o en (si no, lo detecta)")
    ap.add_argument("--modelo", default="large-v3-turbo", help="modelo de Whisper (small es más rápido)")
    args = ap.parse_args()

    archivo = args.archivo.resolve()
    if not archivo.exists():
        sys.exit(f"No encuentro el archivo: {archivo}")

    activar_cuda_windows()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / "audio.wav"
        print("Sacando el audio…", flush=True)
        extraer_audio(archivo, audio)
        modelo, dispositivo = cargar_modelo(args.modelo)
        print(f"Transcribiendo con {dispositivo}…", flush=True)
        segmentos, info = modelo.transcribe(leer_wav(audio), language=args.idioma,
                                            word_timestamps=True, vad_filter=True, beam_size=5)
        segmentos = list(segmentos)

    palabras = [
        {"texto": w.word.strip(), "inicio": round(w.start, 3), "fin": round(w.end, 3)}
        for seg in segmentos for w in (seg.words or []) if w.word.strip()
    ]
    srt = []
    for i, seg in enumerate(segmentos, 1):
        srt.append(f"{i}\n{tiempo_srt(seg.start)} --> {tiempo_srt(seg.end)}\n{seg.text.strip()}\n")

    base = archivo.with_suffix("")
    Path(f"{base}.srt").write_text("\n".join(srt), encoding="utf-8")
    Path(f"{base}.palabras.json").write_text(
        json.dumps({"idioma": info.language, "palabras": palabras}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Listo: {base.name}.srt y {base.name}.palabras.json ({len(palabras)} palabras, idioma {info.language})")


if __name__ == "__main__":
    main()
