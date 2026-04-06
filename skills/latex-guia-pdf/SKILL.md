---
name: latex-guia-pdf
version: 1.0.0
author: proscar.cl
description: >
  Genera guías de contenido matemático (o cualquier asignatura) en formato
  LaTeX profesional y las exporta automáticamente a PDF listo para imprimir.
  Compatible con Claude Code y Codex CLI. Pensado para profesores, investigadores
  y cualquier persona que necesite documentos con simbología matemática real.
triggers:
  - "haz una guía en latex"
  - "crea un apunte en latex"
  - "genera una prueba en latex"
  - "quiero un pdf con fórmulas"
  - "exporta a latex"
  - "genera un taller matemático"
  - "create a latex worksheet"
  - "generate math pdf"
compatibility: Claude Code, Codex CLI, Cursor, cualquier agente que ejecute Python
requires:
  - python3
  - pdflatex (texlive-latex-base)
---

# Skill: Generador de Guías LaTeX → PDF

## ¿Qué hace este skill?

Toma una descripción en lenguaje natural (o un JSON estructurado) y produce:

1. Un archivo `.tex` con fórmulas matemáticas **reales y editables** (no imágenes)
2. Un `.pdf` compilado, listo para imprimir o compartir

---

## Tipos de documento que genera

| Tipo | Código | Descripción |
|------|--------|-------------|
| Guía de ejercicios | `guia` | Selección múltiple A–E, dos columnas, tabla de soluciones |
| Apunte de contenido | `apunte` | Teoremas, definiciones, demostraciones |
| Evaluación / prueba | `prueba` | Mix selección + desarrollo, puntajes |
| Taller | `taller` | Ejercicios de desarrollo con espacio para respuestas |

---

## Instrucciones para el agente (Claude / Codex)

### PASO 1 — Entender la solicitud

Cuando el usuario pida un documento, extrae:

- **Tema**: (ej. "Límites y continuidad", "Vectores", "Ecuaciones diferenciales")
- **Nivel**: (ej. "4° Medio", "Primer año universitario", "Cálculo I")
- **Tipo**: guia / apunte / prueba / taller
- **Número de ejercicios**: cuántos pide el usuario
- **OA o estándar**: si menciona alguno (Mineduc, PAES, etc.)

### PASO 2 — Construir el JSON de la guía

Genera un JSON siguiendo esta estructura exacta:

```json
{
  "institucion":  "Nombre del colegio/universidad (o dejar vacío)",
  "departamento": "Departamento de Matemática",
  "tipo":         "guia",
  "numero":       1,
  "nivel":        "4° Medio",
  "asignatura":   "Matemática",
  "tema":         "Números Complejos",
  "fecha":        "2026",
  "codigo":       "MAT-NC-01",
  "oa":           ["FG-MATE-3M-OAC-01"],
  "bloques": [
    {
      "titulo": "DEFINICIÓN",
      "teoria": "Texto de teoría con LaTeX inline: $z = a + bi$\nFórmulas display:\n\\[\n  i^2 = -1\n\\]",
      "titulo_ejemplo": "Nombre del ejemplo",
      "ejemplo": "Contenido del ejemplo resuelto con LaTeX",
      "ejercicios": [
        {
          "enunciado": "El valor de $i^{100}$ es:",
          "alternativas": ["A) $1$", "B) $-1$", "C) $i$", "D) $-i$", "E) $0$"]
        }
      ]
    }
  ],
  "soluciones": { "1": "A", "2": "C" }
}
```

### PASO 3 — Reglas de escritura LaTeX en el JSON

El agente DEBE usar LaTeX válido en los campos `teoria`, `ejemplo` y `enunciado`:

```
Fórmula inline:    $x^2 + y^2 = r^2$
Fórmula display:   \[ \int_a^b f(x)\,dx = F(b) - F(a) \]
Fracciones:        \frac{numerador}{denominador}
Raíces:            \sqrt{x}  o  \sqrt[n]{x}
Sumatorias:        \sum_{i=1}^{n} a_i
Límites:           \lim_{x \to 0} \frac{\sin x}{x} = 1
Vectores:          \vec{v} = (a, b, c)
Matrices:          \begin{pmatrix} a & b \\ c & d \end{pmatrix}
Números reales:    \mathbb{R}
Módulo:            |z| = \sqrt{a^2 + b^2}
```

**IMPORTANTE:** En Python raw strings (r"..."), las barras invertidas no necesitan escaparse.
En strings normales, usa `\\` en lugar de `\` para comandos LaTeX.

### PASO 4 — Generar el documento

```bash
# Desde JSON:
python scripts/generar_latex.py --input mi_guia.json

# Ejemplo integrado:
python scripts/generar_latex.py --ejemplo

# Especificando parámetros:
python scripts/generar_latex.py --tema "Derivadas" --nivel "4° Medio" --tipo apunte
```

Los archivos se guardan en `output/`:
- `output/NombreTema_n1.tex` — fuente LaTeX editable en Overleaf o cualquier editor
- `output/NombreTema_n1.pdf` — PDF listo para imprimir

### PASO 5 — Verificar el PDF

Si la compilación falla, el agente debe:
1. Leer el archivo `.log` en `output/`
2. Identificar el error (línea que dice `! Error`)
3. Corregir el `.tex` y recompilar con:
   ```bash
   pdflatex -interaction=nonstopmode -output-directory=output output/archivo.tex
   ```

---

## Estructura de los paquetes LaTeX usados

El documento carga automáticamente:

| Paquete | Para qué sirve |
|---------|---------------|
| `amsmath`, `amssymb` | Fórmulas matemáticas avanzadas |
| `amsthm` | Teoremas, definiciones, lemas |
| `tcolorbox` | Cajas de teoría y ejemplos con color |
| `multicol` | Ejercicios en dos columnas |
| `enumitem` | Listas de alternativas A–E |
| `geometry` | Márgenes de página |
| `fancyhdr` | Encabezado y pie con institución/nivel |
| `lastpage` | Total de páginas en el pie |
| `hyperref` | Hipervínculos en el PDF |
| `xcolor` | Colores personalizados |
| `babel` (español) | Idioma y tipografía española |

---

## Compatibilidad con otros editores

El `.tex` generado es compatible con:
- **Overleaf** (online, sin instalar nada) — subir el `.tex` y compilar
- **TeXstudio**, **TeXworks**, **VS Code + LaTeX Workshop**
- **pdflatex**, **xelatex**, **lualatex**

---

## Instalación rápida

```bash
git clone https://github.com/oscraft2/skill-codex-claude.git
cd skill-codex-claude

# Instalar LaTeX (si no está)
# Ubuntu/Debian: sudo apt install texlive-latex-extra texlive-fonts-recommended
# macOS:         brew install --cask mactex
# Windows:       instalar MiKTeX desde miktex.org

# Generar el ejemplo de prueba
python scripts/generar_latex.py --ejemplo
# → output/Números_Complejos_n1.pdf  (137 KB)
```

---

## Contexto educativo chileno

Para guías del currículum Mineduc, usa los OA del archivo:
`oa_data/oa_matematica_1_4medio.json`

Los códigos son:
- `MA1M OA 01` ... `MA1M OA 15` → 1° Medio
- `MA2M OA 01` ... `MA2M OA 12` → 2° Medio
- `FG-MATE-3M-OAC-01` ... `04` → 3° Medio
- `FG-MATE-4M-OAC-01` ... `04` → 4° Medio
