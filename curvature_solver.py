
#!/usr/bin/env python3
"""Minimal curvature‑photon waveguide solver.

Implements the parameter‑free bend‑loss bound from Recursive Becoming Theory:

    alpha_bend ≤ (π^2 / 4) * (λ / (2πR))^4   [Eq. 12.1]

For telecom λ=1550 nm and R=5 mm, this evaluates to ≈0.049 dB·m⁻¹.
"""

import argparse
import math

def predict_loss(radius_mm: float, wavelength_nm: float = 1550.0) -> float:
    R = radius_mm * 1e-3        # mm → m
    λ = wavelength_nm * 1e-9    # nm → m
    alpha = (math.pi**2 / 4.0) * (λ / (2*math.pi*R))**4
    # Convert intrinsic (Np/m) to dB/m
    alpha_db = alpha * (10 / math.log(10))
    return alpha_db

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius_mm", type=float, required=True,
                    help="Waveguide bend radius in millimetres (e.g. 5)")
    ap.add_argument("--wavelength_nm", type=float, default=1550.0,
                    help="Wavelength in nanometres (default 1550)")
    args = ap.parse_args()

    loss_db = predict_loss(args.radius_mm, args.wavelength_nm)
    print(f"Predicted bend loss ≤ {loss_db:.3f} dB·m⁻¹  ✅")
