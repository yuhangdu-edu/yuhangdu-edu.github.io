"""
Empirically find the arrow tip position in layer1_nuli.png
and compute DEFAULT_ANGLE for sba-wheel.js.
"""
import numpy as np
from PIL import Image
import math

IMG = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'

img = Image.open(IMG).convert('RGBA')
W, H = img.size
CX, CY = W // 2, H // 2

arr = np.array(img)  # shape (H, W, 4)
R = arr[:, :, 0].astype(int)
G = arr[:, :, 1].astype(int)
B = arr[:, :, 2].astype(int)
A = arr[:, :, 3].astype(int)

print(f"Image size: {W}x{H}, centre: ({CX},{CY})")

# Compute radius from centre for every pixel
ys, xs = np.mgrid[0:H, 0:W]
dist = np.sqrt((xs - CX)**2 + (ys - CY)**2)

# Identify "arrow" pixels:
#   - opaque (alpha > 128)
#   - NOT white/near-white (to exclude the disc body)
#   - NOT in the 6-hole transparent region (alpha already 0)
# The arrow is colored (non-white opaque).  Use saturation: max(RGB)-min(RGB) > threshold.
rgb_max = np.maximum(np.maximum(R, G), B)
rgb_min = np.minimum(np.minimum(R, G), B)
saturation = (rgb_max - rgb_min).astype(float)

# Also detect dark (non-white) pixels — the arrow outline may be dark grey
brightness = (R + G + B) / 3.0

# Arrow pixels: opaque AND (colorful OR dark)
arrow_mask = (A > 128) & ((saturation > 20) | (brightness < 180))

n_arrow = np.sum(arrow_mask)
print(f"Arrow pixels found: {n_arrow}")

if n_arrow == 0:
    print("No arrow pixels found — check thresholds")
else:
    # Find the pixel furthest from centre (the TIP of the arrow)
    arrow_dist = dist * arrow_mask  # 0 for non-arrow pixels
    tip_flat = np.argmax(arrow_dist)
    tip_y, tip_x = np.unravel_index(tip_flat, (H, W))
    tip_r = dist[tip_y, tip_x]
    tip_angle = math.atan2(tip_y - CY, tip_x - CX)

    print(f"\nArrow TIP pixel: ({tip_x}, {tip_y})")
    print(f"  Radial distance from centre: {tip_r:.1f} px")
    print(f"  Angle from centre: {tip_angle:.6f} rad  ({math.degrees(tip_angle):.2f} deg)")

    # Also compute centroid of arrow pixels
    ys_a = ys[arrow_mask]
    xs_a = xs[arrow_mask]
    cy_c = np.mean(ys_a)
    cx_c = np.mean(xs_a)
    centroid_angle = math.atan2(cy_c - CY, cx_c - CX)
    print(f"\nArrow CENTROID: ({cx_c:.1f}, {cy_c:.1f})")
    print(f"  Angle from centre: {centroid_angle:.6f} rad  ({math.degrees(centroid_angle):.2f} deg)")

    # Print a few sample arrow pixels near the tip
    print(f"\nSample pixels near tip (top-10 by radial distance):")
    flat_idx = np.argsort(-arrow_dist.ravel())[:20]
    seen = set()
    count = 0
    for fi in flat_idx:
        py, px = np.unravel_index(fi, (H, W))
        ang = math.degrees(math.atan2(py - CY, px - CX))
        if count < 10:
            print(f"  ({px:4d},{py:4d}) r={dist[py,px]:6.1f}  "
                  f"RGBA=({arr[py,px,0]:3d},{arr[py,px,1]:3d},{arr[py,px,2]:3d},{arr[py,px,3]:3d})  "
                  f"angle={ang:.2f}°")
            count += 1

    print(f"\n==> Suggested DEFAULT_ANGLE (tip) = {tip_angle:.6f}")
    print(f"==> Suggested DEFAULT_ANGLE (centroid) = {centroid_angle:.6f}")
    print(f"\nCurrent DEFAULT_ANGLE in JS = -2.673061  ({math.degrees(-2.673061):.2f} deg)")
