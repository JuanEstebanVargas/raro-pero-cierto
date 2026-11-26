#!/usr/bin/env python3
"""Publica en Instagram el reel pendiente mas antiguo (API oficial de Instagram con Instagram Login).

Requiere variables de entorno (secretos de GitHub Actions):
  IG_TOKEN    token de larga duracion de la cuenta profesional
  IG_USER_ID  id de la cuenta de Instagram (lo devuelve /me)
  REPO        owner/nombre del repositorio PUBLICO donde estan los videos (lo pone Actions)
Opcionales: IG_API_VERSION (por defecto v25.0), RAMA (por defecto main), SOLO_PROBAR=1

Un reel es "pendiente" si salida/<id>/qa.md dice APROBADO, no existe publicado.json,
no existe NO_PUBLICAR y la fecha del id es hoy o anterior (hora de Bogota).
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BOGOTA = dt.timezone(dt.timedelta(hours=-5))
# Los tokens de "Instagram Login" empiezan por IG y van a graph.instagram.com;
# los de "Facebook Login" (EAA...) van a graph.facebook.com. Se aceptan ambos.
_TOKEN = os.environ.get("IG_TOKEN", "").strip().strip("\"'")
_HOST = "graph.facebook.com" if _TOKEN.startswith("EAA") else "graph.instagram.com"
API = f"https://{_HOST}/{os.environ.get('IG_API_VERSION', 'v25.0')}"


def llamar(metodo: str, ruta: str, datos: dict) -> dict:
    datos = {**datos, "access_token": _TOKEN}
    cuerpo = urllib.parse.urlencode(datos).encode()
    url = f"{API}/{ruta}"
    if metodo == "GET":
        req = urllib.request.Request(url + "?" + cuerpo.decode())
    else:
        req = urllib.request.Request(url, data=cuerpo, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")
        raise SystemExit(f"Error de la API ({e.code}) en {ruta}: {detalle}")


def pendientes() -> list[Path]:
    hoy = dt.datetime.now(BOGOTA).date().isoformat()
    out = []
    for c in sorted((RAIZ / "salida").iterdir()):
        if not c.is_dir():
            continue
        qa = c / "qa.md"
        if (c / "publicado.json").exists() or (c / "NO_PUBLICAR").exists():
            continue
        if not qa.exists():
            continue
        cabecera = qa.read_text(encoding="utf-8")[:300]
        if "Resultado: APROBADO" not in cabecera:
            continue
        if c.name[:10] > hoy:
            continue
        out.append(c)
    return out


def main():
    cola = pendientes()
    if not cola:
        print("No hay reels pendientes de publicar.")
        return
    c = cola[0]
    repo, rama = os.environ["REPO"], os.environ.get("RAMA", "main")
    base = f"https://raw.githubusercontent.com/{repo}/{rama}/salida/{c.name}"
    caption = (c / "publicacion.txt").read_text(encoding="utf-8").strip()[:2200]
    print(f"Publicando {c.name}")
    if os.environ.get("SOLO_PROBAR"):
        print("SOLO_PROBAR activo: no se publica.", base)
        tipo = "Instagram Login (IG...)" if _TOKEN.startswith("IG") else "Facebook Login (EAA...)" if _TOKEN.startswith("EAA") else "desconocido"
        print(f"Token: tipo {tipo}, {len(_TOKEN)} caracteres, API {_HOST}")
        yo = llamar("GET", os.environ["IG_USER_ID"].strip(), {"fields": "username"})
        print(f"Token valido: publicaria en @{yo.get('username')}")
        return
    uid = os.environ["IG_USER_ID"]
    cont = llamar("POST", f"{uid}/media", {
        "media_type": "REELS",
        "video_url": f"{base}/video.mp4",
        "cover_url": f"{base}/portada.jpg",
        "caption": caption,
        "share_to_feed": "true",
    })["id"]
    # la carga es asincrona: esperar a FINISHED (hasta 10 minutos)
    for _ in range(60):
        estado = llamar("GET", cont, {"fields": "status_code,status"})
        if estado.get("status_code") == "FINISHED":
            break
        if estado.get("status_code") in {"ERROR", "EXPIRED"}:
            raise SystemExit(f"Instagram rechazo el video: {estado}")
        time.sleep(10)
    else:
        raise SystemExit("El contenedor no termino de procesarse en 10 minutos")
    media = llamar("POST", f"{uid}/media_publish", {"creation_id": cont})["id"]
    info = llamar("GET", media, {"fields": "permalink,timestamp"})
    (c / "publicado.json").write_text(json.dumps({"media_id": media, **info}, indent=1), encoding="utf-8")
    print("Publicado:", info.get("permalink"))


if __name__ == "__main__":
    if not os.environ.get("IG_TOKEN") or not os.environ.get("IG_USER_ID"):
        sys.exit("Faltan IG_TOKEN o IG_USER_ID")
    main()
