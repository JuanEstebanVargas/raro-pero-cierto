#!/usr/bin/env python3
"""Convierte un guion JSON en un reel 9:16 listo para Instagram.

Uso:  python scripts/producir.py guiones/<id>.json

Pasos: voz (Kokoro, local y gratis) -> tiempos de palabras -> render Remotion
-> portada -> normalizacion con FFmpeg -> salida/<id>/
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

RAIZ = Path(__file__).resolve().parent.parent
VIDEO = RAIZ / "video"
MODELOS = RAIZ / "modelos"
PAUSA = 0.28  # segundos de silencio entre bloques
COLA_CIERRE = 1.2  # segundos extra para que el sello final respire


def navegador() -> str | None:
    for p in [
        os.environ.get("RPC_CHROME"),
        "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
    ]:
        if p and Path(p).exists():
            return p
    return None  # Remotion descargara su propio navegador


def asegurar_modelos():
    MODELOS.mkdir(exist_ok=True)
    base = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
    for f in ["kokoro-v1.0.onnx", "voices-v1.0.bin"]:
        if not (MODELOS / f).exists():
            print(f"Descargando {f}...")
            subprocess.run(["curl", "-sSL", "-o", str(MODELOS / f), base + f], check=True)


def tiempos_palabras(texto: str, inicio: float, dur: float):
    """Reparte la duracion del bloque entre palabras segun su longitud.
    Aproximacion suficiente para subtitulos de 1 a 3 palabras."""
    palabras = texto.split()
    pesos = [len(w.strip("¿¡?!.,;:")) + 2 + (3 if w[-1] in ".,;:?!" else 0) for w in palabras]
    total = sum(pesos)
    t = inicio
    out = []
    for w, p in zip(palabras, pesos):
        d = dur * p / total
        out.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
        t += d
    return out


def main(ruta_guion: str):
    g = json.loads(Path(ruta_guion).read_text(encoding="utf-8"))
    gid = g["id"]
    salida = RAIZ / "salida" / gid
    salida.mkdir(parents=True, exist_ok=True)
    publico = VIDEO / "public" / gid
    publico.mkdir(parents=True, exist_ok=True)

    asegurar_modelos()
    from kokoro_onnx import Kokoro

    k = Kokoro(str(MODELOS / "kokoro-v1.0.onnx"), str(MODELOS / "voices-v1.0.bin"))
    voz = g.get("voz", "em_alex")
    vel = g.get("velocidad", 1.12)

    audio, palabras, escenas = [], [], []
    t = 0.25
    sr = 24000
    audio.append(np.zeros(int(sr * t), dtype=np.float32))
    for i, b in enumerate(g["bloques"]):
        texto = b["narracion"].strip()
        muestras, sr = k.create(texto, voice=voz, speed=vel, lang="es")
        dur = len(muestras) / sr
        palabras += tiempos_palabras(texto, t, dur)
        esc = dict(b["escena"])
        esc["inicio"] = round(max(0, t - (0.1 if i else 0)), 3)
        fin = t + dur + PAUSA
        if esc["tipo"] == "cierre":
            fin += COLA_CIERRE
        esc["fin"] = round(fin, 3)
        escenas.append(esc)
        audio.append(muestras.astype(np.float32))
        audio.append(np.zeros(int(sr * PAUSA), dtype=np.float32))
        t = fin if esc["tipo"] != "cierre" else t + dur + PAUSA
    duracion = escenas[-1]["fin"]
    pista = np.concatenate(audio)
    pista = pista / max(1e-6, np.abs(pista).max()) * 0.9
    sf.write(publico / "voz.wav", pista, sr)
    shutil.copy(publico / "voz.wav", salida / "voz.wav")

    props = {
        "id": gid,
        "tema": g["tema"],
        "titulo": g["titulo"],
        "tituloAcento": g["tituloAcento"],
        "duracion": round(duracion + 0.2, 3),
        "audio": f"{gid}/voz.wav",
        "escenas": escenas,
        "palabras": palabras,
        "fuente": g["fuente"],
        "evidencia": g["evidencia"],
    }
    (salida / "props.json").write_text(json.dumps(props, ensure_ascii=False, indent=1), encoding="utf-8")

    base = ["npx", "remotion"]
    extra = ["--props", str(salida / "props.json")]
    nav = navegador()
    if nav:
        extra += ["--browser-executable", nav]
    crudo = salida / "crudo.mp4"
    subprocess.run(base + ["render", "src/index.ts", "Dato", str(crudo), "--codec", "h264", "--concurrency", "4"] + extra, cwd=VIDEO, check=True)
    subprocess.run(base + ["still", "src/index.ts", "Portada", str(salida / "portada.jpg"), "--image-format", "jpeg"] + extra, cwd=VIDEO, check=True)

    # Normaliza al formato que pide la API de Instagram: H.264, yuv420p, AAC 48 kHz, moov al inicio
    final = salida / "video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(crudo),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20", "-r", "30",
        "-c:a", "aac", "-ar", "48000", "-b:a", "128k", "-movflags", "+faststart", str(final),
    ], check=True)
    crudo.unlink(missing_ok=True)

    pub = g.get("publicacion", {})
    texto = pub.get("descripcion", "") + "\n\n" + " ".join(pub.get("hashtags", []))
    (salida / "publicacion.txt").write_text(texto.strip() + "\n", encoding="utf-8")
    shutil.rmtree(publico, ignore_errors=True)
    print(f"Listo: {final}  ({duracion:.1f} s)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
