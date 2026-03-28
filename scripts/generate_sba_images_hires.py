"""
Generate 2400x2400 SBA-wheel PNGs from tool_design_updated.pptx.
Slides: 1=Layer2-nuli, 2=Layer1-nuli, 3=Layer2-multi, 4=Layer1-multi

Improvements over previous 1200x1200 version:
  - Export PPTX at higher DPI for better text quality
  - Output 2400x2400 (4:1 pixel density at 600px CSS display)
  - Stronger UnsharpMask sharpening
"""
import os, sys, math, tempfile, shutil
import numpy as np
from PIL import Image, ImageFilter

# ── PPTX & output paths ─────────────────────────────────────────────────────
PPTX = r'C:\Users\ydu\OneDrive - London Business School\0 PhD Life\Job Market\personal website\others\tool design\tool_design_updated.pptx'
OUT_DIR = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel'

# ── Output resolution ────────────────────────────────────────────────────────
OUT_W = OUT_H = 2400   # was 1200

# ── PPTX slide export via PowerPoint COM ────────────────────────────────────
# Export resolution: 720 DPI for 13.33" wide → ~9600px wide
# We'll use a square export at a size that gives sufficient disc coverage.
# PowerPoint COM: Presentation.SaveAs(path, ppSaveAsPNG=18) exports all slides.
# Or use Export(path, filterName, scaleWidth, scaleHeight).

EXPORT_SIZE = 7200   # square export px (was 3600)

# ── Crop parameters (scaled from 1800×1800 base) ─────────────────────────────
# Base (1800×1800): SX=515, SY=217, SW=694, SH=1234
# Scale to EXPORT_SIZE: multiply by EXPORT_SIZE/1800
SCALE = EXPORT_SIZE / 1800
SX = int(round(515 * SCALE))   # 2060
SY = int(round(217 * SCALE))   # 868
SW = int(round(694 * SCALE))   # 2776
SH = int(round(1234 * SCALE))  # 4936

print(f"Export size: {EXPORT_SIZE}x{EXPORT_SIZE}")
print(f"Crop box: SX={SX}, SY={SY}, SW={SW}, SH={SH}")
print(f"Output size: {OUT_W}x{OUT_H}")

# ── Hole positions (from PPTX, same for nuli and multi) ──────────────────────
# (cx_frac, cy_frac, w_frac, h_frac) — ALL values are fractions of slide dimensions
# Derived from python-pptx inspection of tool_design_updated.pptx slide 2:
#   RR15: cx=0.4560 cy=0.1874 w=0.0181 h=0.0219  ("No MWH Stay" hole)
#   RR19: cx=0.5300 cy=0.4029 w=0.0176 h=0.0254  (innermost stay row)
#   RR29: cx=0.5470 cy=0.3843 w=0.0176 h=0.0254
#   RR30: cx=0.5644 cy=0.3663 w=0.0176 h=0.0254
#   RR31: cx=0.5809 cy=0.3487 w=0.0176 h=0.0254
#   RR32: cx=0.5976 cy=0.3317 w=0.0176 h=0.0254  (outermost stay row)
HOLE_SHAPES_FRAC = [
    (0.4560, 0.1874, 0.0181, 0.0219),
    (0.5300, 0.4029, 0.0176, 0.0254),
    (0.5470, 0.3843, 0.0176, 0.0254),
    (0.5644, 0.3663, 0.0176, 0.0254),
    (0.5809, 0.3487, 0.0176, 0.0254),
    (0.5976, 0.3317, 0.0176, 0.0254),
]

def frac_to_px(cx_frac, cy_frac, w_frac, h_frac):
    """Convert PPTX fractional hole coords to pixel coords in OUT_W x OUT_H image."""
    # In EXPORT_SIZE x EXPORT_SIZE square export of a 16:9 slide:
    # x pixels = cx_frac * EXPORT_SIZE  (x-axis compressed by 9/16 vs y-axis)
    # y pixels = cy_frac * EXPORT_SIZE
    cx_exp = cx_frac * EXPORT_SIZE
    cy_exp = cy_frac * EXPORT_SIZE
    w_exp  = w_frac  * EXPORT_SIZE
    h_exp  = h_frac  * EXPORT_SIZE
    # After crop (SX, SY) and resize to OUT_W x OUT_H:
    cx_out = (cx_exp - SX) * (OUT_W / SW)
    cy_out = (cy_exp - SY) * (OUT_H / SH)
    w_out  = w_exp * (OUT_W / SW)
    h_out  = h_exp * (OUT_H / SH)
    return cx_out, cy_out, w_out, h_out

