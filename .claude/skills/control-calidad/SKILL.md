---
name: control-calidad
description: Revisa un reel producido de Raro Pero Cierto (ciencia, texto, formato, imagen) y lo aprueba o rechaza con motivos. Usar después de producir el video y antes de entregarlo.
---

# Control de calidad

Revisa como si no hubieras escrito el guion.

1. `python scripts/validar.py video salida/<id>` debe decir APROBADO.
2. Extrae 6 fotogramas y míralos:
   `for t in 1 4 8 12 16 20; do ffmpeg -loglevel error -y -ss $t -i salida/<id>/video.mp4 -frames:v 1 -vf scale=540:-1 /tmp/qa_$t.png; done`
   Comprueba: texto legible y sin cortes, dibujos comprensibles, subtítulos sin tapar el dibujo, sin solapamientos.
3. Compara cada frase de la narración y cada rótulo con `fichas/<id>.md`: ninguna afirmación más fuerte que la "Afirmación permitida", matices presentes, cifras idénticas.
4. Ortografía y tildes en título, rótulos, subtítulos y descripción.
5. Nada de consejo médico ni promesas.
6. Escribe `salida/<id>/qa.md` con `APROBADO` o `RECHAZADO` y la lista de comprobaciones. Si rechazas, di exactamente qué cambiar.
