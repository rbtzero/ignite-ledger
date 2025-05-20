# Ignite-Ledger Bootstrap
![CI](https://github.com/rbtzero/ignite-ledger/actions/workflows/bendloss.yml/badge.svg)
![Interposer CI](https://github.com/rbtzero/ignite-ledger/actions/workflows/interposer.yml/badge.svg)

This repository is the **public, immutable starting point** for the Recursive Becoming Theory (RBT) engineering stack.

## Contents

| Path | Purpose |
|------|---------|
| `curvature_solver.py` | Minimal reference implementation of the curvature–photon waveguide solver (Eq. 12.1). |
| `proof_hash.txt` | SHA-256 digest of the Lean proof corpus and demo notebooks; anchored on-chain. |
| `email_templates/` | Ready‑to‑send LOI messages for Fortune‑100 R&D leads. |
| `demo/` | Placeholder for Colab / Jupyter notebooks used in the live demo streams. |

## Quick start

### Curvature-loss demo

▶ [Uncut curvature demo](https://youtu.be/OJpLFGMwim8)

```bash
python curvature_solver.py --radius_mm 5 --wavelength_nm 1550
```

Expected output:

```
Predicted bend loss ≤ 0.049 dB·m⁻¹  ✅
```

---

![Interposer CI](https://github.com/rbtzero/ignite-ledger/actions/workflows/interposer.yml/badge.svg)

### Self-cooling interposer demo

▶ [Uncut interposer demo](https://youtu.be/6dMowP_vEXM)

```bash
python interposer_estimator.py --power_w 600 --trace_len_m 2
```

Expected output:

```
Predicted ΔT = 6.00 °C   ✅ swap recommended
```

---

![LedgerOpt CI](https://github.com/rbtzero/ignite-ledger/actions/workflows/ledgeropt.yml/badge.svg)

### LedgerOpt max-flow demo

▶ [Uncut LedgerOpt demo](https://youtu.be/vVZ4NJ29y9w)

## Licence

Everything in this repo is released under **Apache 2.0**.  The underlying mathematics is public‑domain (CC0).
