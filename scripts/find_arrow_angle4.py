"""
Precise arrow detection: analyze layer1_nuli.png carefully.
Save a debug image showing what the non-white non-transparent pixels look like.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

IMG = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'
OUT_DEBUG = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\arrow_debug2.png'

img = Image.open(IMG).convert('RGBA')
W, H = img.size
CX, CY = W // 2, H // 2
arr = np.array(img, dtype=float)

R, G, B, A = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

ys, xs = np.mgrid[0:H, 0:W]
dist = np.sqrt((xs - CX)**2 + (ys - CY)**2)
angles = np.arctan2(ys - CY, xs - CX)

# ── Find the arrow by looking at the disc's INNER area (exclude border ring)
# Border ring is at r > 490 (outer 30px of disc).
# Arrow body should be at r = 100-490.

inner_disc = (A > 200) & (dist >= 80) & (dist <= 490)

# Color deviation from white (255,255,255):
deviation = np.sqrt((R-255)**2 + (G-255)**2 + (B-255)**2)

# Arrow pixels: opaque, inner disc, not white
non_white = inner_disc & (deviation > 30)

print(f"Non-white pixels in inner disc (r=80-490): {np.sum(non_white)}")

# Also look at just very saturated colored pixels
rgb_max = np.maximum(np.maximum(R, G), B)
rgb_min = np.minimum(np.minimum(R, G), B)
saturation = np.where(rgb_max > 0, (rgb_max - rgb_min) / rgb_max, 0.0)

colored = inner_disc & (saturation > 0.20) & (A > 200)
print(f"Colored (sat>0.20) pixels in inner disc: {np.sum(colored)}")

dark_colored = inner_disc & (saturation > 0.15) & (np.mean([R, G, B], axis=0) < 200)
print(f"Dark+colored (sat>0.15, bright<200) pixels: {np.sum(dark_colored)}")

# Angle distribution of dark+colored pixels
if np.sum(dark_colored) > 0:
    ang_dc = angles[dark_colored]
    # Fine 2-degree bins
    bins = np.linspace(-math.pi, math.pi, 181)
    hist, edges = np.histogram(ang_dc, bins=bins)
    print("\nAngle histogram of dark+colored inner disc pixels (2-deg bins, top 20):")
    top_bins = np.argsort(-hist)[:20]
    for bi in sorted(top_bins):
        a_lo = math.degrees(edges[bi])
        a_hi = math.degrees(edges[bi+1])
        print(f"  {a_lo:8.1f}° to {a_hi:7.1f}°: {hist[bi]:5d}")

# Find the centroid of dark+colored pixels
if np.sum(dark_colored) > 0:
    dy = np.mean(ys[dark_colored].astype(float)) - CY
    dx = np.mean(xs[dark_colored].astype(float)) - CX
    centroid_ang = math.atan2(dy, dx)
    print(f"\nDark+colored centroid: ({dx+CX:.1f}, {dy+CY:.1f}), angle={math.degrees(centroid_ang):.2f} deg = {centroid_ang:.6f} rad")

# ── Identify connected components by color similarity
# The arrow is likely a single connected region of similar blue/dark color
# Let's find the largest connected component of dark+colored pixels

# Create binary mask
mask = dark_colored.astype(np.uint8)

# Simple connected component labeling using scipy
try:
    from scipy import ndimage
    labeled, n_labels = ndimage.label(mask)
    print(f"\nConnected components of dark+colored pixels: {n_labels}")
    if n_labels > 0:
        sizes = ndimage.sum(mask, labeled, range(1, n_labels+1))
        print(f"Component sizes (top 10): {sorted(sizes, reverse=True)[:10]}")
        largest_label = np.argmax(sizes) + 1
        largest_comp = (labeled == largest_label)
        n_lc = np.sum(largest_comp)
        lc_y = np.mean(ys[largest_comp].astype(float))
        lc_x = np.mean(xs[largest_comp].astype(float))
        lc_ang = math.atan2(lc_y - CY, lc_x - CX)
        lc_r = math.sqrt((lc_x-CX)**2 + (lc_y-CY)**2)
        print(f"Largest component: {n_lc} pixels, centroid=({lc_x:.1f},{lc_y:.1f}), r={lc_r:.1f}")
        print(f"  Angle = {math.degrees(lc_ang):.2f} deg = {lc_ang:.6f} rad")
        print(f"\n==> Recommended DEFAULT_ANGLE = {lc_ang:.6f} (from largest component centroid)")
except ImportError:
    print("scipy not available")

# ── Save debug visualization (downscaled to 600x600 for easy viewing)
scale = 2  # output at 600x600 from 1200x1200
out_w, out_h = W // scale, H // scale
debug = Image.new('RGB', (out_w, out_h), (200, 200, 200))

# Paste the original image (as RGB, white background where transparent)
orig_rgb = Image.new('RGB', (W, H), (255, 255, 255))
orig_rgb.paste(img, mask=img.split()[3])
debug.paste(orig_rgb.resize((out_w, out_h), Image.LANCZOS))
debug_arr = np.array(debug)

# Overlay dark+colored pixels in red
dc_small = dark_colored[::scale, ::scale]
debug_arr[dc_small, 0] = 255
debug_arr[dc_small, 1] = 0
debug_arr[dc_small, 2] = 0

# Draw lines for different angle candidates
draw = ImageDraw.Draw(Image.fromarray(debug_arr))
angles_to_draw = [
    (-2.673061, (255, 165, 0), "Current -153.2"),   # orange = current
    (-2.552613, (255, 255, 0), "Centroid -146.3"),  # yellow
]
img_out = Image.fromarray(debug_arr)
draw = ImageDraw.Draw(img_out)
for (ang, color, label) in angles_to_draw:
    for r in range(0, 280, 3):
        px = int(CX/scale + r * math.cos(ang))
        py = int(CY/scale + r * math.sin(ang))
        if 0 <= px < out_w and 0 <= py < out_h:
            draw.point([(px, py)], fill=color)

# Green cross at center
cx2, cy2 = CX//scale, CY//scale
draw.line([(cx2-15, cy2), (cx2+15, cy2)], fill=(0,255,0), width=2)
draw.line([(cx2, cy2-15), (cx2, cy2+15)], fill=(0,255,0), width=2)

img_out.save(OUT_DEBUG)
print(f"\nDebug image saved: {OUT_DEBUG}")
print("Red=dark+colored pixels, Orange=current DEFAULT_ANGLE, Yellow=centroid angle")
