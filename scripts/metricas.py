#!/usr/bin/env python3
"""Guarda metricas de los reels publicados a las 24 h, 72 h y 7 dias (sin IA, sin cupo de Claude).

Variables: IG_TOKEN, IG_API_VERSION (opcional). Escribe metricas/<id>.json.
"""
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API = f"https://graph.instagram.com/{os.environ.get('IG_API_VERSION', 'v25.0')}"
HITOS = {"24h": 24, "72h": 72, "7d": 168}
METRICAS = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions", "ig_reels_avg_watch_time"]


def get(ruta: str, params: dict) -> dict | None:
    q = urllib.parse.urlencode({**params, "access_token": os.environ["IG_TOKEN"].strip().strip("\"'")})
    try:
        with urllib.request.urlopen(f"{API}/{ruta}?{q}", timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"Aviso {ruta}: {e.code} {e.read().decode(errors='replace')[:200]}")
        return None


def insights(media_id: str) -> dict:
    out = {}
    # se piden de una en una para que una metrica no disponible no tumbe las demas
    for m in METRICAS:
        r = get(f"{media_id}/insights", {"metric": m})
        if r and r.get("data"):
            out[m] = r["data"][0].get("values", [{}])[0].get("value")
    return out


def main():
    ahora = dt.datetime.now(dt.timezone.utc)
    (RAIZ / "metricas").mkdir(exist_ok=True)
    for pub in sorted((RAIZ / "salida").glob("*/publicado.json")):
        p = json.loads(pub.read_text(encoding="utf-8"))
        gid = pub.parent.name
        ts = dt.datetime.fromisoformat(p["timestamp"].replace("+0000", "+00:00"))
        horas = (ahora - ts).total_seconds() / 3600
        ruta = RAIZ / "metricas" / f"{gid}.json"
        datos = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {"id": gid, "media_id": p["media_id"], "permalink": p.get("permalink")}
        for nombre, h in HITOS.items():
            if horas >= h and nombre not in datos:
                datos[nombre] = {"tomado": ahora.isoformat(timespec="minutes"), **insights(p["media_id"])}
                print(gid, nombre, datos[nombre])
        ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
