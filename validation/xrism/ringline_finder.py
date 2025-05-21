#!/usr/bin/env python
"""
ringline_finder.py  —  XRISM Resolve annular-line significance

Usage:
    python ringline_finder.py events.evt

Outputs:
    Δℒ (Poisson log-likelihood) and the corresponding σ.
"""
import sys, numpy as np, astropy.io.fits as fits

E0   = 3.540      # keV
BINW = 0.005      # 5 eV half-width
R_IN, R_OUT = 30, 80   # arcsec

def annulus(x, y, r1, r2):
    r = np.hypot(x, y)
    return (r > r1) & (r < r2)

def main(evt):
    dat = fits.getdata(evt, 1)
    e   = dat['PI'] * 0.001          # PI → keV
    x   = dat['X'];   y = dat['Y']

    on  = annulus(x, y, R_IN, R_OUT)
    off = ~on

    # line window mask
    m  = (e > E0-BINW) & (e < E0+BINW)
    N_on,  N_off  = np.sum(on & m),  np.sum(off & m)

    if N_off == 0:
        print("No background counts – dummy file too small.")
        return

    # Poisson log-likelihood ratio Δℒ
    L = N_on * np.log((N_on+N_off)/N_off) - (N_on+N_off) + N_off
    sigma = np.sqrt(2*L)
    print(f"Annular excess @ {E0:.3f} keV  →  Δℒ = {L:.1f}   ({sigma:.1f} σ)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ringline_finder.py events.evt"); sys.exit(1)
    main(sys.argv[1]) 