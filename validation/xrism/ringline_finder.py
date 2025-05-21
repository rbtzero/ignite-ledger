#!/usr/bin/env python
"""
ringline_finder.py  —  XRISM Resolve annular-line significance

Usage:
    python ringline_finder.py events.evt

Outputs:
    Δℒ (Poisson log-likelihood) and the corresponding σ.
"""
import sys, numpy as np, astropy.io.fits as fits, argparse

# default energies to scan
ENERGIES = [3.540, 2.800]          # keV
BINW     = 0.005                   # half-width (keV)
R_IN, R_OUT = 30, 80               # arcsec

def annulus(x, y, r1, r2):
    r = np.hypot(x, y)
    return (r > r1) & (r < r2)

def run(evt, e0):
    dat = fits.getdata(evt, 1)
    e   = dat['PI'] * 0.001          # PI → keV
    x   = dat['X'];   y = dat['Y']

    on  = annulus(x, y, R_IN, R_OUT)
    off = ~on

    # line window mask
    m  = (e > e0-BINW) & (e < e0+BINW)
    N_on,  N_off  = np.sum(on & m),  np.sum(off & m)

    if N_off == 0:
        print("No background counts – dummy file too small.")
        return

    # Poisson log-likelihood ratio Δℒ
    L = N_on * np.log((N_on+N_off)/N_off) - (N_on+N_off) + N_off
    sigma = np.sqrt(2*L)
    print(f"Annular excess @ {e0:.3f} keV  →  Δℒ = {L:.1f}   ({sigma:.1f} σ)")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("evt", help="Resolve event file")
    p.add_argument("--e", nargs="+", type=float,
                   default=ENERGIES, help="Line energy/ies keV")
    args = p.parse_args()
    for e0 in args.e:
        run(args.evt, e0) 