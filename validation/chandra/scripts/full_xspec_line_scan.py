#!/usr/bin/env python
"""
full_xspec_line_scan.py – TBabs*2TAPEC plus Gaussian scan using Sherpa+XSPEC

Run like
  python full_xspec_line_scan.py --files file1.pha file2.pha ... --energies 3.54 2.80
Produces a TSV table on stdout.
"""
import argparse, sys
from pathlib import Path
import numpy as np
from sherpa.astro import ui as su


def load_dataset(idx: int, pha: Path):
    su.load_pha(idx, str(pha))
    # Work in energy space for ignore filters
    su.set_analysis(idx, "energy")
    su.ignore_id(idx, None, 2.0)
    su.ignore_id(idx, 7.0, None)


def build_continuum(idx: int):
    tb = su.xstbabs(f"tb{idx}")
    tb.nH = 0.14
    tb.nH.freeze()
    ap1 = su.xsapec(f"ap1_{idx}")
    ap2 = su.xsapec(f"ap2_{idx}")
    for ap in (ap1, ap2):
        ap.kT = 4.0
        ap.Abundanc = 0.5
        ap.redshift = 0.0179
    su.set_source(idx, tb * (ap1 + ap2))


def add_gaussian(idx: int, energy_keV: float):
    tag = str(energy_keV).replace('.', '')
    g = su.xszgauss(f"g{tag}")
    g.LineE = energy_keV
    g.LineE.min = energy_keV - 0.03
    g.LineE.max = energy_keV + 0.03
    g.Sigma = 0.03
    g.Sigma.min = 0.01
    g.Sigma.max = 0.06
    g.Norm = 0
    cur = su.get_source(idx)
    su.set_source(idx, cur + g)
    return g


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--files", nargs="+", required=True)
    p.add_argument("--energies", nargs="+", type=float, default=[3.54, 2.80])
    args = p.parse_args()

    print("file\tenergy_keV\tdeltaC\tflux\tflux_err\tcentroid\tsigma")
    for f in args.files:
        su.clean()
        load_dataset(1, Path(f))
        su.set_stat("cstat")
        build_continuum(1)
        su.fit(1)
        base = su.get_fit_results().statval
        for e in args.energies:
            g = add_gaussian(1, e)
            su.fit(1)
            stat = su.get_fit_results().statval
            delta = base - stat
            try:
                su.proj(1, g.Norm)
                ferr = g.Norm.err
            except Exception:
                ferr = np.nan
            print(f"{Path(f).name}\t{e:.3f}\t{delta:.2f}\t{g.Norm.val:.3e}\t{ferr:.3e}\t{g.LineE.val:.4f}\t{g.Sigma.val:.4f}")
            # remove gaussian component cleanly
            cur = su.get_source(1)
            su.set_source(1, cur - g)


if __name__ == "__main__":
    main() 