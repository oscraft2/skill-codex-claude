# 📐 Guía Matemática Skill — Generador de Guías Estilo ISPM

> Genera guías de matemática (y cualquier asignatura) con formato profesional
> compatible con Microsoft Word, con simbología matemática real y
> alineadas a los OA del Ministerio de Educación de Chile.

---

## ✨ ¿Qué hace?

| Función | Descripción |
|---|---|
| 📋 Replica formato | Copia fielmente el layout de la guía de referencia ISPM |
| 📐 Simbología matemática | Fórmulas con caracteres Unicode y OMML (editables en Word) |
| 🎯 OA Mineduc | Etiqueta cada guía con los OA del currículum nacional |
| 🤖 Compatible con Claude y Codex | Funciona como skill en ambas plataformas |
| 📄 Salida Word | Archivo `.docx` listo para imprimir o editar |

---

## 🚀 Instalación rápida (3 pasos)

```bash
# 1. Clonar
git clone https://github.com/TU_USUARIO/guia-matematica-skill.git
cd guia-matematica-skill

# 2. Dependencias
pip install python-docx docx2python
npm install -g docx

# 3. ¡Generar!
python scripts/generar_guia.py --tema "Fracciones" --nivel "7° Básico" --numero 1
```

El archivo aparece en `output/Guia_Fracciones_nº1.docx` ✅

---

## 📁 Estructura del repositorio

```
guia-matematica-skill/
├── SKILL.md                    ← Instrucciones para Claude / Codex
├── README.md                   ← Este archivo
├── templates/
│   └── guia_referencia.docx   ← Guía original de referencia (formato ISPM)
├── oa_data/
│   └── oa_matematica.json     ← OA del Mineduc por nivel (7° Básico → 4° Medio)
├── scripts/
│   └── generar_guia.py        ← Script generador principal
└── output/                    ← Guías generadas (ignorado por git)
```

---

## 🎓 Formato generado

El layout replica exactamente la guía de referencia:

```
┌─────────────────────────────────────┐
│    Departamento de Matemática        │
├──────────────────┬──────────────────┤
│ Nombre: ________ │ Unidad: [Tema]   │
├──────────────────┴──────────────────┤
│         GUÍA N°X — Tema (Nivel)     │
│              OA: OA1, OA2           │
├──────────────────┬──────────────────┤
│  DEFINICIÓN      │  EJEMPLOS        │
│                  │  1. Pregunta...  │
│  Teoría,         │  A) opción       │
│  propiedades,    │  B) opción       │
│  fórmulas        │  C) opción       │
│                  │  D) opción       │
│                  │  E) opción       │
├──────────────────┴──────────────────┤
│  Soluciones: 1.A  2.B  3.C  4.D ... │
└─────────────────────────────────────┘
```

---

## 🤖 Usar con Claude (claude.ai)

1. Sube el `SKILL.md` a tu instalación de Claude Desktop / Cowork
2. Sube una guía ejemplo como referencia
3. Escribe: `"crea una guía de Ecuaciones Cuadráticas para 2° Medio, número 3"`

Claude genera el JSON estructurado y ejecuta el script automáticamente.

## 🤖 Usar con Codex / ChatGPT

1. Usa el contenido de `SKILL.md` como system prompt
2. Pide la guía en lenguaje natural
3. El modelo responde con el JSON y ejecuta el script vía Code Interpreter

---

## 📐 Simbología matemática

Las fórmulas se insertan usando:
- **Unicode directo**: `x²`, `√`, `∈`, `≠`, `π`, `∑`, `∫`
- **OMML**: para fracciones complejas y radicales anidados (editables en Word)

Ejemplo en el JSON:
```json
"teoria": "El módulo de z = a + bi es |z| = √(a² + b²)"
```

Se renderiza en Word con formato profesional tipográfico.

---

## 🗂 OA del Mineduc

El archivo `oa_data/oa_matematica.json` cubre:

| Nivel | OA disponibles |
|---|---|
| 7° Básico | Números enteros |
| 8° Básico | Potencias y propiedades |
| 1° Medio | Números racionales e irracionales |
| 2° Medio | Potencias de exponente racional |
| 3° Medio | Ecuaciones cuadráticas |
| 4° Medio | Números complejos |

Para agregar más OA o asignaturas, edita el JSON siguiendo el mismo esquema.

---

## 🔧 Opciones avanzadas

```bash
# Desde JSON personalizado
python scripts/generar_guia.py --input mi_guia.json

# Especificar nombre de salida
python scripts/generar_guia.py --tema "Vectores" --nivel "3° Medio" --output mi_guia.docx

# Ver ayuda
python scripts/generar_guia.py --help
```

---

## 📋 Requisitos

- Python 3.8+
- Node.js 16+
- `npm install -g docx`
- `pip install python-docx docx2python`

---

## 📄 Licencia

MIT — libre para uso educativo. Si lo adaptas para tu institución, ¡comparte la mejora!

---

*Desarrollado para el Instituto San Pablo Misionero (ISPM), Chile.*
*Compatible con el currículum Mineduc 2024.*
