#!/usr/bin/env python3
"""Control de calidad automatico de un guion (antes de producir) o de un video (despues).

Uso:
  python scripts/validar.py guion guiones/<id>.json
  python scripts/validar.py video salida/<id>
Sale con codigo 1 y lista de errores si algo falla.
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TIPOS = {"svg", "numero", "comparacion", "lista", "cierre"}
PROHIBIDAS = [
    "cura", "curar", "milagro", "garantizado", "100% seguro", "nunca falla",
    "los médicos no quieren", "secreto que", "dosis",
]


def validar_guion(ruta: str) -> list[str]:
    e: list[str] = []
    g = json.loads(Path(ruta).read_text(encoding="utf-8"))
    for campo in ["id", "tema", "titulo", "tituloAcento", "fuente", "evidencia", "bloques", "publicacion"]:
        if campo not in g:
            e.append(f"Falta el campo '{campo}'")
    if e:
        return e
    if Path(ruta).stem != g["id"]:
        e.append("El nombre del archivo debe ser igual al id")
    if len((g["titulo"] + " " + g["tituloAcento"]).split()) > 7:
        e.append("El gancho del titulo supera 7 palabras")
    if len(g["tema"]) > 12:
        e.append("La etiqueta de tema supera 12 caracteres")
    texto = " ".join(b.get("narracion", "") for b in g["bloques"])
    n = len(texto.split())
    if not 55 <= n <= 140:
        e.append(f"La narracion tiene {n} palabras; debe tener entre 55 y 140 (20 a 50 s)")
    if not 4 <= len(g["bloques"]) <= 8:
        e.append("Debe haber entre 4 y 8 bloques")
    if g["bloques"][-1]["escena"]["tipo"] != "cierre":
        e.append("El ultimo bloque debe ser la escena 'cierre'")
    for i, b in enumerate(g["bloques"]):
        esc = b.get("escena", {})
        if esc.get("tipo") not in TIPOS:
            e.append(f"Bloque {i}: tipo de escena invalido {esc.get('tipo')}")
        if len(b.get("narracion", "").split()) > 30:
            e.append(f"Bloque {i}: narracion de mas de 30 palabras; dividir")
        if esc.get("tipo") == "svg":
            svg = esc.get("svg", "")
            try:
                raiz = ET.fromstring(svg)
                if raiz.get("viewBox") != "0 0 800 800":
                    e.append(f"Bloque {i}: el SVG debe usar viewBox='0 0 800 800'")
            except ET.ParseError as x:
                e.append(f"Bloque {i}: SVG mal formado ({x})")
            if re.search(r"<script|href=|https?://", re.sub(r"xmlns(:\w+)?=['\"][^'\"]*['\"]", "", svg)):
                e.append(f"Bloque {i}: el SVG no puede tener scripts ni enlaces externos")
            if esc.get("etiqueta") and len(esc["etiqueta"].split()) > 7:
                e.append(f"Bloque {i}: etiqueta de mas de 7 palabras")
    bajo = texto.lower() + " " + g["publicacion"].get("descripcion", "").lower()
    for p in PROHIBIDAS:
        if re.search(r"\b" + re.escape(p) + r"\b", bajo):
            e.append(f"Palabra o promesa no permitida: '{p}'")
    if "Fuente" not in g["publicacion"].get("descripcion", ""):
        e.append("La descripcion debe incluir 'Fuente:' con la referencia completa")
    tags = g["publicacion"].get("hashtags", [])
    if not 3 <= len(tags) <= 5:
        e.append("Usar entre 3 y 5 hashtags")
    pub = Path(__file__).resolve().parent.parent / "ideas" / "publicados.json"
    if pub.exists():
        hechos = json.loads(pub.read_text(encoding="utf-8")).get("publicados", [])
        tit = (g["titulo"] + " " + g["tituloAcento"]).lower()
        for h in hechos:
            if h.get("id") != g["id"] and h.get("gancho", "").lower() == tit:
                e.append(f"Gancho repetido de {h['id']}")
    return e


def validar_video(carpeta: str) -> list[str]:
    e: list[str] = []
    c = Path(carpeta)
    v = c / "video.mp4"
    for f in ["video.mp4", "portada.jpg", "publicacion.txt"]:
        if not (c / f).exists():
            e.append(f"Falta {f}")
    if e:
        return e
    info = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate:format=duration,size",
         "-of", "json", str(v)], capture_output=True, text=True, check=True).stdout)
    vs = [s for s in info["streams"] if s["codec_type"] == "video"]
    au = [s for s in info["streams"] if s["codec_type"] == "audio"]
    if not vs or vs[0]["codec_name"] != "h264" or (vs[0]["width"], vs[0]["height"]) != (1080, 1920):
        e.append("El video debe ser H.264 1080x1920")
    if not au or au[0]["codec_name"] != "aac" or au[0]["sample_rate"] != "48000":
        e.append("El audio debe ser AAC 48 kHz")
    dur = float(info["format"]["duration"])
    if not 15 <= dur <= 90:
        e.append(f"Duracion {dur:.1f} s fuera de 15 a 90 s")
    if int(info["format"]["size"]) > 300 * 1024 * 1024:
        e.append("El archivo supera 300 MB")
    # detecta silencios largos (voz fallida)
    r = subprocess.run(["ffmpeg", "-i", str(v), "-af", "silencedetect=n=-45dB:d=2.5", "-f", "null", "-"], capture_output=True, text=True)
    if "silence_start" in r.stderr:
        e.append("Hay un silencio de mas de 2,5 s: revisar la voz")
    return e


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in {"guion", "video"}:
        sys.exit(__doc__)
    errores = validar_guion(sys.argv[2]) if sys.argv[1] == "guion" else validar_video(sys.argv[2])
    if errores:
        print("RECHAZADO")
        for x in errores:
            print(" -", x)
        sys.exit(1)
    print("APROBADO")
