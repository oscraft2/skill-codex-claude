"""
generar_guia.py — Generador de guías de matemática estilo ISPM
Replica el formato exacto de la guía de referencia subida.

Uso:
    python generar_guia.py --tema "Ecuaciones Cuadráticas" --nivel "2° Medio" --numero 3
    python generar_guia.py --input mi_guia.json --output salida.docx

Requiere:
    pip install docx2python python-docx openai
    npm install -g docx
"""

import json
import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path

# ─── Configuración ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent
OA_PATH  = BASE_DIR / "oa_data" / "oa_matematica.json"
OUT_DIR  = BASE_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

# ─── Estructura de una guía ───────────────────────────────────────────────────

GUIA_TEMPLATE = {
    "institucion": "Instituto San Pablo Misionero",
    "departamento": "Departamento de Matemática",
    "numero": 1,
    "nivel": "4° Medio",
    "asignatura": "Matemática",
    "tema": "Números Complejos",
    "oa": ["OA1", "OA2"],
    "bloques": [
        {
            "titulo": "DEFINICIÓN",
            "teoria": "Texto de la teoría con definiciones y propiedades...",
            "ejemplos": [
                {
                    "numero": 1,
                    "enunciado": "¿Cuál de las siguientes expresiones es correcta?",
                    "alternativas": ["A) opción 1", "B) opción 2", "C) opción 3", "D) opción 4", "E) opción 5"],
                    "respuesta": "A"
                }
            ]
        }
    ],
    "soluciones": {"1": "A", "2": "B", "3": "C"}
}

# ─── Generador JS (docx-js) ───────────────────────────────────────────────────

