---
name: dato-diario
description: Produce el reel diario de Raro Pero Cierto de principio a fin (idea, verificación, guion, video, control de calidad, entrega). Usar en la ejecución programada diaria o cuando se pida "el video de hoy".
---

# Dato diario

Objetivo: dejar en `salida/<id>/` un reel aprobado por el control de calidad, con su portada y texto de publicación, y dejarlo en la cola de publicación automática.

`<id>` = `AAAA-MM-DD-palabra-clave`. La fecha es el primer día, desde hoy (hora de Bogotá), que todavía no tenga carpeta en `salida/`. Así la cola nunca tiene dos videos el mismo día. Si ya hay 3 o más videos en cola sin publicar (sin `publicado.json`), no produzcas otro: termina con un resumen.

## Pasos

1. `bash scripts/preparar.sh` (instala dependencias; tarda unos minutos la primera vez).
2. Si `ideas/backlog.json` tiene menos de 5 ideas en estado `puntuada`, ejecuta la skill `investigar-ideas`.
3. Toma la idea `puntuada` con mayor `puntuacion` cuyo pilar no se haya usado en los 2 últimos registros de `ideas/publicados.json`.
4. Skill `verificar-dato`. Si la idea queda `descartada`, vuelve al paso 3 (máximo 3 intentos; luego investiga de nuevo).
5. Skill `escribir-guion` → `guiones/<id>.json`.
6. `. .venv/bin/activate && python scripts/validar.py guion guiones/<id>.json`. Corrige y repite hasta APROBADO.
7. `python scripts/producir.py guiones/<id>.json`.
8. Skill `control-calidad`. Si rechaza, corrige el guion y vuelve al paso 6 (máximo 2 vueltas).
9. Actualiza la idea a `producida`, añade a `ideas/publicados.json` un registro `{id, fecha, pilar, gancho, fuente}`.
10. Haz commit en `main` de `fichas/`, `guiones/`, `ideas/` y `salida/<id>/` (video.mp4, portada.jpg, publicacion.txt, props.json, qa.md) y haz push a `main`. El flujo `Publicar reel del día` de GitHub Actions lo publica a las 18:00 de Bogotá de la fecha del id.
11. Ventana de veto: entre la producción y las 18:00, Juanes puede impedir la publicación creando el archivo `salida/<id>/NO_PUBLICAR`.
12. Termina con un resumen de 3 líneas: id, gancho, fuente.

## Ahorro de cupo

- No leas archivos grandes enteros (backlog: solo las ideas necesarias con `jq` o Python).
- No regeneres el video por cambios cosméticos menores; anótalos en el PR.