HOLES = [frac_to_px(*h) for h in HOLE_SHAPES_FRAC]

# Disc geometry in output image
CX_OUT = OUT_W // 2   # 1200
CY_OUT = OUT_H // 2   # 1200
# Disc radius in output: slightly inside disc boundary
R_INNER = int(round(510 * OUT_W / 1200))   # 1020 (fully opaque inner zone)
R_OUTER = int(round(536 * OUT_W / 1200))   # 1072 (outer transition zone)


def export_pptx_slides(pptx_path, out_dir, size):
    """Export all slides from PPTX as PNG using PowerPoint COM automation."""
    import comtypes.client
    print("Opening PowerPoint via COM...")
    ppt_app = comtypes.client.CreateObject("PowerPoint.Application")
    ppt_app.Visible = True

    try:
        prs = ppt_app.Presentations.Open(
            os.path.abspath(pptx_path),
            ReadOnly=True,
            Untitled=False,
            WithWindow=False
        )
        n = prs.Slides.Count
        print(f"Presentation opened: {n} slides")
        paths = []
        for i in range(1, n + 1):
            out_path = os.path.join(out_dir, f"slide{i}.png")
            prs.Slides(i).Export(os.path.abspath(out_path), "PNG", size, size)
            print(f"  Exported slide {i} -> {out_path}")
            paths.append(out_path)
        prs.Close()
        return paths
    finally:
        ppt_app.Quit()


def crop_and_resize(src_path, out_path):
    """Crop oval bounding box from exported slide and resize to OUT_W x OUT_H."""
    img = Image.open(src_path).convert('RGBA')
    assert img.size == (EXPORT_SIZE, EXPORT_SIZE), f"Unexpected size: {img.size}"
    cropped = img.crop((SX, SY, SX + SW, SY + SH))
    resized = cropped.resize((OUT_W, OUT_H), Image.LANCZOS)
    return resized


def apply_disc_mask(img_arr):
    """
    Apply two-zone alpha mask for Layer 1:
      r < R_INNER  → fully opaque (alpha = 255)
      R_INNER ≤ r < R_OUTER → gradual transition (white → transparent)
      r ≥ R_OUTER  → fully transparent (alpha = 0)
    Also preserve the 6 holes as fully transparent.
    """
    H, W = img_arr.shape[:2]
    ys, xs = np.mgrid[0:H, 0:W]
    dist = np.sqrt((xs - CX_OUT)**2 + (ys - CY_OUT)**2).astype(float)

    # Start with white opaque disc
    result = np.ones((H, W, 4), dtype=np.uint8) * 255

    # Copy RGB from original
    result[:, :, :3] = img_arr[:, :, :3]

    # Alpha: inner zone fully opaque
    alpha = np.zeros((H, W), dtype=np.uint8)
    alpha[dist < R_INNER] = 255

    # Transition zone: fade to transparent
    t_mask = (dist >= R_INNER) & (dist < R_OUTER)
    t_vals = 1.0 - (dist[t_mask] - R_INNER) / (R_OUTER - R_INNER)
    alpha[t_mask] = (t_vals * 255).astype(np.uint8)

    result[:, :, 3] = alpha

    # Punch 6 transparent holes (core area)
    for (cx, cy, w, h) in HOLES:
        x0 = max(0, int(cx - w / 2) - 2)
        y0 = max(0, int(cy - h / 2) - 2)
        x1 = min(W, int(cx + w / 2) + 2)
        y1 = min(H, int(cy + h / 2) + 2)
        result[y0:y1, x0:x1, 3] = 0

    # Flood-fill outward from each transparent hole through connected near-white pixels.
    # PowerPoint renders shadow/glow effects that extend ~30px beyond shape bounds,
    # leaving visible white borders around holes. Seed only from inner-disc holes
    # (r < R_INNER), not from the outer transparent ring. The colored sectors
    # (blue/teal, R < 230) act as natural barriers so fill stays within the fills.
    WHITE_THRESH = 230  # pixels with all channels > this are "near-white fills"
    ys_f, xs_f = np.mgrid[0:H, 0:W]
    dist_f = np.sqrt((xs_f - CX_OUT)**2 + (ys_f - CY_OUT)**2)
    # Seed: only transparent pixels inside the disc (the 6 punched holes)
    expanding = (result[:, :, 3] == 0) & (dist_f < R_INNER)
    near_white_opaque = (
        (result[:, :, 0] > WHITE_THRESH) &
        (result[:, :, 1] > WHITE_THRESH) &
        (result[:, :, 2] > WHITE_THRESH) &
        (result[:, :, 3] > 0)
    )
    for _ in range(60):  # max 60px expansion
        adj = np.zeros_like(expanding, dtype=bool)
        adj[1:, :]  |= expanding[:-1, :]  # above
        adj[:-1, :] |= expanding[1:, :]   # below
        adj[:, 1:]  |= expanding[:, :-1]  # left
        adj[:, :-1] |= expanding[:, 1:]   # right
        new_t = near_white_opaque & adj
        if not new_t.any():
            break
        result[new_t, 3] = 0
        expanding = new_t  # BFS: only expand from frontier
        near_white_opaque &= ~new_t

    return result


