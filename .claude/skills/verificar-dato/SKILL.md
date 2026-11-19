---
name: verificar-dato
description: Verifica un dato curioso con fuentes fiables antes de escribir el guion de Raro Pero Cierto, y fija la afirmación máxima permitida. Usar siempre antes de escribir-guion.
---

# Verificar dato

Actúa como un verificador escéptico: tu trabajo es encontrar por qué el dato podría ser falso o exagerado.

1. Busca al menos 2 fuentes fiables e independientes: artículos científicos o revisiones, agencias públicas (NASA, NOAA, OMS, institutos nacionales), museos y universidades, enciclopedias con referencias. Evita blogs de "curiosidades" como fuente final.
2. Comprueba cifras exactas, unidades y matices ("hasta", "en promedio", "en algunas especies").
3. Clasifica la evidencia: `Revisión científica`, `Estudio científico`, `Agencia oficial`, `Dato histórico`, `Consenso científico`.
4. Escribe `fichas/<id>.md`:

```
# <dato>
Veredicto: VERIFICADO | MATIZADO | FALSO
Afirmación permitida: <la frase más fuerte que la evidencia sostiene, ni una palabra más>
Matices obligatorios: <lo que no se puede omitir>
Cifras: <cifra = valor + unidad + fuente>
Fuentes:
1. <cita completa> — <url>
2. <cita completa> — <url>
Evidencia: <categoría>
```

5. Si es FALSO, la idea solo vale como pilar MITO (desmentido). Si no hay 2 fuentes fiables, marca la idea `descartada` con el motivo.
6. Actualiza el estado en el backlog a `verificada` o `descartada`.
