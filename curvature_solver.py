#!/usr/bin/env python3
"""
Minimal curvature-photon waveguide solver.

Implements the parameter-free bend-loss bound from Recursive Becoming Theory:

    alpha_bend ≤ (π^2 / 4) * (λ / (2πR))^4        [Eq. 12.1]

Example (telecom λ = 1550 nm, R = 5 mm) returns ≈ 6.35 e-17 dB·m⁻¹.
"""

import argparse
import math


def predict_loss(radius_mm: float, wavelength_nm: float = 1550.0) -> float:
    """Return bend-loss upper bound in dB per metre.

    Args:
        radius_mm: Bend radius in millimetres.
        wavelength_nm: Wavelength in nanometres (default 1550).

    Returns:
        Loss coefficient in dB · m⁻¹ (float, parameter-free bound).
    """
    R = radius_mm * 1e-3       # mm → m
    lam = wavelength_nm * 1e-9 # nm → m
    alpha_np = (math.pi**2 / 4.0) * (lam / (2 * math.pi * R))**4  # Np · m⁻¹
    alpha_db = alpha_np * (10.0 / math.log(10.0))                 # dB · m⁻¹
    return alpha_db


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius_mm", type=float, required=True,
                    help="Waveguide bend radius in millimetres (e.g. 5)")
    ap.add_argument("--wavelength_nm", type=float, default=1550.0,
                    help="Wavelength in nanometres (default 1550)")
    args = ap.parse_args()

    loss_db = predict_loss(args.radius_mm, args.wavelength_nm)
    print(f"Predicted bend loss ≤ {loss_db:.3e} dB·m⁻¹  ✅")
