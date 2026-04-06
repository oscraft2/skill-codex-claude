---
name: guia-matematica-universal
version: 1.0.0
author: Instituto San Pablo Misionero (ISPM)
description: >
  Skill para generar guías de matemática (y cualquier asignatura) en formato
  ISPM: dos columnas (teoría izquierda / ejercicios derecha), estilo Word
  profesional con simbología matemática OMML, tabla de soluciones al final.
  Compatible con Claude (claude.ai) y Codex/ChatGPT.
triggers:
  - "haz una guía de"
  - "crea una guía de"
  - "genera una guía"
  - "guía nº"
  - "worksheet de"
  - "make a worksheet"
  - "create a guide"
---

# Skill: Generador de Guías Estilo ISPM

## Descripción del formato de referencia

La guía de referencia (`templates/guia_referencia.docx`) define el formato institucional:

| Elemento | Especificación |
|---|---|
| Página | A4, márgenes 0.9cm laterales, 0.8cm superior/inferior |
| Encabezado | Logo + "Departamento de Matemática" en azul oscuro (`#1F3864`) |
| Fila de datos | Tabla 2 celdas: Nombre (línea) / Unidad |
| Cuerpo | Tabla de 2 columnas por bloque temático |
| Columna izquierda | Teoría, definiciones, fórmulas |
| Columna derecha | Preguntas de selección múltiple A–E |
| Pie | Tabla de soluciones numéricas |
| Fuente | Arial, teoría 9pt, enunciados 9pt |
| Colores | Azul oscuro `#1F3864` títulos, `#2E74B5` bordes |

## Instrucciones para el modelo (Claude / Codex)

### PASO 1 — Analizar la petición

Cuando el usuario pida una guía, extrae:
- **Tema**: (ej. "Ecuaciones Cuadráticas", "Fracciones", "Vectores")
- **Nivel**: 7° Básico → 4° Medio (o nivel equivalente si es otro país)
- **Asignatura**: Matemática, Física, Química, etc.
- **Número de guía**: (si lo indica)
- **OA relacionados**: busca en `oa_data/oa_matematica.json` (u otro JSON de OA)

### PASO 2 — Estructurar el contenido

Genera la guía siguiendo EXACTAMENTE esta estructura JSON:

```json
{
  "institucion": "Instituto San Pablo Misionero",
  "departamento": "Departamento de Matemática",
  "numero": 1,
  "nivel": "4° Medio",
  "asignatura": "Matemática",
  "tema": "Números Complejos",
  "oa": ["OA1", "OA2"],
  "bloques": [
    {
      "titulo": "DEFINICIÓN DE LA UNIDAD IMAGINARIA",
      "teoria": "El cuadrado de un número real siempre es no negativo. Por ejemplo, no existe ningún número real x para el cual x² = -1. Para remediar esta situación, introducimos un número llamado unidad imaginaria, que denotamos con i y cuyo cuadrado es -1.\n\ni² = -1\n\nPOTENCIAS DE i\ni¹ = i, i² = -1, i³ = -i, i⁴ = 1 (ciclo de período 4)",
      "ejemplos": [
        {
          "numero": 1,
          "enunciado": "¿Cuál(es) de las siguientes ecuaciones NO tiene solución en los números reales?\nI) x² + 9 = 0\nII) x⁴ + 16 = 0\nIII) x² - 25 = 0",
          "alternativas": ["A) Solo I", "B) Solo II", "C) Solo III", "D) Solo I y II", "E) I, II y III"],
          "respuesta": "D"
        },
        {
          "numero": 2,
          "enunciado": "El valor de i²³⁵ + i²⁹ es:",
          "alternativas": ["A) i + 1", "B) -1 + i", "C) 1 - i", "D) i", "E) 0"],
          "respuesta": "E"
        }
      ]
    }
  ],
  "soluciones": {
    "1": "D",
    "2": "E"
  }
}
```

### PASO 3 — Simbología matemática

Para fórmulas en el .docx generado, usa estas convenciones en el texto:

| Símbolo | En texto plano | En OMML (Word) |
|---|---|---|
| x² | `x²` (Unicode) | `<m:oMath>` con `<m:sup>` |
| √x | `√x` | `<m:rad>` |
| fracción a/b | `a/b` | `<m:f>` con `<m:num>` y `<m:den>` |
| ≠ | `≠` | Unicode directo |
| ∈ | `∈` | Unicode directo |
| i (imaginaria) | **i** (negrita) | `<m:r><m:rPr><m:b/></m:rPr>` |

> Para generación con Node.js `docx`, las fórmulas simples se insertan como
> texto Unicode enriquecido. Para fórmulas complejas, usar `xmlData` con OMML.

### PASO 4 — Generar el archivo

#### Opción A: Script Python (recomendado, usa Node.js internamente)
```bash
python scripts/generar_guia.py \
  --tema "Ecuaciones Cuadráticas" \
  --nivel "2° Medio" \
  --numero 3
```

#### Opción B: JSON directo
```bash
python scripts/generar_guia.py --input mi_guia.json
```

#### Opción C: Generación programática (para integrar en otro sistema)
```python
from scripts.generar_guia import build_docx_js, GUIA_TEMPLATE
import json

guia = {**GUIA_TEMPLATE, "tema": "Vectores", "nivel": "3° Medio"}
js = build_docx_js(guia, "output/guia_vectores.docx")
# ejecutar con subprocess node
```

### PASO 5 — OA del Mineduc

El archivo `oa_data/oa_matematica.json` contiene los OA oficiales por nivel.
Para cargarlos:
```python
import json
with open("oa_data/oa_matematica.json") as f:
    oa = json.load(f)

oa_nivel = oa["niveles"]["4° Medio"]["OA"]
# → lista de OA con código, descripción y temas
```

---

## Reglas de replicación de formato

El modelo DEBE respetar:

1. **Siempre tabla de 2 columnas** por bloque temático
2. **Siempre preguntas A–E** de selección múltiple (formato PAES/SIMCE)
3. **Siempre tabla de soluciones** al final con formato compacto
4. **Encabezado con "Departamento de Matemática"** centrado
5. **Fila Nombre / Unidad** después del encabezado
6. **Colores institucionales**: `#1F3864` y `#2E74B5`
7. **Mínimo 5 preguntas por bloque**, máximo 10
8. **Los OA cubiertos** deben aparecer en el encabezado de la guía

## Para otras asignaturas

El mismo script funciona para cualquier asignatura:
- Cambia `departamento` en el JSON
- Usa el JSON de OA correspondiente (o créalo siguiendo el mismo esquema)
- Las fórmulas de Física/Química se insertan igual con Unicode/OMML

---

## Instalación rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/guia-matematica-skill.git
cd guia-matematica-skill

# 2. Instalar dependencias
pip install python-docx docx2python
npm install -g docx

# 3. Generar primera guía
python scripts/generar_guia.py --tema "Fracciones" --nivel "7° Básico" --numero 1

# El archivo aparece en output/
```

## Compatibilidad

| Plataforma | Compatible |
|---|---|
| Claude (claude.ai) | ✅ Nativo vía skill |
| Codex / ChatGPT | ✅ Vía API + script |
| GitHub Codespaces | ✅ |
| Google Colab | ✅ (instalar Node.js) |
| Windows local | ✅ |
| macOS / Linux | ✅ |
