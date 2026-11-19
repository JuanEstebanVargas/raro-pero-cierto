---
name: dato-diario
description: Produce el reel diario de Raro Pero Cierto de principio a fin (idea, verificación, guion, video, control de calidad, entrega). Usar en la ejecución programada diaria o cuando se pida "el video de hoy".
---

# Dato diario

Objetivo: dejar en `salida/<id>/` un reel aprobado por el control de calidad, con su portada y texto de publicación, y entregarlo en una rama nueva con un pull request.

`<id>` = `AAAA-MM-DD-palabra-clave` con la fecha de publicación prevista (mañana si se ejecuta de noche).

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
10. Crea la rama `claude/dato-<id>`, haz commit de `fichas/`, `guiones/`, `ideas/` y `salida/<id>/` (video.mp4, portada.jpg, publicacion.txt, props.json) y abre un pull request titulado `Dato <id>: <gancho>` con: el gancho, el texto de publicación, la fuente y el resultado del control de calidad. Fusionar el PR = aprobación humana.

## Ahorro de cupo

- No leas archivos grandes enteros (backlog: solo las ideas necesarias con `jq` o Python).
- No regeneres el video por cambios cosméticos menores; anótalos en el PR.
