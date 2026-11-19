---
name: analizar-rendimiento
description: Analiza las métricas de los reels publicados de Raro Pero Cierto y actualiza ideas/rendimiento.md con lo que funciona. Usar en el informe semanal o cuando haya métricas nuevas en metricas/.
---

# Analizar rendimiento

Entrada: `metricas/*.json` (un archivo por reel con vistas, me gusta, comentarios, guardados, compartidos y seguidores ganados a 24 h, 72 h y 7 días). Si no hay API configurada, Juanes puede pegar los números de la app en `metricas/<id>.json` con el mismo formato.

1. Calcula la mediana de vistas a 72 h de los últimos 20 reels.
2. Para cada reel: rendimiento relativo = vistas / mediana; envíos y guardados por cada 1.000 vistas.
3. Agrupa por pilar, tipo de gancho (contradicción, cifra, pregunta), primera escena (numero, svg) y duración.
4. Un formato es "ganador" si 3 de sus 4 últimos reels superan 1,5 veces la mediana.
5. Actualiza `ideas/rendimiento.md` con: top 3 formatos, pilares a subir o bajar, y como máximo 3 cambios concretos para la semana siguiente. `investigar-ideas` lo lee al puntuar.
6. Escribe `informes/semana-AAAA-WW.md` con las cifras y las recomendaciones.
