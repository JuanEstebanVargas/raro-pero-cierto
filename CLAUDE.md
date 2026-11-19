# Raro Pero Cierto — fábrica de reels de datos curiosos

Cuenta de Instagram que publica **un dato curioso verificado al día** en un reel vertical de 20 a 45 s, animado con código (SVG + Remotion), con voz sintética local (Kokoro) y subtítulos karaoke. Presupuesto: solo Claude Pro; todo lo demás es software gratuito.

## Reglas que no se rompen

1. **Nada se publica sin fuente.** Cada dato necesita al menos 2 fuentes fiables independientes (revista científica, agencia pública, museo, universidad, enciclopedia con referencias). Si no las hay, el dato se descarta.
2. **Cero mitos disfrazados de dato.** Si una "curiosidad" popular es falsa, solo se usa para desmentirla, y se dice explícitamente.
3. **Nada de consejo médico, dosis ni promesas de salud.** Hablamos de cómo funciona algo, nunca de qué debe hacer alguien.
4. **Originalidad.** Nunca copiar guion, imágenes ni estructura literal de otra cuenta. Se toman temas y formatos, no contenido.
5. **Publicación automática con ventana de veto.** Solo se publica lo que el control de calidad marca `Resultado: APROBADO`. Juanes puede frenar un video creando `salida/<id>/NO_PUBLICAR` antes de las 18:00 de Bogotá.
6. **Voz:** voz sintética fija (`em_alex`, velocidad 1.12). Nunca clonar ni imitar la voz de una persona real.

## Flujo diario (skill `dato-diario`)

1. `investigar-ideas` → añade candidatos a `ideas/backlog.json` y los puntúa.
2. Elegir la idea con mayor puntuación que esté en estado `puntuada`.
3. `verificar-dato` → ficha en `fichas/<id>.md`; si falla, marcar `descartada` y volver al paso 2.
4. `escribir-guion` → `guiones/<id>.json` (usa `dibujar-escena` para los SVG).
5. `python scripts/validar.py guion guiones/<id>.json` → corregir hasta APROBADO.
6. `python scripts/producir.py guiones/<id>.json` → `salida/<id>/`.
7. `control-calidad` → `python scripts/validar.py video salida/<id>` + revisión visual de fotogramas.
8. Registrar en `ideas/publicados.json`, actualizar estado a `producida`, commit y push a `main`.
9. GitHub Actions publica a las 18:00 de Bogotá (`.github/workflows/publicar.yml`), descarga métricas cada 6 h y renueva el token de Instagram cada 15 días.

## Archivos

- `marca/guia-de-estilo.md` — tono, paleta, reglas visuales.
- `ideas/backlog.json` — ideas con estado y puntuación. Estados: `entrante`, `puntuada`, `verificada`, `descartada`, `guionizada`, `producida`, `publicada`.
- `ideas/publicados.json` — historial para no repetir temas.
- `fichas/` — verificación con fuentes. `guiones/` — guion + escenas. `salida/` — video final, portada, texto.
- `video/` — proyecto Remotion (plantilla `src/Dato.tsx`, colores en `src/marca.ts`).
- `scripts/preparar.sh` — instala dependencias (ejecutar primero en un entorno nuevo).

## Comandos

```
bash scripts/preparar.sh
. .venv/bin/activate
python scripts/validar.py guion guiones/<id>.json
python scripts/producir.py guiones/<id>.json
python scripts/validar.py video salida/<id>
```
