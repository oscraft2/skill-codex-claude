---
name: planificacion-curricular-chile
version: 1.0.0
author: proscar.cl
description: >
  Completa, genera y valida documentos de planificación curricular según
  la normativa vigente del Ministerio de Educación de Chile. Compatible con
  planificaciones anuales, redes de contenido, unidades didácticas, planes
  de clase y planillas de evaluación. El usuario sube su formato y el skill
  lo completa con los OA oficiales del currículum nacional (1° Básico a 4° Medio).
triggers:
  - "completa la planificación"
  - "haz una planificación"
  - "crea una red de contenidos"
  - "genera un plan de clases"
  - "llena el formato de planificación"
  - "planificación anual"
  - "unidad didáctica"
  - "red anual de contenidos"
  - "make a lesson plan"
  - "curriculum planning chile"
compatibility: Claude Code, Codex CLI, Claude.ai (con archivos adjuntos)
requires:
  - python3
  - python-docx (pip install python-docx)
---

# Skill: Planificación Curricular — Chile

## Qué hace este skill

Cuando el usuario sube un documento de planificación (vacío o parcialmente
completado), el agente lo analiza, identifica los campos vacíos y los llena
usando los OA oficiales del Mineduc, los indicadores de evaluación sugeridos,
los objetivos transversales y la estructura de unidades de los Programas
de Estudio vigentes.

Funciona con cualquier asignatura. El usuario solo necesita subir su
formato institucional — tabla Word, Excel, PDF — y decir para qué
nivel y asignatura es.

---

## Tipos de documento que maneja

| Documento | Descripción | Entrada |
|-----------|-------------|---------|
| Planificación anual | OA por semestre/mes, horas, evaluación | .docx, .xlsx |
| Red de contenidos | Mapa de unidades y OA | .docx, .xlsx |
| Unidad didáctica | OA, indicadores, actividades, evaluación | .docx |
| Plan de clase | Inicio/desarrollo/cierre, tiempo, recursos | .docx |
| Planilla de evaluación | Rúbricas, listas de cotejo | .docx, .xlsx |

---

## Instrucciones para el agente

### PASO 1 — Analizar el documento del usuario

Leer el archivo adjunto e identificar:
- Asignatura (Matemática, Lenguaje, Historia, Ciencias, etc.)
- Nivel/curso (1° Básico, 2° Medio, etc.)
- Tipo de documento (ver tabla arriba)
- Campos vacíos que necesitan completarse
- Formato institucional (columnas, secciones, estilo)

IMPORTANTE: Nunca cambiar el formato visual. Solo completar el contenido.

### PASO 2 — Cargar los OA del nivel

```python
import json
from pathlib import Path

oa_data = json.loads(Path("oa_data/oa_todos_niveles.json").read_text(encoding="utf-8"))
oa_nivel = oa_data["asignaturas"]["Matematica"]["niveles"]["2° Medio"]["OA"]
```

Si el archivo no existe, los OA de Matemática 1° a 4° Medio están en
`oa_data/oa_matematica_1_4medio.json` con sus URLs de verificación.

### PASO 3 — Completar según el tipo de documento

#### Planificación anual
Para cada unidad/mes/semestre, completar:
- Códigos de OA oficiales del programa
- Eje temático (Números, Álgebra, Geometría, Probabilidad, etc.)
- Horas pedagógicas estimadas (según Plan de Estudios Mineduc)
- Habilidades asociadas (resolver problemas, modelar, representar, argumentar)
- Tipo de evaluación sugerida (diagnóstica / formativa / sumativa)

#### Red de contenidos
- Organizar OA por unidad temática con secuencia lógica
- Marcar OA priorizados (Priorización 2023-2025) vs complementarios
- Indicar relaciones entre OA de distintas unidades
- Señalar cuáles están relacionados con PAES o SIMCE

#### Unidad didáctica — estructura estándar Mineduc

```
1. IDENTIFICACIÓN
   Asignatura / Nivel / Unidad N° / Tiempo estimado en horas

2. PROPÓSITO DE LA UNIDAD
   2-3 oraciones describiendo el aprendizaje central

3. OBJETIVOS DE APRENDIZAJE
   - Código oficial (ej: MA2M OA 03)
   - Descripción textual literal del currículum nacional
   - OAT asociados (convivencia escolar, TICs, medioambiente, etc.)

4. INDICADORES DE EVALUACIÓN
   - Mínimo 3 por OA
   - Verbo observable en 3ra persona plural
   - Ej: "Calculan el módulo de un número complejo dado su forma binomial"

5. ACTIVIDADES DE APRENDIZAJE
   Inicio (10-15 min): activación de conocimientos previos
   Desarrollo (25-30 min): actividad principal + recursos
   Cierre (10 min): síntesis + evaluación formativa

6. EVALUACIÓN
   Tipo / Instrumento / Criterios de logro

7. RECURSOS Y MATERIALES
   Texto escolar Mineduc, material adicional, software educativo
```

#### Plan de clase
```
DATOS:      Fecha / Curso / N° de clase / Tiempo (45 o 90 min)
OA:         Código + descripción completa
INICIO:     (10-15 min) Activación + pregunta problematizadora
DESARROLLO: (25-30 min) Actividad central + recursos
CIERRE:     (10 min) Síntesis + retroalimentación
EVALUACIÓN: Cómo se observa el logro en esta clase
```

