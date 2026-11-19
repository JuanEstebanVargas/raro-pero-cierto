---
name: investigar-ideas
description: Busca y puntúa nuevas ideas de datos curiosos para Raro Pero Cierto y las añade a ideas/backlog.json. Usar cuando el backlog tenga menos de 5 ideas puntuadas o se pida investigar tendencias.
---

# Investigar ideas

Añade de 8 a 12 ideas nuevas al backlog, puntuadas.

## Fuentes (gratuitas y legales, sin scraping de Instagram)

- Búsqueda web: noticias de ciencia de los últimos 14 días (descubrimientos, estudios nuevos, efemérides del mes).
- Preguntas frecuentes: búsquedas tipo "por qué...", "es verdad que...", foros de preguntas.
- Efemérides: aniversarios del día o la semana (historia, ciencia, espacio).
- Tendencias: temas que crecen en buscadores y en Shorts/Reels de divulgación (solo para detectar temas, nunca copiar).
- `ideas/rendimiento.md`, si existe: los pilares y ganchos que mejor han funcionado.

## Para cada idea

Registro en `ideas/backlog.json` → `ideas[]`:
```json
{"slug": "pulpo-tres-corazones", "pilar": "ANIMALES", "dato": "El pulpo tiene tres corazones y sangre azul", "gancho": "El pulpo / tiene tres corazones", "por_que_ahora": "", "fuentes_iniciales": ["url"], "puntos": {"V":4,"R":5,"D":3,"A":2,"I":4,"F":5}, "puntuacion": 0, "estado": "puntuada", "creada": "AAAA-MM-DD"}
```

## Puntuación (1 a 5 cada criterio)

- **V** Viralidad: ¿provoca "no puede ser" y ganas de enviarlo? (25 %)
- **R** Relevancia: ¿es raro Y cierto, y se explica en 30 s? (20 %)
- **D** Diferenciación: ¿poco visto, o con un ángulo nuevo? (15 %)
- **A** Actualidad: ¿noticia, efeméride o tendencia ahora? (15 %)
- **I** Interacción: ¿invita a comentar o guardar? (15 %)
- **F** Facilidad: ¿se dibuja con formas simples y las plantillas existentes? (10 %)

`puntuacion = round(20 * (0.25V + 0.20R + 0.15D + 0.15A + 0.15I + 0.10F))` (sobre 100).

## Filtros eliminatorios

- Ya está en `ideas/publicados.json` o en el backlog (mismo dato).
- Requiere imágenes reales sensibles, violencia, o personas reales identificables.
- Es consejo médico o de salud individual.
- No hay al menos una fuente fiable a la vista.