def sharpen(img):
    """Apply UnsharpMask sharpening for crisp text."""
    return img.filter(ImageFilter.UnsharpMask(radius=0.8, percent=160, threshold=2))


def process_layer2(slide_img):
    """Layer 2: static disc — no alpha mask, just crop+resize+sharpen."""
    arr = np.array(slide_img.convert('RGB'))
    out = Image.fromarray(arr, 'RGB')
    return sharpen(out)


def process_layer1(slide_img):
    """Layer 1: apply disc mask + punch holes + sharpen."""
    arr = np.array(slide_img.convert('RGBA'))
    masked = apply_disc_mask(arr)
    img = Image.fromarray(masked, 'RGBA')
    # Sharpen only the RGB channels (preserve alpha)
    rgb = img.convert('RGB')
    rgb_sharp = sharpen(rgb)
    a = img.split()[3]
    result = Image.merge('RGBA', list(rgb_sharp.split()) + [a])
    return result


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp_dir = tempfile.mkdtemp(prefix='sba_slides_')
    print(f"Temporary slide export directory: {tmp_dir}")

    try:
        slide_paths = export_pptx_slides(PPTX, tmp_dir, EXPORT_SIZE)

        if len(slide_paths) < 4:
            print(f"ERROR: expected 4 slides, got {len(slide_paths)}")
            sys.exit(1)

        configs = [
            (slide_paths[0], 'layer2_nuli.png',  'layer2', 'nuli'),
            (slide_paths[1], 'layer1_nuli.png',  'layer1', 'nuli'),
            (slide_paths[2], 'layer2_multi.png', 'layer2', 'multi'),
            (slide_paths[3], 'layer1_multi.png', 'layer1', 'multi'),
        ]

        for src, fname, layer, parity in configs:
            print(f"\nProcessing {fname}...")
            slide_img = crop_and_resize(src, None)

            if layer == 'layer2':
                out_img = process_layer2(slide_img)
                save_path = os.path.join(OUT_DIR, fname)
                out_img.save(save_path, 'PNG', optimize=False)
            else:
                out_img = process_layer1(slide_img)
                save_path = os.path.join(OUT_DIR, fname)
                out_img.save(save_path, 'PNG', optimize=False)

            sz = os.path.getsize(save_path) // 1024
            print(f"  Saved {save_path} ({out_img.size[0]}x{out_img.size[1]}, {sz} KB)")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("\nDone! All 4 images generated at 2400x2400.")
    print("Next: update sba-wheel.html (canvas 2400x2400) and sba-wheel.js (W=2400).")


if __name__ == '__main__':
    main()