def build_docx_js(guia: dict, output_path: str) -> str:
    """Genera el script JS que produce el .docx con formato ISPM."""

    bloques_js = []
    num_pregunta = 1

    for bloque in guia.get("bloques", []):
        teoria   = bloque.get("teoria", "").replace("`", "'").replace("\\", "\\\\")
        titulo_b = bloque.get("titulo", "").replace("`", "'")

        # Construir preguntas del bloque
        preguntas_js = []
        for ej in bloque.get("ejemplos", []):
            enunciado = ej.get("enunciado", "").replace("`", "'")
            alts = "\n".join([
                f'              new Paragraph({{ children: [new TextRun({{ text: `{a.replace("`","'")}`, size: 18, font: "Arial" }})] }})'
                for a in ej.get("alternativas", [])
            ])
            preguntas_js.append(f"""
            new Paragraph({{
              children: [new TextRun({{ text: `{num_pregunta}. {enunciado}`, bold: true, size: 18, font: "Arial" }})]
            }}),
{alts},
            new Paragraph({{ children: [new TextRun({{ text: " ", size: 10 }})] }}),""")
            num_pregunta += 1

        preguntas_str = "\n".join(preguntas_js)

        # Celda izquierda: teoría
        cell_left = f"""new TableCell({{
              width: {{ size: 4500, type: WidthType.DXA }},
              margins: {{ top: 100, bottom: 100, left: 150, right: 150 }},
              borders: {{
                top: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                bottom: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                left: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                right: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
              }},
              children: [
                new Paragraph({{
                  children: [new TextRun({{ text: `{titulo_b}`, bold: true, size: 20, font: "Arial", color: "1F3864" }})]
                }}),
                new Paragraph({{ children: [new TextRun({{ text: " ", size: 6 }})] }}),
                new Paragraph({{
                  children: [new TextRun({{ text: `{teoria}`, size: 18, font: "Arial" }})]
                }}),
              ]
            }})"""

        # Celda derecha: preguntas
        cell_right = f"""new TableCell({{
              width: {{ size: 4500, type: WidthType.DXA }},
              margins: {{ top: 100, bottom: 100, left: 150, right: 150 }},
              borders: {{
                top: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                bottom: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                left: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                right: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
              }},
              children: [
                new Paragraph({{
                  children: [new TextRun({{ text: "EJEMPLOS", bold: true, size: 20, font: "Arial", color: "1F3864" }})]
                }}),
                new Paragraph({{ children: [new TextRun({{ text: " ", size: 6 }})] }}),
{preguntas_str}
              ]
            }})"""

        bloques_js.append(f"""
        new Table({{
          width: {{ size: 9000, type: WidthType.DXA }},
          columnWidths: [4500, 4500],
          rows: [
            new TableRow({{
              children: [
                {cell_left},
                {cell_right},
              ]
            }})
          ]
        }}),
        new Paragraph({{ children: [new TextRun({{ text: " ", size: 8 }})] }}),""")

    # Tabla de soluciones
    sols = guia.get("soluciones", {})
    sols_filas = list(sols.items())
    # Agrupar de 6 en 6
    filas_sol = []
    for i in range(0, len(sols_filas), 6):
        grupo = sols_filas[i:i+6]
        celdas = " ".join([
            f'new TableCell({{ width: {{size: 1500, type: WidthType.DXA}}, margins: {{top:60,bottom:60,left:80,right:80}}, children: [new Paragraph({{ children: [new TextRun({{ text: `{k}. {v}`, size: 18, font: "Arial" }})] }})] }})'
            for k, v in grupo
        ])
        filas_sol.append(f"new TableRow({{ children: [{celdas}] }})")

    filas_sol_str = ",\n".join(filas_sol)

    tema      = guia.get("tema", "").replace("`", "'")
    nivel     = guia.get("nivel", "")
    numero    = guia.get("numero", 1)
    depto     = guia.get("departamento", "Departamento de Matemática")
    oa_list   = ", ".join(guia.get("oa", []))

    js_code = f"""
const {{
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign, PageNumber
}} = require('docx');
const fs = require('fs');

const doc = new Document({{
  sections: [{{
    properties: {{
      page: {{
        size: {{ width: 11906, height: 16838 }},
        margin: {{ top: 800, right: 900, bottom: 800, left: 900 }}
      }}
    }},
    children: [

      // ── Encabezado ─────────────────────────────────────────────
      new Paragraph({{
        alignment: AlignmentType.CENTER,
        children: [new TextRun({{ text: `{depto}`, bold: true, size: 26, font: "Arial", color: "1F3864" }})]
      }}),
      new Paragraph({{
        border: {{ bottom: {{ style: BorderStyle.SINGLE, size: 6, color: "2E74B5", space: 1 }} }},
        children: []
      }}),
      new Paragraph({{ children: [new TextRun({{ text: " ", size: 6 }})] }}),

      // ── Fila info (Nombre / Unidad) ─────────────────────────────
      new Table({{
        width: {{ size: 9000, type: WidthType.DXA }},
        columnWidths: [5400, 3600],
        rows: [
          new TableRow({{
            children: [
              new TableCell({{
                width: {{ size: 5400, type: WidthType.DXA }},
                borders: {{
                  top: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                  bottom: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                  left: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                  right: {{ style: BorderStyle.NONE, size: 0, color: "FFFFFF" }},
                }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{ children: [
                  new TextRun({{ text: "Nombre: ", bold: true, size: 18, font: "Arial" }}),
                  new TextRun({{ text: "________________________________________", size: 18, font: "Arial" }})
                ] }})]
              }}),
              new TableCell({{
                width: {{ size: 3600, type: WidthType.DXA }},
                borders: {{
                  top: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                  bottom: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                  left: {{ style: BorderStyle.NONE, size: 0, color: "FFFFFF" }},
                  right: {{ style: BorderStyle.SINGLE, size: 4, color: "2E74B5" }},
                }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{ children: [
                  new TextRun({{ text: "Unidad: ", bold: true, size: 18, font: "Arial" }}),
                  new TextRun({{ text: `{tema}`, size: 18, font: "Arial" }})
                ] }})]
              }}),
            ]
          }})
        ]
      }}),
      new Paragraph({{ children: [new TextRun({{ text: " ", size: 6 }})] }}),

      // ── Título guía ─────────────────────────────────────────────
      new Paragraph({{
        alignment: AlignmentType.CENTER,
        children: [new TextRun({{ text: `GUÍA N° {numero} — {tema} ({nivel})`, bold: true, size: 24, font: "Arial", color: "1F3864" }})]
      }}),
      new Paragraph({{
        alignment: AlignmentType.CENTER,
        children: [new TextRun({{ text: `OA: {oa_list}`, size: 18, font: "Arial", color: "595959" }})]
      }}),
      new Paragraph({{ children: [new TextRun({{ text: " ", size: 8 }})] }}),

      // ── Bloques teoría/ejercicios ────────────────────────────────
      {"".join(bloques_js)}

      // ── Tabla de soluciones ──────────────────────────────────────
      new Paragraph({{
        children: [new TextRun({{ text: "Soluciones:", bold: true, size: 18, font: "Arial", color: "1F3864" }})]
      }}),
      new Table({{
        width: {{ size: 9000, type: WidthType.DXA }},
        columnWidths: [1500, 1500, 1500, 1500, 1500, 1500],
        rows: [
          {filas_sol_str}
        ]
      }}),
    ]
  }}]
}});

Packer.toBuffer(doc).then(buf => {{
  fs.writeFileSync('{output_path}', buf);
  console.log('OK: {output_path}');
}}).catch(err => {{
  console.error('ERROR:', err.message);
  process.exit(1);
}});
"""
    return js_code


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generador de guías ISPM")
    parser.add_argument("--input",   help="JSON con estructura de la guía")
    parser.add_argument("--tema",    default="Números Complejos")
    parser.add_argument("--nivel",   default="4° Medio")
    parser.add_argument("--numero",  type=int, default=1)
    parser.add_argument("--output",  default="")
    args = parser.parse_args()

    # Cargar guía desde JSON o usar template
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            guia = json.load(f)
    else:
        guia = GUIA_TEMPLATE.copy()
        guia["tema"]   = args.tema
        guia["nivel"]  = args.nivel
        guia["numero"] = args.numero

    # Nombre de salida
    output_path = args.output or str(
        OUT_DIR / f"Guia_{guia['tema'].replace(' ','_')}_nº{guia['numero']}.docx"
    )

    # Generar JS temporal
    js_code = build_docx_js(guia, output_path)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js",
                                     delete=False, encoding="utf-8") as f:
        f.write(js_code)
        js_path = f.name

    # Ejecutar con Node.js
    result = subprocess.run(["node", js_path], capture_output=True, text=True)
    os.unlink(js_path)

    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Guía generada: {output_path}")


if __name__ == "__main__":
    main()
