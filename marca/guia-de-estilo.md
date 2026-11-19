# Guía de estilo — Raro Pero Cierto

## Concepto

"Lo que no sabías y es verdad, en 30 segundos y con la fuente." Datos curiosos de temática abierta, siempre verificados.

## Pilares (rotar para variedad; no más de 2 días seguidos del mismo)

| Pilar | Etiqueta `tema` | Ejemplos |
| --- | --- | --- |
| Cuerpo humano | CUERPO | por qué el estómago no se digiere, huesos que se renuevan |
| Animales | ANIMALES | pulpos con tres corazones, tardígrados |
| Espacio | ESPACIO | un día en Venus dura más que su año |
| Historia | HISTORIA | Cleopatra vivió más cerca del iPhone que de las pirámides |
| Ciencia cotidiana | CIENCIA | por qué el hielo flota, la miel no caduca |
| Mente | MENTE | por qué olvidas a qué entraste a una habitación |
| Mito desmentido | MITO | "solo usamos el 10 % del cerebro" (falso) |

## Personalidad y tono

- Curiosa, precisa, con humor seco. Un amigo que sabe mucho y lo cuenta sin presumir.
- Segunda persona ("tu estómago", "tú crees que..."). Frases de 6 a 15 palabras.
- Español neutro, sin regionalismos fuertes. Números con coma decimal (1,5).
- Prohibido: frases motivacionales, alarmismo, "no lo vas a creer", "los científicos odian esto".

## Estructura del guion (20 a 45 s, 55 a 140 palabras)

1. **Gancho (0 a 3 s):** el dato en su versión más sorprendente o una pregunta imposible. Nunca "hoy te voy a contar".
2. **Giro (3 a 8 s):** la pregunta que el espectador se hace ("¿y entonces por qué...?").
3. **Explicación (8 a 30 s):** el mecanismo en 2 o 3 pasos, cada uno con su escena.
4. **Remate (últimos 5 s):** una consecuencia o comparación memorable + "Raro, pero cierto." como frase final.

## Título en pantalla (gancho)

- `titulo` + `tituloAcento` juntos: 3 a 7 palabras. El acento es la parte sorprendente.
- Formatos que funcionan: contradicción ("Tu estómago / no se digiere"), cifra ("Un día en Venus / dura 243 días"), pregunta ("¿Por qué el hielo / flota?").

## Visual

- Paleta en `video/src/marca.ts`: papel `#F3ECDF`, tinta `#1D1A2B`, amarillo `#FFC531`, magenta `#E5426F`, turquesa `#1FA3A0`. Colores de apoyo permitidos en SVG: rosa piel `#F28C8C`, verde menta `#9BE3C4`, azul cielo `#8EC5FF`, marrón `#B07A4F`.
- Ilustración plana, contorno de tinta de 12 a 16 px, esquinas redondeadas, sin degradados ni sombras.
- Personajes y objetos con cara simple (dos puntos y una curva) cuando ayude a la emoción.
- Una idea por escena. Texto dentro del SVG: máximo 4 palabras por rótulo, en mayúsculas, Montserrat 900.
- Variar tipos de escena: no repetir el mismo tipo más de 2 veces seguidas.

## Publicación

- Descripción: 2 o 3 frases que amplían el dato + línea "Fuente:" con la referencia completa + una pregunta al público.
- 3 a 5 hashtags: siempre `#datoscuriosos` + 1 del pilar + 1 o 2 específicos.
- Audio: la voz va en el video. Si se publica desde la app, se puede añadir música en tendencia a volumen bajo.
