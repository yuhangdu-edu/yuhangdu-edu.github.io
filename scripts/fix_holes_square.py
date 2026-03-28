"""
Fix Layer 1 holes: take the good flood-fill base (c6cb46f) and enlarge
rectangular holes to squares (max(w, h)), then re-run flood-fill.
No radius cleanup — that step over-punched hole 0.
"""
import sys, math
import numpy as np
from PIL import Image

# ── Same constants as generate_sba_images_hires.py ───────────────────────────
OUT_W = OUT_H = 2400
EXPORT_SIZE   = 7200
SCALE         = EXPORT_SIZE / 1800
SX = int(round(515 * SCALE))
SY = int(round(217 * SCALE))
SW = int(round(694 * SCALE))
SH = int(round(1234 * SCALE))
CX_OUT = OUT_W // 2  # 1200
CY_OUT = OUT_H // 2  # 1200
R_INNER = int(round(510 * OUT_W / 1200))   # 1020
R_OUTER = int(round(536 * OUT_W / 1200))   # 1072

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
    w_out  = w_exp * (OUT_W / SW)
    h_out  = h_exp * (OUT_H / SH)
    return cx_out, cy_out, w_out, h_out

HOLES = [frac_to_px(*h) for h in HOLE_SHAPES_FRAC]

for i, (cx, cy, w, h) in enumerate(HOLES):
    side = max(w, h)
    x0 = max(0, int(cx - side/2) - 2);  x1 = min(OUT_W, int(cx + side/2) + 2)
    y0 = max(0, int(cy - side/2) - 2);  y1 = min(OUT_H, int(cy + side/2) + 2)
    print(f"Hole {i}: center=({cx:.1f},{cy:.1f}), w={w:.1f}, h={h:.1f}, "
          f"side={side:.1f}, punch=[{x0}:{x1}, {y0}:{y1}] = {x1-x0}x{y1-y0}px")


def fix_layer1(in_path, out_path):
    img = Image.open(in_path).convert('RGBA')
    assert img.size == (OUT_W, OUT_H), f"Unexpected size {img.size}"
    arr = np.array(img)

    # Step 1 — punch square holes (overwrite existing rectangular holes)
    for (cx, cy, w, h) in HOLES:
        side = max(w, h)
        x0 = max(0, int(cx - side/2) - 2);  x1 = min(OUT_W, int(cx + side/2) + 2)
        y0 = max(0, int(cy - side/2) - 2);  y1 = min(OUT_H, int(cy + side/2) + 2)
        arr[y0:y1, x0:x1, 3] = 0

    # Step 2 — flood-fill: spread transparency from inner-disc holes into
    # adjacent near-white pixels (catches shadow/glow from new square edges)
    H, W = arr.shape[:2]
    ys_f, xs_f = np.mgrid[0:H, 0:W]
    dist_f = np.sqrt((xs_f - CX_OUT)**2 + (ys_f - CY_OUT)**2)

    expanding = (arr[:, :, 3] == 0) & (dist_f < R_INNER)
    nw_opaque = (
        (arr[:, :, 0] > 230) &
        (arr[:, :, 1] > 230) &
        (arr[:, :, 2] > 230) &
        (arr[:, :, 3] > 0)
    )
    iters = 0
    for _ in range(60):
        adj = np.zeros_like(expanding, dtype=bool)
        adj[1:, :]  |= expanding[:-1, :]
        adj[:-1, :] |= expanding[1:, :]
        adj[:, 1:]  |= expanding[:, :-1]
        adj[:, :-1] |= expanding[:, 1:]
        new_t = nw_opaque & adj
        if not new_t.any():
            break
        arr[new_t, 3] = 0
        expanding = new_t
        nw_opaque &= ~new_t
        iters += 1
    print(f"  Flood-fill: {iters} iterations")

    out_img = Image.fromarray(arr, 'RGBA')
    out_img.save(out_path, 'PNG', optimize=False)
    sz = __import__('os').path.getsize(out_path) // 1024
    print(f"  Saved {out_path} ({sz} KB)")


OUT_DIR = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel'

print("\nProcessing layer1_nuli.png ...")
fix_layer1(r'C:\Users\ydu\AppData\Local\Temp\layer1_nuli_base.png',
           OUT_DIR + r'\layer1_nuli.png')

print("\nProcessing layer1_multi.png ...")
fix_layer1(r'C:\Users\ydu\AppData\Local\Temp\layer1_multi_base.png',
           OUT_DIR + r'\layer1_multi.png')

print("\nDone.")