### PASO 4 — Respetar la normativa vigente

#### Bases curriculares vigentes
| Nivel | Base curricular | Vigencia |
|-------|----------------|---------|
| 1° a 6° Básico | Bases Curriculares 2012 | Vigente |
| 7° a 2° Medio | Bases Curriculares 2015 | Vigente |
| 3° y 4° Medio | Bases Curriculares 2019 | Desde 2020 |

#### Estructura de códigos OA por asignatura y nivel
```
Matemática
  1°–6° Básico:  MA01 OA 01, MA02 OA 01, ... (número según nivel)
  7°–8° Básico:  MA07 OA 01 ... MA07 OA 19
  1° Medio:      MA1M OA 01 ... MA1M OA 15
  2° Medio:      MA2M OA 01 ... MA2M OA 12
  3° Medio FG:   FG-MATE-3M-OAC-01 ... FG-MATE-3M-OAC-04
  4° Medio FG:   FG-MATE-4M-OAC-01 ... FG-MATE-4M-OAC-04

Lenguaje y Comunicación / Lengua y Literatura
  1°–6° Básico:  LE01 OA 01 ...
  7°–2° Medio:   LE7B OA 01 ...
  3°–4° Medio:   FG-LEN-3M-OAC-01 ...

Historia, Geografía y CC.SS.
  1°–6° Básico:  HI01 OA 01 ...
  7°–2° Medio:   HI7B OA 01 ...

Ciencias Naturales / Biología / Física / Química
  1°–6° Básico:  CN01 OA 01 ...
  7°–2° Medio:   CN7B OA 01 ... (luego se dividen por especialidad en Media)
```

#### Horas pedagógicas semanales mínimas (Plan de Estudios Mineduc)
```
Matemática:   1°–6° Básico: 6 h | 7°–2° Medio: 4 h | 3°–4° Medio: 4 h
Lenguaje:     1°–6° Básico: 8 h | 7°–2° Medio: 5 h | 3°–4° Medio: 4 h
Historia:     1°–6° Básico: 3 h | 7°–2° Medio: 3 h | 3°–4° Medio: 3 h
Ciencias:     1°–6° Básico: 2 h | 7°–2° Medio: 3 h | 3°–4° Medio: 4 h
Ed. Física:   todos los niveles: 2 h
Inglés:       5°–6° Básico: 3 h | 7°–2° Medio: 3 h | 3°–4° Medio: 4 h
```

#### Priorización Curricular 2023-2025
Los OA se clasifican en:
- **Basales**: fundamentales, no se pueden omitir
- **Complementarios**: se trabajan si hay tiempo disponible

El agente debe indicar la clasificación cuando complete planificaciones.

### PASO 5 — Redacción de indicadores de evaluación

Estructura: VERBO OBSERVABLE + CONTENIDO + CONDICIÓN (opcional)

```
Correcto:
  "Calculan el módulo de números complejos en forma binomial"
  "Resuelven ecuaciones cuadráticas mediante factorización"
  "Representan números enteros en la recta numérica"

Incorrecto:
  "Conocen el módulo"          → verbo no observable
  "Entienden las ecuaciones"   → demasiado vago
  "El alumno calcula..."       → debe ser en plural (los estudiantes)
```

Verbos por nivel cognitivo (taxonomía de Bloom):
```
Recordar:    identifican, nombran, reconocen, listan, ubican
Comprender:  explican, describen, clasifican, resumen, interpretan
Aplicar:     calculan, resuelven, usan, demuestran, aplican
Analizar:    comparan, diferencian, relacionan, examinan, organizan
Evaluar:     juzgan, justifican, argumentan, defienden, evalúan
Crear:       diseñan, proponen, construyen, formulan, elaboran
```

### PASO 6 — Generar o completar el documento

```bash
# Completar un DOCX existente del colegio
python scripts/completar_planificacion.py \
    --input formato_planificacion.docx \
    --asignatura "Matemática" \
    --nivel "1° Medio"

# Generar planificación anual desde cero
python scripts/completar_planificacion.py \
    --tipo anual \
    --asignatura "Matemática" \
    --nivel "2° Medio" \
    --output planificacion_2M_mat.docx

# Generar unidad didáctica completa
python scripts/completar_planificacion.py \
    --tipo unidad \
    --asignatura "Matemática" \
    --nivel "3° Medio" \
    --unidad 1 \
    --output unidad1_3M_mat.docx
```

---

## Fuentes oficiales que el agente puede citar

- OA verificables en: https://www.curriculumnacional.cl/curriculum/
- Bases Curriculares: https://www.curriculumnacional.cl/Curriculum/Bases_Curriculares
- Programas de Estudio: https://www.curriculumnacional.cl/614/w3-propertyvalue-118605.html
- Priorización 2023-2025: https://www.curriculumnacional.cl/portal/Priorizacion-Curricular-2023-2025

---

## Instalación rápida

```bash
git clone https://github.com/oscraft2/skill-codex-claude.git
cd skill-codex-claude
pip install python-docx

# Subir el formato de tu colegio y ejecutar
python scripts/completar_planificacion.py \
    --input mi_formato.docx \
    --asignatura "Matemática" \
    --nivel "1° Medio"
```
