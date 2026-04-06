#!/usr/bin/env python3
"""
generar_latex.py — Generador de documentos LaTeX para profesores
Autor: proscar.cl · https://github.com/oscraft2/skill-codex-claude

Uso:
    python scripts/generar_latex.py --ejemplo
    python scripts/generar_latex.py --tema "Límites" --nivel "4° Medio"
    python scripts/generar_latex.py --input mi_guia.json

Requiere: xelatex (texlive-xetex) — o sube el .tex a Overleaf gratis
"""
import json, sys, subprocess, argparse, shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUT_DIR  = BASE_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

LETRAS = ["A","B","C","D","E"]

# ── Ejemplo integrado ────────────────────────────────────────────────────────
EJEMPLO = {
    "institucion":  "",
    "departamento": "Departamento de Matemática",
    "tipo":         "guia",
    "numero":       1,
    "nivel":        "3° Medio",
    "asignatura":   "Matemática",
    "tema":         "Números Complejos",
    "fecha":        "2026",
    "oa":           ["FG-MATE-3M-OAC-01"],
    "bloques": [
        {
            "titulo": r"UNIDAD IMAGINARIA Y POTENCIAS DE $i$",
            "teoria": (
                r"No existe ningún número real $x$ tal que $x^2 = -1$. "
                r"Definimos la \textbf{unidad imaginaria} $i$:"
                "\n" r"\[ i^2 = -1 \qquad i = \sqrt{-1} \]" "\n\n"
                r"\textbf{Ciclo de potencias (período 4):}"
                "\n" r"\[ i^1=i,\quad i^2=-1,\quad i^3=-i,\quad i^4=1 \]" "\n"
                r"En general $i^{4k}=1$ para todo $k\in\mathbb{Z}$."
            ),
            "titulo_ejemplo": "Ejemplo resuelto",
            "ejemplo": (
                r"Calcular $i^{235}$.\newline "
                r"$235 = 4\cdot 58 + 3 \Rightarrow i^{235} = i^3 = -i$"
            ),
            "ejercicios": [
                {"enunciado": r"El valor de $i^{100}$ es:",
                 "alternativas": [r"$1$", r"$-1$", r"$i$", r"$-i$", r"$0$"]},
                {"enunciado": r"La expresión $i+i^2+i^3+i^4$ equivale a:",
                 "alternativas": [r"$4i$", r"$1$", r"$0$", r"$-1$", r"$4$"]},
                {"enunciado": r"Si $n$ es múltiplo de 4, entonces $i^n$ es:",
                 "alternativas": [r"$i$", r"$-i$", r"$-1$", r"$1$", r"$0$"]},
            ]
        },
        {
            "titulo": r"NÚMERO COMPLEJO $z = a + bi$",
            "teoria": (
                r"Un número $z = a+bi$ con $a,b\in\mathbb{R}$ es un \textbf{número complejo}."
                "\n\n"
                r"\begin{itemize}[leftmargin=1.5em]" "\n"
                r"  \item $\operatorname{Re}(z)=a$\ (parte real)" "\n"
                r"  \item $\operatorname{Im}(z)=b$\ (parte imaginaria)" "\n"
                r"  \item $|z|=\sqrt{a^2+b^2}$\ (módulo)" "\n"
                r"  \item $\bar{z}=a-bi$\ (conjugado)" "\n"
                r"\end{itemize}"
            ),
            "titulo_ejemplo": "Ejemplo resuelto",
            "ejemplo": (
                r"Sea $z=3+4i$. Calcular $|z|$."
                "\n" r"\[ |z|=\sqrt{3^2+4^2}=\sqrt{25}=5 \]"
            ),
            "ejercicios": [
                {"enunciado": r"La parte imaginaria de $z = 1-2i$ es:",
                 "alternativas": [r"$-2i$", r"$1$", r"$-2$", r"$2$", r"$-1$"]},
                {"enunciado": r"Si $z=5+12i$, entonces $|z|$ es:",
                 "alternativas": [r"$17$", r"$13$", r"$\sqrt{119}$", r"$169$", r"$7$"]},
                {"enunciado": r"El conjugado de $z=-3+7i$ es:",
                 "alternativas": [r"$3+7i$", r"$-3-7i$", r"$3-7i$", r"$-7+3i$", r"$7-3i$"]},
            ]
        },
        {
            "titulo": "OPERACIONES CON COMPLEJOS",
            "teoria": (
                r"Sean $z_1=a+bi$ y $z_2=c+di$:" "\n\n"
                r"\textbf{Adición:} $z_1+z_2=(a+c)+(b+d)i$" "\n\n"
                r"\textbf{Multiplicación:}"
                "\n" r"\[ z_1\cdot z_2=(ac-bd)+(ad+bc)i \]" "\n\n"
                r"\textbf{División} (amplificar por el conjugado):"
                "\n" r"\[ \frac{z_1}{z_2}=\frac{z_1\cdot\bar{z}_2}{|z_2|^2} \]"
            ),
            "titulo_ejemplo": "Ejemplo resuelto",
            "ejemplo": (
                r"Calcular $(2+3i)(1-i)$."
                "\n" r"\[ (2+3i)(1-i)=2-2i+3i-3i^2=2+i+3=5+i \]"
            ),
            "ejercicios": [
                {"enunciado": r"Si $u=2+3i$ y $v=-5+4i$, entonces $u+v$ es:",
                 "alternativas": [r"$-3+7i$", r"$3+7i$", r"$-3-7i$", r"$7-3i$", r"$2+4i$"]},
                {"enunciado": r"El producto $(1+i)(1-i)$ es:",
                 "alternativas": [r"$0$", r"$2i$", r"$2$", r"$-2$", r"$1+2i$"]},
                {"enunciado": r"El valor de $\dfrac{1}{i}$ es:",
                 "alternativas": [r"$1$", r"$i$", r"$-i$", r"$-1$", r"$0$"]},
            ]
        }
    ],
    "soluciones": {
        "1":"A","2":"C","3":"D",
        "4":"C","5":"B","6":"B",
        "7":"A","8":"C","9":"C"
    }
}


