#!/usr/bin/env python
"""
line_scan_locked_continuum.py – two–spectrum scan where the second spectrum
shares the continuum parameters of the first (frozen), mimicking the
Hitomi/Resolve "on/off" analysis.

Usage
  python line_scan_locked_continuum.py spec_std.pi spec_g7.pi
prints a TSV with ΔC and flux for the grade-7 spectrum with continuum locked.
"""
import sys, numpy as np
from pathlib import Path
from sherpa.astro import ui as su

ENERGIES = [3.54, 2.80]


def load_and_prepare(idx: int, pha: Path):
    su.load_pha(idx, str(pha))
    su.set_analysis(idx, "energy")
    su.ignore_id(idx, None, 2.0)
    su.ignore_id(idx, 7.0, None)


def build_continuum(idx: int):
    tb = su.xstbabs(f"tb{idx}"); tb.nH = 0.14; tb.nH.freeze()
    ap1 = su.xsapec(f"ap1_{idx}"); ap2 = su.xsapec(f"ap2_{idx}")
    for ap in (ap1, ap2):
        ap.kT = 4.0; ap.Abundanc = 0.5; ap.redshift = 0.0179
    su.set_source(idx, tb * (ap1 + ap2))
    return ap1, ap2


def add_gaussian(idx: int, e: float):
    tag = str(e).replace('.', '')
    g = su.xszgauss(f"g{tag}")
    g.LineE = e; g.LineE.min = e - 0.03; g.LineE.max = e + 0.03
    g.Sigma = 0.03; g.Sigma.min = 0.01; g.Sigma.max = 0.06
    g.Norm = 0
    su.set_source(idx, su.get_source(idx) + g)
    return g


def main():
    if len(sys.argv) != 3:
        sys.exit("need two PHA files: good-grade then grade-7")
    std_pha, g7_pha = map(Path, sys.argv[1:])

    # 1) Fit continuum on good-grade spectrum
    su.clean()
    load_and_prepare(1, std_pha)
    su.set_stat("cstat")
    ap1_std, ap2_std = build_continuum(1)
    su.fit(1)
    cont_vals = {p.name: p.val for p in (ap1_std.kT, ap1_std.norm,
                                         ap2_std.kT, ap2_std.norm)}

    # 2) Load grade-7 spectrum with continuum fixed to those values
    su.clean()
    load_and_prepare(1, g7_pha)
    su.set_stat("cstat")
    ap1_g7, ap2_g7 = build_continuum(1)
    for ap_g7, ap_std in zip((ap1_g7, ap2_g7), (ap1_std, ap2_std)):
        ap_g7.kT = ap_std.kT.val; ap_g7.kT.freeze()
        ap_g7.norm = ap_std.norm.val; ap_g7.norm.freeze()
    base = su.calc_stat(1)

    print("file\tenergy_keV\tdeltaC\tflux\tflux_err")
    for e in ENERGIES:
        g = add_gaussian(1, e)
        su.fit(1)
        stat = su.get_fit_results().statval
        delta = base - stat
        try:
            su.proj(1, g.Norm)
            ferr = g.Norm.err
        except Exception:
            ferr = np.nan
        print(f"{g7_pha.name}\t{e:.3f}\t{delta:.2f}\t{g.Norm.val:.3e}\t{ferr:.3e}")
        su.set_source(1, su.get_source(1) - g)


if __name__ == "__main__":
    main() 