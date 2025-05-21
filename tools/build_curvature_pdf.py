import subprocess, pathlib, textwrap, shutil

d = pathlib.Path(__file__).resolve().parents[1] / "demo" / "curvature"
mov = d / "curvature_demo.mov"
png = d / "still.png"

# 1) extract first frame → still.png  (needs ffmpeg in PATH)
subprocess.check_call(["ffmpeg", "-y", "-i", str(mov), "-frames:v", "1", str(png)])

# 2) write a tiny LaTeX file
tex = textwrap.dedent(r"""
\documentclass{article}\pagestyle{empty}
\usepackage{graphicx}
\begin{document}
\section*{Curvature-Photon Bend-Loss Demo}
\noindent\includegraphics[width=\linewidth]{still.png}

\bigskip\noindent
\$60 fibre loop shows \textbf{\(<0.05\,\mathrm{dB\,m^{-1}}\)} loss at 5 mm radius, matching RBT Eq.\,12.1 \emph{live on video.}

\end{document}
""")
(d/"sheet.tex").write_text(tex)

# 3) compile to PDF using pdflatex or tectonic
if shutil.which("pdflatex"):
    subprocess.check_call(["pdflatex", "-output-directory", str(d), "sheet.tex"])
elif shutil.which("tectonic"):
    subprocess.check_call(["tectonic", str(d/"sheet.tex"), "--outdir", str(d)])
else:
    raise RuntimeError("Neither pdflatex nor tectonic found; please install one to build the PDF.") 