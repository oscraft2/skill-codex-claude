# Wiki · skill-codex-claude

> Documentación completa sobre el concepto de **skills** para agentes de IA (Claude, Codex CLI, Cursor, Windsurf, etc.) y cómo están implementados en este repositorio.

---

## Tabla de contenidos

1. [¿Qué es una skill y por qué existe?](#1-qué-es-una-skill-y-por-qué-existe)
2. [Cómo funciona técnicamente](#2-cómo-funciona-técnicamente)
3. [Anatomía de un archivo SKILL.md](#3-anatomía-de-un-archivo-skillmd)
4. [Skills disponibles en este repositorio](#4-skills-disponibles-en-este-repositorio)
5. [Cómo usar una skill con Claude o Codex](#5-cómo-usar-una-skill-con-claude-o-codex)
6. [Cómo crear una skill desde cero](#6-cómo-crear-una-skill-desde-cero)
7. [Arquitectura del repositorio](#7-arquitectura-del-repositorio)
8. [Datos curriculares (OA Mineduc)](#8-datos-curriculares-oa-mineduc)
9. [Preguntas frecuentes (FAQ)](#9-preguntas-frecuentes-faq)
10. [Glosario](#10-glosario)
11. [Contribuir](#11-contribuir)

---

## 1. ¿Qué es una skill y por qué existe?

### El problema

Claude, Codex y otros agentes de IA son generalistas: pueden escribir código, redactar textos, resolver matemáticas y mucho más. Pero para tareas muy específicas y repetitivas —como generar guías curriculares en el formato institucional de un colegio chileno— el usuario tendría que repetir cada vez las mismas instrucciones detalladas:

> *"Hazme una guía en formato Word de dos columnas, con teoría a la izquierda y ejercicios PAES a la derecha, con la tabla de soluciones al final, colores azul #1F3864, usando los OA del Mineduc para 2° Medio..."*

Esto es tedioso, propenso a errores y difícil de compartir con otros.

### La solución: skills

Una **skill** es un archivo de texto (`SKILL.md`) que encapsula todo ese conocimiento especializado de forma portable y reutilizable. El agente lee ese archivo una sola vez y luego entiende exactamente cómo debe comportarse ante ese tipo de pedido.

```
Usuario:  "haz una guía de Fracciones para 7° Básico"
Agente:   lee SKILL.md → genera guía en formato ISPM con OA correctos → entrega .docx
```

### Analogía

Una skill es como una **receta de cocina**:  
- La receta (SKILL.md) define exactamente los ingredientes y los pasos.  
- El cocinero (el agente IA) ejecuta la receta con los ingredientes que tú le das (tu pedido).  
- El resultado es siempre consistente, sin importar quién haga el pedido.

---

## 2. Cómo funciona técnicamente

### Flujo general

```
┌──────────────────────────────────────────────────┐
│  REPOSITORIO / PROYECTO                          │
│                                                  │
│  SKILL.md  ←── el agente lo lee al iniciar      │
│  scripts/  ←── herramientas que ejecuta el agente│
│  oa_data/  ←── datos curriculares de referencia  │
└──────────────────────────────────────────────────┘
         ▼
┌──────────────────────────────────────────────────┐
│  AGENTE IA (Claude Code / Codex CLI)             │
│                                                  │
│  1. Detecta SKILL.md en el directorio            │
│  2. Carga las instrucciones y los triggers       │
│  3. Espera un mensaje del usuario                │
│  4. Si el mensaje coincide con un trigger →      │
│     activa el comportamiento definido en SKILL   │
│  5. Ejecuta los pasos: genera JSON, corre script │
│  6. Entrega el archivo final al usuario          │
└──────────────────────────────────────────────────┘
```

### Detección automática

Claude Code y Codex CLI buscan automáticamente un archivo `SKILL.md` en:
1. La raíz del repositorio actual
2. El directorio `.claude/` (para Claude Code)
3. Los directorios especificados con `--skill-dir`

No se necesita configuración extra: si el archivo existe, la skill está activa.

### Múltiples skills

Un repositorio puede tener varias skills en subdirectorios:

```
mi-proyecto/
├── SKILL.md                           ← skill principal (raíz)
└── skills/
    ├── skill-secundaria-1/
    │   └── SKILL.md
    └── skill-secundaria-2/
        └── SKILL.md
```

---

## 3. Anatomía de un archivo SKILL.md

Un archivo `SKILL.md` tiene dos partes: un **frontmatter YAML** con metadatos y el **cuerpo Markdown** con las instrucciones para el agente.

### Estructura completa

```markdown
---
name: nombre-de-la-skill
version: 1.0.0
author: nombre-del-autor
description: >
  Descripción corta de qué hace esta skill.
triggers:
  - "frase que activa la skill"
  - "otra frase activadora"
  - "english trigger too"
compatibility: Claude Code, Codex CLI, Cursor
requires:
  - python3
  - paquete-necesario
---

# Título de la skill

## Descripción
...

## Instrucciones para el agente

### PASO 1 — ...
### PASO 2 — ...
### PASO N — ...

## Instalación rápida
...
```

### Campos del frontmatter

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| `name` | ✅ | Identificador único, en kebab-case, sin espacios |
| `version` | ✅ | Versión semántica (`MAJOR.MINOR.PATCH`) |
| `author` | ✅ | Nombre o URL del autor |
| `description` | ✅ | Resumen en 2-3 líneas de qué hace la skill |
| `triggers` | ✅ | Lista de frases que activan la skill (en español e inglés) |
| `compatibility` | ➖ | Agentes compatibles |
| `requires` | ➖ | Dependencias externas (Python, Node.js, LaTeX, etc.) |

### Buenas prácticas para los triggers

Los triggers son frases parciales que el agente detecta en el mensaje del usuario. Deben:
- Ser lo suficientemente específicos para no activarse accidentalmente
- Incluir variantes en español e inglés
- Cubrir distintas formas de pedir lo mismo

```yaml
# ✅ Bien: específicos y variados
triggers:
  - "haz una guía de"
  - "crea una guía de"
  - "genera una guía"
  - "make a worksheet"

# ❌ Mal: demasiado genérico
triggers:
  - "haz"
  - "crea"
```

### Cuerpo de instrucciones

El cuerpo define cómo debe comportarse el agente. Conviene estructurarlo en **pasos numerados** (`PASO 1`, `PASO 2`, ...) para que el agente los siga en orden:

1. **Analizar el pedido** — qué extrae del mensaje del usuario
2. **Estructurar el contenido** — cómo organiza los datos (usualmente en JSON)
3. **Generar el archivo** — qué script ejecuta y con qué parámetros
4. **Verificar el resultado** — cómo confirma que todo salió bien

---

## 4. Skills disponibles en este repositorio

### Skill 1: `guia-matematica` (raíz)

**Archivo:** `SKILL.md` en la raíz del repositorio  
**Script:** `scripts/generar_guia.py`  
**Salida:** `.docx` editable en Microsoft Word

Genera guías de matemática (o cualquier asignatura) en formato ISPM:
- Diseño de **dos columnas**: teoría a la izquierda, ejercicios a la derecha
- Preguntas de **selección múltiple A–E** (estilo PAES/SIMCE)
- **Tabla de soluciones** al final
- Fórmulas matemáticas con **Unicode + OMML** (editables en Word)
- OA del Mineduc etiquetados automáticamente

| Propiedad | Valor |
|-----------|-------|
| Niveles | 7° Básico → 4° Medio |
| Asignaturas | Matemática (extensible) |
| Formato | `.docx` editable |
| Dependencias | `python-docx`, Node.js `docx` |

**Ejemplo de uso:**
```bash
# El agente recibe: "haz una guía de Ecuaciones Cuadráticas para 2° Medio"
python scripts/generar_guia.py --tema "Ecuaciones Cuadráticas" --nivel "2° Medio" --numero 3
# → output/Ecuaciones_Cuadraticas_n3.docx
```

---

### Skill 2: `latex-guia-pdf`

**Archivo:** `skills/latex-guia-pdf/SKILL.md`  
**Script:** `scripts/generar_latex.py`  
**Salida:** `.tex` editable + `.pdf` compilado

Genera documentos académicos con **fórmulas matemáticas reales** (no imágenes) usando LaTeX:
- Tipos: guía, apunte, prueba, taller
- Diseño con cajas **tcolorbox** de colores
- Compatible con **Overleaf** (sin instalar nada), pdflatex y xelatex
- Paquetes incluidos: `amsmath`, `amssymb`, `amsthm`, `tcolorbox`, `multicol`

| Propiedad | Valor |
|-----------|-------|
| Niveles | 7° Básico → universidad |
| Asignaturas | Cualquiera con fórmulas |
| Formato | `.tex` + `.pdf` |
| Dependencias | `texlive-xetex` o MiKTeX (o Overleaf online) |

**Ejemplo de uso:**
```bash
# El agente recibe: "quiero un pdf con fórmulas de Límites para 4° Medio"
python scripts/generar_latex.py --tema "Límites" --nivel "4° Medio" --tipo apunte
# → output/Limites_n1.tex  +  output/Limites_n1.pdf
```

---

### Skill 3: `planificacion-curricular-chile`

**Archivo:** `skills/planificacion-curricular-chile/SKILL.md`  
**Script:** `scripts/completar_planificacion.py`  
**Salida:** `.docx` con planificación completa

Completa o genera documentos de planificación curricular según la normativa del Mineduc:
- Tipos: planificación anual, red de contenidos, unidad didáctica, plan de clase
- OA oficiales para **todas las asignaturas y niveles** (1° Básico → 4° Medio)
- Indicadores redactados con verbos Bloom observables
- Respeta la Priorización Curricular 2023-2025

| Propiedad | Valor |
|-----------|-------|
| Niveles | 1° Básico → 4° Medio |
| Asignaturas | Matemática, Lenguaje, Historia, Ciencias y más |
| Formato | `.docx` institucional |
| Dependencias | `python-docx` |

**Ejemplo de uso:**
```bash
# El agente recibe: "haz una planificación anual de Matemática para 1° Medio"
python scripts/completar_planificacion.py --tipo anual --asignatura "Matemática" --nivel "1° Medio"
# → planificacion_1M_matematica.docx
```

---

## 5. Cómo usar una skill con Claude o Codex

### Con Claude Code (recomendado)

Claude Code detecta `SKILL.md` automáticamente al abrir un directorio:

```bash
# 1. Clonar el repositorio
git clone https://github.com/oscraft2/skill-codex-claude.git
cd skill-codex-claude

# 2. Abrir Claude Code en este directorio
claude .

# 3. Hablar naturalmente
# Claude ya tiene cargada la skill y responde a los triggers
```

### Con Codex CLI

```bash
# 1. Instalar Codex CLI
npm install -g @openai/codex

# 2. Navegar al directorio con la skill
cd skill-codex-claude

# 3. Ejecutar con contexto de la skill
codex "haz una guía de Vectores para 3° Medio"
```

### Con cualquier agente (modo manual)

Si tu agente no detecta `SKILL.md` automáticamente, puedes copiar y pegar el contenido del archivo directamente en el chat como contexto del sistema:

```
[Copia aquí el contenido de SKILL.md]

---

Usuario: haz una guía de Fracciones para 7° Básico
```

### Instalar una skill específica con npx

```bash
# Solo la skill de guías matemáticas
npx skills add https://github.com/oscraft2/skill-codex-claude --skill guia-matematica

# Solo la skill de LaTeX
npx skills add https://github.com/oscraft2/skill-codex-claude --skill latex-guia-pdf

# Solo la skill de planificaciones
npx skills add https://github.com/oscraft2/skill-codex-claude --skill planificacion-curricular-chile
```

---

## 6. Cómo crear una skill desde cero

### Paso 1: Identificar el caso de uso

Define claramente:
- **¿Qué tarea repetitiva resuelve?** (ej: "generar informes de notas en PDF")
- **¿Qué entra?** (ej: "lista de alumnos con notas")
- **¿Qué sale?** (ej: ".pdf con informe por alumno")
- **¿Qué herramientas usa?** (Python, Node.js, LaTeX, etc.)

### Paso 2: Crear la estructura de directorios

```bash
mkdir -p skills/mi-nueva-skill
touch skills/mi-nueva-skill/SKILL.md
mkdir -p scripts
```

### Paso 3: Escribir el frontmatter

```yaml
---
name: mi-nueva-skill
version: 1.0.0
author: mi-nombre
description: >
  Descripción de qué hace esta skill en 2-3 líneas.
  Qué entra, qué sale, para quién es útil.
triggers:
  - "frase específica que pide esto"
  - "otra forma de pedirlo"
  - "english version too"
compatibility: Claude Code, Codex CLI
requires:
  - python3
  - librería-necesaria
---
```

### Paso 4: Escribir las instrucciones

Estructura el cuerpo en pasos claros. El agente los seguirá en orden:

```markdown
# Skill: Mi Nueva Skill

## Instrucciones para el agente

### PASO 1 — Analizar el pedido
Cuando el usuario pida X, extrae:
- **Campo A**: descripción
- **Campo B**: descripción

### PASO 2 — Estructurar el contenido
Genera un JSON con esta estructura:
\`\`\`json
{
  "campo_a": "valor",
  "campo_b": "valor"
}
\`\`\`

### PASO 3 — Ejecutar el script
\`\`\`bash
python scripts/mi_script.py --input datos.json
\`\`\`

### PASO 4 — Verificar el resultado
Confirma que el archivo se generó en `output/` y muéstraselo al usuario.
```

### Paso 5: Escribir el script correspondiente

```python
# scripts/mi_script.py
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output/resultado.pdf")
    args = parser.parse_args()

    datos = json.loads(Path(args.input).read_text(encoding="utf-8"))
    # ... lógica de generación ...
    print(f"✅ Archivo generado: {args.output}")

if __name__ == "__main__":
    main()
```

### Paso 6: Probar la skill

```bash
# Prueba directa del script
python scripts/mi_script.py --input ejemplo.json

# Prueba con el agente
claude .
# → "frase específica que pide esto para nivel X"
```

### Paso 7: Agregar al README y al índice

Documenta tu nueva skill en `README.md` siguiendo el mismo formato que las existentes, y si tienes `index.html`, agrégala también al directorio web.

---

## 7. Arquitectura del repositorio

```
skill-codex-claude/
│
├── SKILL.md                              ← Skill 1: guia-matematica (activa en raíz)
├── README.md                             ← Documentación principal del repositorio
├── WIKI.md                               ← Este archivo: documentación extendida
├── index.html                            ← Directorio web (GitHub Pages)
│
├── skills/
│   ├── latex-guia-pdf/
│   │   ├── SKILL.md                      ← Skill 2: latex-guia-pdf
│   │   └── ejemplo_numeros_complejos.tex ← Archivo .tex de referencia
│   │
│   └── planificacion-curricular-chile/
│       └── SKILL.md                      ← Skill 3: planificacion-curricular-chile
│
├── scripts/
│   ├── generar_guia.py                   ← Genera .docx estilo ISPM (Skill 1)
│   ├── generar_latex.py                  ← Genera .tex + .pdf (Skill 2)
│   └── completar_planificacion.py        ← Completa planificaciones (Skill 3)
│
├── oa_data/
│   ├── oa_matematica_1_4medio.json       ← OA oficiales 1°–4° Medio con URLs
│   └── oa_matematica.json                ← OA generales de Matemática
│
├── templates/
│   └── guia_referencia.docx              ← Plantilla de referencia formato ISPM
│
└── ejemplos/
    └── guia_numeros_complejos_ejemplo.pdf ← PDF de ejemplo generado con la Skill 2
```

### Relación entre componentes

```
Usuario
  │
  ▼
SKILL.md ──────► define qué espera el agente y cómo responder
  │
  ▼
Agente IA ──────► interpreta el pedido según las instrucciones del SKILL.md
  │
  ├──► oa_data/*.json        (consulta OA curriculares)
  │
  └──► scripts/*.py          (ejecuta la herramienta de generación)
           │
           ├──► templates/   (usa plantillas base)
           │
           └──► output/      (deposita el archivo final)
```

---

## 8. Datos curriculares (OA Mineduc)

Las skills de este repositorio están alineadas con el **Currículum Nacional de Chile**. Los Objetivos de Aprendizaje (OA) son extraídos de [curriculumnacional.cl](https://www.curriculumnacional.cl) y almacenados en `oa_data/`.

### Estructura de los archivos de OA

```json
{
  "asignatura": "Matemática",
  "niveles": {
    "1° Medio": {
      "base_curricular": "Bases Curriculares 2015",
      "OA": [
        {
          "codigo": "MA1M OA 01",
          "descripcion": "Representar y operar con números reales...",
          "eje": "Números",
          "url": "https://www.curriculumnacional.cl/..."
        }
      ]
    }
  }
}
```

### Tabla de códigos por nivel (Matemática)

| Nivel | Códigos | Base curricular |
|-------|---------|----------------|
| 1° Básico | `MA01 OA 01` → `MA01 OA XX` | BC 2012 |
| 2° Básico | `MA02 OA 01` → `MA02 OA XX` | BC 2012 |
| 3° Básico | `MA03 OA 01` → `MA03 OA XX` | BC 2012 |
| 4° Básico | `MA04 OA 01` → `MA04 OA XX` | BC 2012 |
| 5° Básico | `MA05 OA 01` → `MA05 OA XX` | BC 2012 |
| 6° Básico | `MA06 OA 01` → `MA06 OA XX` | BC 2012 |
| 7° Básico | `MA07 OA 01` → `MA07 OA 19` | BC 2015 |
| 8° Básico | `MA08 OA 01` → `MA08 OA XX` | BC 2015 |
| 1° Medio | `MA1M OA 01` → `MA1M OA 15` | BC 2015 |
| 2° Medio | `MA2M OA 01` → `MA2M OA 12` | BC 2015 |
| 3° Medio FG | `FG-MATE-3M-OAC-01` → `04` | BC 2019 |
| 4° Medio FG | `FG-MATE-4M-OAC-01` → `04` | BC 2019 |

### Verificación de OA

Cada OA en los archivos JSON incluye su URL de verificación oficial en `curriculumnacional.cl`. Esto permite auditar que los OA usados por el agente sean los correctos y estén vigentes.

---

## 9. Preguntas frecuentes (FAQ)

**¿Necesito saber programar para usar las skills?**  
No. Solo necesitas tener instalado Python 3 y las dependencias indicadas (`pip install python-docx`). El agente IA ejecuta los scripts por ti.

**¿Funciona con ChatGPT?**  
Sí, pero de forma semi-manual: copia el contenido de `SKILL.md` y pégalo como contexto del sistema (system prompt) antes de hacer tu pedido.

**¿Puedo usar las skills para asignaturas que no sean Matemática?**  
Sí. Los scripts de generación de guías y LaTeX aceptan cualquier asignatura. Para los OA, la Skill 3 (planificaciones) soporta todas las asignaturas del currículum chileno.

**¿Qué pasa si no tengo LaTeX instalado?**  
La Skill 2 genera el archivo `.tex`. Puedes subirlo a [Overleaf](https://overleaf.com) (gratuito) para compilarlo a PDF sin instalar nada.

**¿Los documentos generados son editables?**  
Sí. Los `.docx` se abren y editan en Word, LibreOffice o Google Docs. Los `.tex` se editan en cualquier editor de texto o en Overleaf.

**¿Puedo cambiar el logo o el nombre del colegio?**  
Sí. En el JSON que genera el agente, cambia el campo `institucion` y `departamento`. Para el logo, edita la plantilla `templates/guia_referencia.docx`.

**¿Las skills funcionan sin conexión a internet?**  
Sí, una vez descargado el repositorio. Los scripts y los datos de OA son locales. Solo se necesita internet para que el agente IA procese tu pedido.

**¿Puedo agregar más skills?**  
Claro. Crea una carpeta en `skills/`, agrega tu `SKILL.md` y el script correspondiente, y documéntalo en el README. Ver [sección 6](#6-cómo-crear-una-skill-desde-cero).

**¿Puedo usar estas skills en otros países?**  
Las skills de generación de guías (1 y 2) son universales. La skill 3 (planificaciones) es específica del currículum chileno, pero puedes adaptarla cargando OA de otro país en el mismo formato JSON.

**¿Hay una API?**  
No hay API separada. Las skills se usan directamente con el agente IA en tu entorno local o en Claude.ai con archivos adjuntos.

---

## 10. Glosario

| Término | Definición |
|---------|-----------|
| **Skill** | Archivo `SKILL.md` que instruye al agente cómo comportarse ante un tipo específico de pedido |
| **Trigger** | Frase o palabra clave que activa una skill cuando aparece en el mensaje del usuario |
| **Frontmatter** | Bloque YAML al inicio del `SKILL.md` con metadatos (nombre, versión, triggers, etc.) |
| **OA** | Objetivo de Aprendizaje. Unidad básica del currículum nacional chileno |
| **PAES** | Prueba de Acceso a la Educación Superior. Reemplazó a la PSU en 2022 |
| **SIMCE** | Sistema de Medición de la Calidad de la Educación. Evaluación nacional chilena |
| **ISPM** | Instituto San Pablo Misionero. Institución de referencia para el formato de guías |
| **Bloom** | Taxonomía de objetivos educativos (Recordar → Comprender → Aplicar → Analizar → Evaluar → Crear) |
| **OMML** | Office Math Markup Language. Formato de fórmulas nativo de Microsoft Word |
| **tcolorbox** | Paquete LaTeX para crear cajas de colores con contenido matemático |
| **Priorización curricular** | Clasificación de OA en basales y complementarios vigente 2023-2025 en Chile |
| **Agente IA** | Programa que combina un modelo de lenguaje con herramientas para ejecutar tareas autónomamente |
| **Claude Code** | Herramienta de línea de comandos de Anthropic para usar Claude en proyectos de código |
| **Codex CLI** | Herramienta de línea de comandos de OpenAI para usar modelos GPT en proyectos |

---

## 11. Contribuir

### ¿Cómo puedo contribuir?

- **Agregar OA de otras asignaturas**: crea un JSON en `oa_data/` siguiendo el mismo esquema
- **Agregar formatos de planificación**: sube tu `.docx` institucional como plantilla
- **Crear una nueva skill**: ver [sección 6](#6-cómo-crear-una-skill-desde-cero)
- **Reportar errores en OA**: abre un issue con el OA incorrecto y la fuente correcta

### Cómo abrir un Pull Request

```bash
# 1. Fork del repositorio en GitHub
# 2. Clonar tu fork
git clone https://github.com/TU_USUARIO/skill-codex-claude.git
cd skill-codex-claude

# 3. Crear una rama para tu contribución
git checkout -b feat/mi-nueva-skill

# 4. Hacer los cambios
# ...

# 5. Commit y push
git add .
git commit -m "feat: agregar skill para informes de notas"
git push origin feat/mi-nueva-skill

# 6. Abrir un Pull Request en GitHub
```

### Convenciones de commit

```
feat:     nueva funcionalidad o skill
fix:      corrección de error
docs:     cambios en documentación
data:     actualización de datos curriculares (OA)
style:    cambios de formato sin afectar la lógica
```

### Criterios para aceptar una skill

1. El `SKILL.md` tiene frontmatter completo (name, version, author, description, triggers)
2. Los triggers son específicos y no generan falsos positivos
3. Las instrucciones están en pasos numerados claros
4. El script correspondiente funciona con `python3` y dependencias estándar
5. Hay al menos un ejemplo de uso documentado

---

*Desarrollado por [proscar.cl](https://proscar.cl) · Datos curriculares: [Mineduc Chile](https://www.curriculumnacional.cl)*
