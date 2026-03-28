"""
Replace white PPTX shape backgrounds near holes 1-5 in Layer 1 with disc color.

Making the white shapes transparent exposes Layer 2's sector divider lines behind
them. Instead, we REPLACE white pixels with the disc's light-blue background color
(sampled from nearby non-white opaque disc pixels) so they remain opaque and
continue to cover Layer 2, but now blend visually with the disc instead of showing
as white boxes.

Radius=200 covers all white shape backgrounds (original 80px cleanup was too small).
Disc background is ~184,219,241 — well below the >240 white threshold.
"""
import os
import numpy as np
from PIL import Image

OUT_W = OUT_H = 2400
EXPORT_SIZE   = 7200
SCALE         = EXPORT_SIZE / 1800
SX = int(round(515 * SCALE))
SY = int(round(217 * SCALE))
SW = int(round(694 * SCALE))
SH = int(round(1234 * SCALE))

HOLE_SHAPES_FRAC = [
    (0.4560, 0.1874, 0.0181, 0.0219),
    (0.5300, 0.4029, 0.0176, 0.0254),
    (0.5470, 0.3843, 0.0176, 0.0254),
    (0.5644, 0.3663, 0.0176, 0.0254),
    (0.5809, 0.3487, 0.0176, 0.0254),
    (0.5976, 0.3317, 0.0176, 0.0254),
]

def frac_to_px(cx_frac, cy_frac, w_frac, h_frac):
    cx_exp = cx_frac * EXPORT_SIZE;  cy_exp = cy_frac * EXPORT_SIZE
    w_exp  = w_frac  * EXPORT_SIZE;  h_exp  = h_frac  * EXPORT_SIZE
    cx_out = (cx_exp - SX) * (OUT_W / SW)
    cy_out = (cy_exp - SY) * (OUT_H / SH)
    w_out  = w_exp  * (OUT_W / SW)
    h_out  = h_exp  * (OUT_H / SH)
    return cx_out, cy_out, w_out, h_out

HOLES = [frac_to_px(*h) for h in HOLE_SHAPES_FRAC]

RADIUS = 200

OUT_DIR = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel'

for fname in ['layer1_nuli.png', 'layer1_multi.png']:
    path = os.path.join(OUT_DIR, fname)
    img  = Image.open(path).convert('RGBA')
    arr  = np.array(img)
    H, W = arr.shape[:2]
    total = 0

    print(f"\nProcessing {fname} ...")

    for i, (cx, cy, w_l1, h_l1) in enumerate(HOLES):
        if i == 0:
            continue   # hole 0 is in the white disc sector; skip

        cxi, cyi = int(round(cx)), int(round(cy))
        sx0 = max(0, cxi - RADIUS);  sx1 = min(W, cxi + RADIUS)
        sy0 = max(0, cyi - RADIUS);  sy1 = min(H, cyi + RADIUS)
        reg = arr[sy0:sy1, sx0:sx1, :]

        # Identify white pixels to replace
        is_white = (
            (reg[:, :, 0].astype(int) > 240) &
            (reg[:, :, 1].astype(int) > 240) &
            (reg[:, :, 2].astype(int) > 240) &
            (reg[:, :, 3]             > 0)
        )

        # Sample disc background: median of non-white, opaque, non-transparent pixels
        # Use a ring further out (radius 220-280) to avoid the white-shape zone
        sr = 250
        sx0s = max(0, cxi - sr); sx1s = min(W, cxi + sr)
        sy0s = max(0, cyi - sr); sy1s = min(H, cyi + sr)
        sample_reg = arr[sy0s:sy1s, sx0s:sx1s, :]
        ys_s, xs_s = np.mgrid[sy0s:sy1s, sx0s:sx1s]
        dist_s = np.sqrt((xs_s - cx)**2 + (ys_s - cy)**2)
        disc_mask = (
            (dist_s >= 210) & (dist_s < sr) &
            (sample_reg[:, :, 3] > 200) &
            ~((sample_reg[:, :, 0] > 240) &
              (sample_reg[:, :, 1] > 240) &
              (sample_reg[:, :, 2] > 240))
        )
        if disc_mask.sum() >= 10:
            disc_r = int(np.median(sample_reg[:, :, 0][disc_mask]))
            disc_g = int(np.median(sample_reg[:, :, 1][disc_mask]))
            disc_b = int(np.median(sample_reg[:, :, 2][disc_mask]))
        else:
            disc_r, disc_g, disc_b = 184, 219, 241   # fallback

        print(f"  Hole {i}: disc color sampled = ({disc_r},{disc_g},{disc_b}), "
              f"replacing {is_white.sum()} white px")

        # Replace white → disc color (keep alpha=255 so Layer 2 stays covered)
        reg[is_white, 0] = disc_r
        reg[is_white, 1] = disc_g
        reg[is_white, 2] = disc_b
        # alpha stays 255 — do NOT set to 0
        arr[sy0:sy1, sx0:sx1, :] = reg
        total += int(is_white.sum())

    print(f"  Total replaced: {total:,}")
    Image.fromarray(arr, 'RGBA').save(path, 'PNG', optimize=False)
    print(f"  Saved {path} ({os.path.getsize(path) // 1024} KB)")

print("\nDone.")
