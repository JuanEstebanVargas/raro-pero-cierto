---
name: escribir-guion
description: Escribe el guion JSON de un reel de Raro Pero Cierto a partir de una ficha verificada, con narración, escenas y texto de publicación. Usar después de verificar-dato.
---

# Escribir guion

Entrada: `fichas/<id>.md` (solo se puede afirmar lo que dice "Afirmación permitida") y `marca/guia-de-estilo.md`.
Salida: `guiones/<id>.json`. Ejemplo completo y válido: `guiones/2026-11-20-estomago.json`.

## Esquema

```json
{
  "id": "<id>", "tema": "CUERPO", "titulo": "Tu estómago", "tituloAcento": "no se digiere",
  "voz": "em_alex", "velocidad": 1.12,
  "fuente": "<cita corta: Autor, Revista, año | Agencia, año>",
  "evidencia": "<categoría de la ficha>",
  "bloques": [ {"narracion": "<1 o 2 frases>", "escena": { ... }} ],
  "publicacion": {"descripcion": "<2-3 frases>\n\nFuente: <cita completa>\n\n<pregunta>", "hashtags": ["#datoscuriosos", "..."]}
}
```

## Tipos de escena (una por bloque)

- `{"tipo":"numero","valor":243,"decimales":0,"unidad":"días","etiqueta":"dura un día en Venus"}` — cifra que cuenta hacia arriba.
- `{"tipo":"comparacion","a":{"nombre":"Venus: día","valor":243,"texto":"243"},"b":{"nombre":"Venus: año","valor":225,"texto":"225"}}` — dos barras.
- `{"tipo":"lista","titulo":"Su defensa","items":["...","...","..."]}` — 2 a 4 ítems de máximo 5 palabras.
- `{"tipo":"svg","etiqueta":"Un escudo de moco","svg":"<svg viewBox='0 0 800 800' ...>...</svg>"}` — ilustración propia (skill `dibujar-escena`).
- `{"tipo":"cierre"}` — obligatorio y último; sello "Raro pero cierto" + fuente.

## Reglas

- 4 a 7 bloques; 55 a 140 palabras en total; máximo 30 palabras por bloque.
- Primer bloque = el gancho, con la escena más llamativa (número o svg).
- Al menos 2 escenas `svg` por video. No repetir el mismo tipo más de 2 veces seguidas.
- Escribe números como se dicen ("doscientos cuarenta y tres" no; "243" sí: la voz los lee).
- Evita siglas que la voz lea mal; escribe "ADN" como "ADN" está bien, pero "pH" mejor como "pe hache" en la narración (en pantalla, "pH").
- La última frase de la narración termina en "Raro, pero cierto."
- Valida con `python scripts/validar.py guion guiones/<id>.json`.
