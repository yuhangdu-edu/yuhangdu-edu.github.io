"""
Replace white fills in Layer 2 data boxes with surrounding background color.

Each of the 22 sectors × 6 holes = 132 data boxes in Layer 2 has a white
PPTX text-box fill that shows through the transparent holes in Layer 1.
For each position we:
  1. Compute the Layer 2 pixel position using the rotation formula from sba-wheel.js
  2. Sample the median non-white color in an annular ring around the box
  3. Replace all near-white pixels in the box area with that color
"""
import math, os
import numpy as np
from PIL import Image

# ── Constants (same as generate_sba_images_hires.py) ──────────────────────────
OUT_W = OUT_H = 2400
EXPORT_SIZE   = 7200
SCALE         = EXPORT_SIZE / 1800
SX = int(round(515 * SCALE))   # 2060
SY = int(round(217 * SCALE))   # 868
SW = int(round(694 * SCALE))   # 2776
SH = int(round(1234 * SCALE))  # 4936
CX_OUT = OUT_W // 2  # 1200
CY_OUT = OUT_H // 2  # 1200

# ── Wheel geometry (from sba-wheel.js) ────────────────────────────────────────
N             = 22
ASTEP         = 2 * math.pi / N
A0            = -math.pi / 2
DEFAULT_ANGLE = -2.878   # arrow angle in natural Layer 1 PNG (empirical)

# ── Layer 1 hole positions in PPTX fractional coords ──────────────────────────
HOLE_SHAPES_FRAC = [
    (0.4560, 0.1874, 0.0181, 0.0219),   # hole 0: No MWH Stay count
    (0.5300, 0.4029, 0.0176, 0.0254),   # hole 1: innermost stay row
    (0.5470, 0.3843, 0.0176, 0.0254),
    (0.5644, 0.3663, 0.0176, 0.0254),
    (0.5809, 0.3487, 0.0176, 0.0254),
    (0.5976, 0.3317, 0.0176, 0.0254),   # hole 5: outermost stay row
]

def frac_to_px(cx_frac, cy_frac, w_frac, h_frac):
    cx_exp = cx_frac * EXPORT_SIZE;  cy_exp = cy_frac * EXPORT_SIZE
    w_exp  = w_frac  * EXPORT_SIZE;  h_exp  = h_frac  * EXPORT_SIZE
    cx_out = (cx_exp - SX) * (OUT_W / SW)
    cy_out = (cy_exp - SY) * (OUT_H / SH)
    w_out  = w_exp  * (OUT_W / SW)
    h_out  = h_exp  * (OUT_H / SH)
    return cx_out, cy_out, w_out, h_out

HOLES_L1 = [frac_to_px(*h) for h in HOLE_SHAPES_FRAC]

def get_l2_pos(hole_idx, sector_idx):
    """
    Layer 2 pixel position revealed by hole_idx when Layer 1 shows sector_idx.

    From sba-wheel.js:
        rotation = (A0 + selected*ASTEP + ASTEP/2) - DEFAULT_ANGLE
        ctx.translate(CX, CY); ctx.rotate(rotation); drawImage Layer1

    A Layer 1 pixel at (px, py) maps to Layer 2 at:
        x = CX + (px-CX)*cos(rotation) - (py-CY)*sin(rotation)
        y = CY + (px-CX)*sin(rotation) + (py-CY)*cos(rotation)
    """
    cx_l1, cy_l1 = HOLES_L1[hole_idx][0], HOLES_L1[hole_idx][1]
    rx = cx_l1 - CX_OUT
    ry = cy_l1 - CY_OUT
    rotation = (A0 + sector_idx * ASTEP + ASTEP / 2) - DEFAULT_ANGLE
    c = math.cos(rotation)
    s = math.sin(rotation)
    return CX_OUT + rx * c - ry * s, CY_OUT + rx * s + ry * c

def sample_bg(arr, cx, cy, r_in, r_out):
    """Median non-white RGB in annulus [r_in, r_out] around (cx, cy)."""
    H, W = arr.shape[:2]
    ci, ri = int(round(cx)), int(round(cy))
    x0 = max(0, ci - r_out);  x1 = min(W, ci + r_out + 1)
    y0 = max(0, ri - r_out);  y1 = min(H, ri + r_out + 1)
    if x0 >= x1 or y0 >= y1:
        return None
    reg = arr[y0:y1, x0:x1]
    ys, xs = np.mgrid[y0:y1, x0:x1]
    dist = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    ring  = (dist >= r_in) & (dist < r_out)
    r_ch  = reg[:, :, 0].astype(float)
    g_ch  = reg[:, :, 1].astype(float)
    b_ch  = reg[:, :, 2].astype(float)
    nw    = ring & ~((r_ch > 230) & (g_ch > 230) & (b_ch > 230))
    if nw.sum() < 5:
        return None
    return (int(np.median(r_ch[nw])), int(np.median(g_ch[nw])), int(np.median(b_ch[nw])))

def clear_white(arr, cx, cy, half_w, half_h, fill_rgb):
    """Replace near-white pixels in rectangle [±half_w, ±half_h] with fill_rgb."""
    H, W = arr.shape[:2]
    ci, ri = int(round(cx)), int(round(cy))
    x0 = max(0, ci - half_w);  x1 = min(W, ci + half_w + 1)
    y0 = max(0, ri - half_h);  y1 = min(H, ri + half_h + 1)
    if x0 >= x1 or y0 >= y1:
        return 0
    reg  = arr[y0:y1, x0:x1]
    white = (reg[:, :, 0].astype(int) > 220) & \
            (reg[:, :, 1].astype(int) > 220) & \
            (reg[:, :, 2].astype(int) > 220)
    count = int(white.sum())
    if count:
        reg[white] = fill_rgb
        arr[y0:y1, x0:x1] = reg
    return count

# ── Main ──────────────────────────────────────────────────────────────────────
OUT_DIR = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel'

for fname in ['layer2_nuli.png', 'layer2_multi.png']:
    path = os.path.join(OUT_DIR, fname)
    img  = Image.open(path).convert('RGB')
    arr  = np.array(img)
    total = 0

    print(f"\nProcessing {fname} ...")

    for h in range(6):
        cx_l1, cy_l1, w_l1, h_l1 = HOLES_L1[h]
        half_w = int(w_l1 / 2) + 4   # slightly larger than hole to catch glow
        half_h = int(h_l1 / 2) + 4
        r_in  = max(half_w, half_h) + 6
        r_out = max(half_w, half_h) + 45

        skipped = 0
        for s in range(N):
            cx_l2, cy_l2 = get_l2_pos(h, s)

            color = sample_bg(arr, cx_l2, cy_l2, r_in, r_out)
            if color is None:
                color = sample_bg(arr, cx_l2, cy_l2, r_out, r_out + 40)
            if color is None:
                skipped += 1
                continue

            n = clear_white(arr, cx_l2, cy_l2, half_w, half_h, color)
            total += n

        if skipped:
            print(f"  hole {h}: {skipped} sectors skipped (no bg sample)")

    print(f"  Total white pixels replaced: {total:,}")
    Image.fromarray(arr, 'RGB').save(path, 'PNG', optimize=False)
    print(f"  Saved {path} ({os.path.getsize(path) // 1024} KB)")

print("\nDone.")
