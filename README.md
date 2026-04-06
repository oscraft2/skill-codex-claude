# skill-codex-claude

> Colección de skills para Claude Code, Codex CLI y cualquier agente compatible con el estándar open skills.  
> Desarrollado por **[proscar.cl](https://proscar.cl)** — herramientas de IA para el aula chilena.

📖 **[Wiki completa →](WIKI.md)** — Qué es una skill, cómo funciona, cómo crear una, FAQ y glosario.

---

## ¿Qué es una skill?

Una skill es un archivo `SKILL.md` que le dice al agente de IA cómo comportarse ante ciertos pedidos. Se instala en tu proyecto con un comando y el agente la detecta automáticamente sin configuración extra.

Compatible con: **Claude Code · Codex CLI · Cursor · Windsurf · cualquier agente que lea SKILL.md**

---

## Skills disponibles en este repositorio

### 1. `guia-matematica` — Generador de guías Word estilo ISPM

Genera guías de matemática en formato `.docx` con layout de dos columnas (teoría izquierda / ejercicios derecha), estilo PAES/SIMCE, tabla de soluciones y OA del Mineduc etiquetados automáticamente.

| | |
|---|---|
| **Formato de salida** | `.docx` editable en Word |
| **Fórmulas** | Texto Unicode + OMML (editables en Word) |
| **OA incluidos** | 1° a 4° Medio, códigos oficiales Mineduc |
| **Niveles** | 7° Básico → 4° Medio |
| **Asignaturas** | Matemática (extensible a cualquiera) |

**Instalar:**
```bash
npx skills add https://github.com/oscraft2/skill-codex-claude --skill guia-matematica
```

**Usar:**
```bash
python scripts/generar_guia.py --tema "Ecuaciones Cuadráticas" --nivel "2° Medio" --numero 3
python scripts/generar_guia.py --input mi_guia.json
```

---

### 2. `latex-guia-pdf` — Generador de documentos LaTeX → PDF

Genera guías, apuntes, pruebas y talleres en LaTeX con fórmulas matemáticas reales y editables (no imágenes). El `.tex` es compatible con Overleaf, pdflatex y xelatex.

| | |
|---|---|
| **Formato de salida** | `.tex` editable + `.pdf` compilado |
| **Fórmulas** | LaTeX nativo: `amsmath`, `amssymb`, `amsthm` |
| **Tipos de doc** | Guía · Apunte · Prueba · Taller |
| **Diseño** | Cajas tcolorbox azul/verde, alternativas A–E en fila horizontal |
| **Compilador** | xelatex local o Overleaf online (gratis) |

**Instalar:**
```bash
npx skills add https://github.com/oscraft2/skill-codex-claude --skill latex-guia-pdf
```

**Usar:**
```bash
# Generar el ejemplo incluido (Números Complejos 3° Medio)
python scripts/generar_latex.py --ejemplo

# Desde parámetros
python scripts/generar_latex.py --tema "Límites" --nivel "4° Medio" --tipo apunte

# Desde JSON con contenido completo
python scripts/generar_latex.py --input mi_guia.json
```

**Requisitos:**
```bash
# Ubuntu/Debian
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended

# macOS
brew install --cask mactex

# Sin instalar nada: sube el .tex a https://overleaf.com
```

---

### 3. `planificacion-curricular-chile` — Planificación curricular según Mineduc

Completa o genera documentos de planificación curricular según la normativa vigente del Ministerio de Educación de Chile. El profe sube su formato institucional y el skill lo llena con los OA oficiales, indicadores de evaluación y estructura de unidades.

| | |
|---|---|
| **Documentos** | Planificación anual · Red de contenidos · Unidad didáctica · Plan de clase |
| **OA** | 1° Básico → 4° Medio, todas las asignaturas |
| **Normativa** | Bases Curriculares Mineduc + Priorización 2023-2025 |
| **Formato de salida** | `.docx` con tabla profesional |
| **Indicadores** | Redactados con verbos Bloom observables |

**Instalar:**
```bash
npx skills add https://github.com/oscraft2/skill-codex-claude --skill planificacion-curricular-chile
```

**Usar:**
```bash
# Completar un formato Word de tu colegio
python scripts/completar_planificacion.py \
    --input mi_formato.docx \
    --asignatura "Matemática" \
    --nivel "1° Medio"

# Generar planificación anual desde cero
python scripts/completar_planificacion.py \
    --tipo anual \
    --asignatura "Matemática" \
    --nivel "2° Medio"
```

**Requisitos:**
```bash
pip install python-docx
```

---

## Instalación rápida (las 3 skills a la vez)

```bash
git clone https://github.com/oscraft2/skill-codex-claude.git
cd skill-codex-claude

# Dependencias Python
pip install python-docx

# Dependencias Node.js (para generar .docx con la skill 1)
npm install -g docx

# Dependencias LaTeX (para la skill 2)
# Ubuntu: sudo apt install texlive-xetex texlive-latex-extra
# macOS:  brew install --cask mactex
# O usa Overleaf online sin instalar nada
```

---

## Estructura del repositorio

```
skill-codex-claude/
│
├── SKILL.md                              ← skill 1: guia-matematica (raíz)
├── README.md
├── index.html                            ← directorio web de skills (GitHub Pages)
│
├── skills/
│   ├── latex-guia-pdf/
│   │   ├── SKILL.md                      ← skill 2: latex-guia-pdf
│   │   └── ejemplo_numeros_complejos.tex ← ejemplo de referencia
│   │
│   └── planificacion-curricular-chile/
│       └── SKILL.md                      ← skill 3: planificacion-curricular-chile
│
├── scripts/
│   ├── generar_guia.py                   ← generador .docx (skill 1)
│   ├── generar_latex.py                  ← generador .tex + .pdf (skill 2)
│   └── completar_planificacion.py        ← completador planificaciones (skill 3)
│
├── oa_data/
│   ├── oa_matematica_1_4medio.json       ← OA oficiales 1°-4° Medio (Mineduc)
│   └── oa_matematica.json                ← OA generales matemática
│
└── templates/
    └── guia_referencia.docx              ← plantilla formato ISPM
```

---

## Datos curriculares

Los OA están extraídos directamente de [curriculumnacional.cl](https://www.curriculumnacional.cl) con URL de verificación por cada objetivo:

| Nivel | Códigos | URL de verificación |
|-------|---------|-------------------|
| 1° Medio | `MA1M OA 01` → `MA1M OA 15` | [ver](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/matematica/1-medio) |
| 2° Medio | `MA2M OA 01` → `MA2M OA 12` | [ver](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/matematica/2-medio) |
| 3° Medio | `FG-MATE-3M-OAC-01` → `04` | [ver](https://www.curriculumnacional.cl/curriculum/3o-4o-medio/matematica-3o-medio/3-medio-fg) |
| 4° Medio | `FG-MATE-4M-OAC-01` → `04` | [ver](https://www.curriculumnacional.cl/curriculum/3o-4o-medio/matematica-4o-medio/4-medio-fg) |

---

## Contribuir

Si eres profe y quieres agregar OA de otra asignatura o un formato de planificación de tu colegio, abre un issue o un PR. El objetivo es que cualquier docente chileno pueda usar estas herramientas sin conocimientos técnicos.

---

## Licencia

MIT — libre para uso educativo. Si lo adaptas para tu institución, comparte la mejora.

---

*Desarrollado por [proscar.cl](https://proscar.cl) · Datos curriculares: [Mineduc Chile](https://www.curriculumnacional.cl)*