def alternativas_latex(alts: list) -> str:
    """
    Genera alternativas A–E en UNA sola fila horizontal.
    Usa minipage para que quepan en el ancho disponible.
    Esto funciona tanto dentro como fuera de multicols.
    """
    n = len(alts)
    if n == 0:
        return ""
    # Ancho de cada minipage: dividimos el 98% del linewidth
    ancho = f"{0.98/n:.3f}"
    linea = r"\noindent"
    for i, alt in enumerate(alts):
        letra = LETRAS[i] if i < len(LETRAS) else str(i+1)
        linea += (
            rf"\begin{{minipage}}{{{ancho}\linewidth}}"
            rf"\textbf{{{letra})}}\ {alt}"
            r"\end{minipage}"
        )
    linea += "\n"
    return linea


def build_latex(g: dict) -> str:
    dept  = g.get("departamento", "Departamento de Matemática")
    tipo  = g.get("tipo", "guia").capitalize()
    num   = g.get("numero", 1)
    nivel = g.get("nivel", "")
    asig  = g.get("asignatura", "Matemática")
    tema  = g.get("tema", "")
    fecha = g.get("fecha", "2026")
    inst  = g.get("institucion", "")
    oas   = ", ".join(g.get("oa", []))

    # ── Preámbulo ─────────────────────────────────────────────────────────────
    pre = r"""\documentclass[11pt,a4paper]{article}

%% Motor: xelatex (o sube el .tex a overleaf.com)
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{spanish}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{hyperref}
\usepackage{booktabs}

\geometry{top=2cm,bottom=2.2cm,left=2cm,right=2cm}

%% Colores
\definecolor{azulp}{RGB}{0,90,160}
\definecolor{azulc}{RGB}{220,235,250}
\definecolor{verde}{RGB}{0,130,90}
\definecolor{grisf}{RGB}{248,248,248}
\definecolor{gris}{gray}{0.5}

%% Cajas tcolorbox
\tcbuselibrary{skins,breakable}
\newtcolorbox{cajat}[1][Teoría]{enhanced,breakable,
  colback=azulc,colframe=azulp,
  fonttitle=\bfseries\color{white},coltitle=white,
  attach boxed title to top left={yshift=-2mm,xshift=4mm},
  boxed title style={colback=azulp},
  title={#1},arc=4pt,boxrule=0.8pt,
  left=6pt,right=6pt,top=6pt,bottom=6pt}

\newtcolorbox{cajae}[1][Ejemplo resuelto]{enhanced,breakable,
  colback=grisf,colframe=verde,
  fonttitle=\bfseries\color{white},coltitle=white,
  attach boxed title to top left={yshift=-2mm,xshift=4mm},
  boxed title style={colback=verde},
  title={#1},arc=4pt,boxrule=0.8pt,
  left=6pt,right=6pt,top=6pt,bottom=6pt}

%% Encabezado y pie
\pagestyle{fancy}\fancyhf{}
"""
    pre += rf"\lhead{{\small\textbf{{{dept}}}}}" + "\n"
    pre += rf"\rhead{{\small {nivel} --- {asig}}}" + "\n"
    pre += r"\lfoot{\small\textit{proscar.cl}}" + "\n"
    pre += r"\rfoot{\small Página \thepage\ de \pageref{LastPage}}" + "\n"
    pre += r"""\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.4pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}

\begin{document}
"""

    # ── Encabezado visual ─────────────────────────────────────────────────────
    enc = ""
    if inst:
        enc += rf"\begin{{center}}\Large\textbf{{{inst}}}\end{{center}}"+"\n"
    enc += rf"\begin{{center}}\large\textbf{{{dept}}}\end{{center}}"+"\n"
    enc += r"\vspace{-2mm}"+"\n"
    enc += r"\begin{center}"+"\n"
    enc += r"\begin{tabular}{|p{7cm}|p{5cm}|p{3cm}|}"+"\n"+r"\hline"+"\n"
    enc += rf"\textbf{{Nombre:}} & \textbf{{Nivel:}} {nivel} & \textbf{{Fecha:}} {fecha} \\"+"\n"
    enc += r"\hline"+"\n"
    enc += rf"\textbf{{Unidad:}} {tema} & \multicolumn{{2}}{{l|}}{{\textbf{{Asig.:}} {asig}}} \\"+"\n"
    enc += r"\hline"+"\n"
    enc += r"\end{tabular}"+"\n"+r"\end{center}"+"\n"+r"\vspace{2mm}"+"\n"

    # Título
    tit = rf"\begin{{center}}\textbf{{\Large {tipo} N°{num} --- {tema}}}"
    if nivel:
        tit += rf"\\\normalsize\textit{{{nivel}}}"
    if oas:
        tit += rf"\\\small OA: \texttt{{{oas}}}"
    tit += r"\end{center}"+"\n"+r"\vspace{2mm}"+"\n"

    # ── Bloques ───────────────────────────────────────────────────────────────
    cuerpo = ""
    n = 1
    for b in g.get("bloques", []):
        titulo_b = b.get("titulo", "")
        teoria   = b.get("teoria", "")
        tej      = b.get("titulo_ejemplo", "Ejemplo resuelto")
        ej       = b.get("ejemplo", "")
        ejers    = b.get("ejercicios", [])

        if teoria:
            cuerpo += rf"\begin{{cajat}}[{titulo_b}]"+"\n"+teoria+"\n"+r"\end{cajat}"+"\n\n"
        if ej:
            cuerpo += rf"\begin{{cajae}}[{tej}]"+"\n"+ej+"\n"+r"\end{cajae}"+"\n\n"

        if ejers:
            cuerpo += r"\textbf{Ejercicios}"+"\n\n"
            cuerpo += r"\begin{enumerate}[label=\textbf{\arabic*.},start="+str(n)+"]\n"
            for e in ejers:
                enun = e.get("enunciado", "")
                alts = e.get("alternativas", [])
                cuerpo += rf"\item {enun}\\[2pt]"+"\n"
                if alts:
                    cuerpo += alternativas_latex(alts)
                cuerpo += r"\vspace{4pt}"+"\n"
                n += 1
            cuerpo += r"\end{enumerate}"+"\n\n"

        cuerpo += r"\vspace{4mm}"+"\n"

    # ── Tabla de soluciones ───────────────────────────────────────────────────
    sol = ""
    sols = g.get("soluciones", {})
    if sols:
        items  = list(sols.items())
        grupos = [items[i:i+8] for i in range(0, len(items), 8)]
        sol += r"\vspace{4mm}"+"\n"
        sol += r"\begin{center}\textbf{Soluciones}\end{center}"+"\n"
        sol += r"\begin{center}"+"\n"
        ncols = min(8, len(items))
        sol += r"\begin{tabular}{|"+"c|"*ncols+"}\n"+r"\hline"+"\n"
        for grupo in grupos:
            sol += " & ".join([rf"\textbf{{{k}}}" for k,_ in grupo])+r" \\"+"\n"
            sol += r"\hline"+"\n"
            sol += " & ".join([v for _,v in grupo])+r" \\"+"\n"
            sol += r"\hline"+"\n"
        sol += r"\end{tabular}"+"\n"+r"\end{center}"+"\n"

    pie = (
        "\n"+r"\vfill"+"\n"
        r"\begin{center}\small\color{gris}"
        r"Generado con \texttt{latex-guia-pdf} $\cdot$ "
        r"\href{https://proscar.cl}{proscar.cl}"
        r"\end{center}"+"\n"
        r"\end{document}"+"\n"
    )

    return pre + enc + tit + cuerpo + sol + pie


