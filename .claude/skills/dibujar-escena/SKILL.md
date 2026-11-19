---
name: dibujar-escena
description: Dibuja ilustraciones SVG en el estilo de Raro Pero Cierto para las escenas de tipo svg de un guion. Usar al escribir un guion o cuando una escena necesite un dibujo nuevo.
---

# Dibujar escena SVG

## Contrato técnico

- `<svg viewBox='0 0 800 800' xmlns='http://www.w3.org/2000/svg'>` y nada fuera de ese lienzo.
- Usa comillas simples dentro del SVG (va dentro de un string JSON).
- Solo formas: `path`, `rect`, `circle`, `ellipse`, `polygon`, `line`, `g`, `text`. Sin `image`, `script`, `href`, filtros, degradados ni fuentes externas.
- Texto: `font-family='Montserrat' font-weight='900'`, mayúsculas, máximo 4 palabras por rótulo, tamaño 30 a 60.

## Estilo

- Plano, contorno `stroke='#1D1A2B'` de 12 a 16, `stroke-linejoin='round'`, `stroke-linecap='round'`.
- Colores: amarillo `#FFC531`, magenta `#E5426F`, turquesa `#1FA3A0`, piel `#F28C8C`, menta `#9BE3C4`, cielo `#8EC5FF`, marrón `#B07A4F`, blanco `#FFFFFF`. Fondo transparente (la plantilla pone el papel).
- Composición centrada, el sujeto ocupa del 50 al 75 % del lienzo. Deja aire en los bordes (40 px).
- Para emoción, cara simple: dos círculos de radio 18 a 24 y una curva.
- Para explicar procesos: flechas gruesas (`stroke-width='14'`) y 2 o 3 rótulos.

## Comprobación

Tras producir, mira los fotogramas del control de calidad: si el dibujo no se entiende en 1 segundo sin la voz, simplifícalo.
