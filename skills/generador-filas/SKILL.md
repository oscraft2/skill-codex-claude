---
name: generador-filas
version: 1.0.0
author: proscar.cl
description: >
  Genera filas B, C, D (y más) a partir de una prueba fila A en Word (.docx).
  Mismas preguntas, mismas alternativas, distinto orden. Incluye tabla de
  equivalencias para corrección docente. Compatible con el formato ISPM y
  cualquier prueba de selección múltiple.
triggers:
  - "haz la fila B"
  - "genera las filas"
  - "crea fila B de la prueba"
  - "quiero fila B y C"
  - "genera versión B de la prueba"
  - "orden diferente de preguntas"
  - "mezcla las preguntas"
  - "make another version of the test"
compatibility: Claude Code, Codex CLI, Claude.ai (con archivos adjuntos)
requires:
  - python3
  - python-docx (pip install python-docx)
---

# Skill: Generador de Filas de Prueba

## ¿Qué hace este skill?

A partir de una prueba fila A en Word, genera automáticamente filas B, C, D…
con las mismas preguntas y alternativas, pero en orden diferente. Al final
produce una **tabla de equivalencias** para que el docente pueda corregir
todas las filas fácilmente.

---

## Qué cambia entre filas

| Elemento | ¿Cambia? |
|---|---|
| Texto de las preguntas | ✅ Sí — orden mezclado |
| Texto de las alternativas | ✅ Sí — orden mezclado dentro de cada pregunta |
| Enunciado de la prueba | ❌ No |
| Instrucciones | ❌ No |
| Nombre del colegio / encabezado | ❌ No |
| Puntaje total | ❌ No |
| Número de preguntas | ❌ No |

---

## Instrucciones para el agente

### PASO 1 — Leer la prueba fila A

```python
python scripts/generador_filas.py --input prueba_fila_A.docx --filas B C
```

El script:
1. Lee el .docx y extrae todas las preguntas de selección múltiple
2. Detecta el encabezado, instrucciones y pie de página (no los toca)
3. Mezcla preguntas y alternativas con semilla diferente por fila
4. Genera un .docx por fila + un .docx con la tabla de equivalencias

### PASO 2 — Qué detecta automáticamente

El script detecta preguntas por estos patrones:
- Numeradas: "1.", "2.", "1)", "2)"
- Con alternativas: "a)", "b)", "c)", "d)", "e)" o "A)", "B)", "C)", "D)", "E)"
- También detecta tablas de 2 columnas estilo ISPM

### PASO 3 — Tabla de equivalencias (para el docente)

Ejemplo de tabla generada:

| Preg. Fila A | Resp. A | Preg. Fila B | Resp. B | Preg. Fila C | Resp. C |
|---|---|---|---|---|---|
| 1 | C | 4 | A | 7 | B |
| 2 | A | 1 | D | 3 | A |
| ... | | | | | |

Esta tabla permite corregir cualquier fila usando la misma pauta.

---

## Ejemplo de uso

```bash
# Generar fila B a partir de fila A
python scripts/generador_filas.py --input prueba_A.docx --filas B

# Generar filas B, C y D
python scripts/generador_filas.py --input prueba_A.docx --filas B C D

# Especificar semilla (para reproducibilidad)
python scripts/generador_filas.py --input prueba_A.docx --filas B C --semilla 42

# Mezclar solo preguntas (no alternativas)
python scripts/generador_filas.py --input prueba_A.docx --filas B --no-mezclar-alternativas
```

---

## Instalación

```bash
git clone https://github.com/oscraft2/skill-codex-claude.git
cd skill-codex-claude
pip install python-docx

python scripts/generador_filas.py --input mi_prueba.docx --filas B C
```