def compilar(tex: Path) -> bool:
    exe = shutil.which("xelatex") or shutil.which("pdflatex")
    if not exe:
        print("⚠️  Sin compilador LaTeX local.")
        print("   → Sube el .tex a https://overleaf.com (gratis, sin instalar nada)")
        return False
    cmd = [exe, "-interaction=nonstopmode", f"-output-directory={tex.parent}", str(tex)]
    for _ in range(2):
        r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        log = tex.with_suffix(".log")
        print(f"❌ Error — revisa: {log}")
        for line in r.stdout.split("\n"):
            if line.startswith("!"):
                print(f"   {line}")
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description="Genera guías LaTeX → PDF para profesores")
    ap.add_argument("--input",   help="JSON con la guía")
    ap.add_argument("--ejemplo", action="store_true", help="Ejemplo de Números Complejos")
    ap.add_argument("--tema",    default="Matemática General")
    ap.add_argument("--nivel",   default="")
    ap.add_argument("--tipo",    default="guia", choices=["guia","apunte","prueba","taller"])
    ap.add_argument("--numero",  type=int, default=1)
    ap.add_argument("--output",  default="")
    args = ap.parse_args()

    if args.input:
        guia = json.load(open(args.input, encoding="utf-8"))
    elif args.ejemplo:
        guia = EJEMPLO
    else:
        guia = {
            "departamento": "Departamento de Matemática",
            "tipo": args.tipo, "numero": args.numero,
            "nivel": args.nivel, "asignatura": "Matemática",
            "tema": args.tema, "fecha": "2026",
            "bloques": [], "soluciones": {}
        }

    nombre   = args.output or str(OUT_DIR / f"{guia.get('tema','doc').replace(' ','_')}_n{guia.get('numero',1)}")
    tex_path = Path(nombre+".tex")

    tex_path.write_text(build_latex(guia), encoding="utf-8")
    print(f"✅ LaTeX: {tex_path}")

    if compilar(tex_path):
        pdf = Path(nombre+".pdf")
        print(f"✅ PDF:   {pdf}")
        for ext in [".aux",".log",".out"]:
            f = Path(nombre+ext)
            if f.exists(): f.unlink()
    else:
        print(f"📄 Sube a Overleaf: https://overleaf.com/project/new")
    print(f"\n📁 Archivos en: {OUT_DIR}/")

if __name__ == "__main__":
    main()
