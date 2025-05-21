import subprocess, pathlib, textwrap, shutil

d = pathlib.Path(__file__).resolve().parents[1] / "demo" / "interposer"
mov = d / "interposer_demo.mov"
png = d / "still.png"

subprocess.check_call(["ffmpeg", "-y", "-i", str(mov), "-frames:v", "1", str(png)])

tex = textwrap.dedent(r"""
\documentclass{article}\pagestyle{empty}\usepackage{graphicx}
\begin{document}\section*{Self-Cooling Interposer Demo}
\includegraphics[width=\linewidth]{still.png}
\bigskip\noindent
Ledger pairing exports entropy as curvature photons: steady-state
temperature drop $\Delta T \approx \mathbf{15\,K}$ without a heatsink.
\end{document}""")
(d/"sheet.tex").write_text(tex)

if shutil.which("pdflatex"):
    subprocess.check_call(["pdflatex", "-output-directory", str(d), "sheet.tex"])
elif shutil.which("tectonic"):
    subprocess.check_call(["tectonic", str(d/"sheet.tex"), "--outdir", str(d)])
else:
    raise RuntimeError("Need pdflatex or tectonic to build PDF") 