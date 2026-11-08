#!/usr/bin/env python3
"""
verify.py — verify the TAU strands yourself.

Reproduces the spectral gap (lambda2) of any DNA sequence with free tools.

lambda2 = the SIGNED real part of the 2nd eigenvalue (by magnitude) of the
4x4 row-normalized base-transition matrix.  A random sequence gives lambda2 = 0
(noise); a structured sequence gives a nonzero value (order).

Run:
    python verify.py data/tau_base.dna        # expect ~ -0.142  (disordered)
    python verify.py data/strands/core.dna    # expect ~ +0.117  (ordered)

Only numpy is required.
"""
import sys
import numpy as np

_D = {"A": 0, "C": 1, "G": 2, "T": 3}


def lambda2(seq):
    """Spectral gap of a DNA sequence (ACGT)."""
    digits = [_D[c] for c in seq.upper() if c in _D]
    if len(digits) < 2:
        return 0.0
    # 4x4 transition counts
    t = [[0, 0, 0, 0] for _ in range(4)]
    prev = digits[0]
    for d in digits[1:]:
        t[prev][d] += 1
        prev = d
    # row-normalize (zero rows -> uniform)
    P = []
    for row in t:
        rs = float(sum(row))
        if rs > 0:
            P.append([row[0] / rs, row[1] / rs, row[2] / rs, row[3] / rs])
        else:
            P.append([0.25, 0.25, 0.25, 0.25])
    ev = np.linalg.eigvals(np.array(P))
    # second eigenvalue by magnitude, signed real part
    order = sorted(range(4), key=lambda i: -abs(ev[i]))
    return float(ev[order[1]].real)


def main():
    if len(sys.argv) < 2:
        print("usage: python verify.py <file.dna> [file2.dna ...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        with open(path) as f:
            seq = "".join(f.read().split())
        print("%-40s lambda2 = %+.6f" % (path, lambda2(seq)))


if __name__ == "__main__":
    main()
