#!/usr/bin/env python3
"""
Self-Cooling Interposer Estimator  –  RBT Sec 14.4

ΔT = sqrt(σ_c P L) − sqrt(σ_cp P L)

If ΔT ≥ 5 °C → print "✅ swap recommended"
"""

import argparse, math

SIGMA_C  = 0.12   # °C² / (W·m)  (copper)
SIGMA_CP = 0.03   # °C² / (W·m)  (curvature-photon export)

def delta_t(power_w: float, length_m: float) -> float:
    return math.sqrt(SIGMA_C * power_w * length_m) - math.sqrt(SIGMA_CP * power_w * length_m)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--power_w", type=float, required=True,
                    help="Package power in watts (e.g. 600)")
    ap.add_argument("--trace_len_m", type=float, required=True,
                    help="Total length of copper traces to swap (metres, e.g. 0.05)")
    args = ap.parse_args()

    dT = delta_t(args.power_w, args.trace_len_m)
    verdict = "✅ swap recommended" if dT >= 5 else "❌ benefit too small"
    print(f"Predicted ΔT = {dT:.2f} °C   {verdict}") 