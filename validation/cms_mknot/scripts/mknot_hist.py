#!/usr/bin/env python
"""
mknot_hist.py – build recoil-mass spectrum and save PNG

Run with ROOT6 available, after mknot_skim.py produced skim.root:
  python mknot_hist.py skim.root mrecoil_edge.png
"""
import sys, math, ROOT

infile  = sys.argv[1] if len(sys.argv)>1 else "skim.root"
outfile = sys.argv[2] if len(sys.argv)>2 else "mrecoil_edge.png"

f = ROOT.TFile.Open(infile)
t = f.Get("events")

h = ROOT.TH1F("h","recoil mass; m_{recoil} [GeV]; events / 0.5 GeV",120,0,60)

for ev in t:
    jet_pt = ev.jet_pt[0]
    jet_px = ev.jet_px[0]; jet_py = ev.jet_py[0]
    met    = ev.pfMet
    met_px = ev.pfMetPx;  met_py = ev.pfMetPy

    mrec2 = (met + jet_pt)**2 - ((jet_px+met_px)**2 + (jet_py+met_py)**2)
    if mrec2>0:
        h.Fill(math.sqrt(mrec2))

c = ROOT.TCanvas()
h.Draw()
c.SaveAs(outfile)
print(f"Histogram saved to {outfile}") 