"""
Better arrow detection: find unique color clusters in layer1_nuli.png
to identify the actual arrow indicator shape.
"""
import numpy as np
from PIL import Image
import math

IMG = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'

img = Image.open(IMG).convert('RGBA')
W, H = img.size
CX, CY = W // 2, H // 2
arr = np.array(img)

R = arr[:, :, 0].astype(int)
G = arr[:, :, 1].astype(int)
B = arr[:, :, 2].astype(int)
A = arr[:, :, 3].astype(int)

ys, xs = np.mgrid[0:H, 0:W]
dist = np.sqrt((xs - CX)**2 + (ys - CY)**2)

# Focus inside the disc (r < 530 to stay well inside disc boundary)
inside_disc = (A > 200) & (dist < 530)

# Saturation in HSV sense: (max-min)/max
rgb_max = np.maximum(np.maximum(R, G), B).astype(float)
rgb_min = np.minimum(np.minimum(R, G), B).astype(float)
saturation = np.where(rgb_max > 0, (rgb_max - rgb_min) / rgb_max, 0)
brightness = (R + G + B) / 3.0

print("=== Color analysis inside disc ===")
# Histogram of saturation for opaque pixels inside disc
sat_vals = saturation[inside_disc]
print(f"Pixels inside disc: {np.sum(inside_disc)}")
print(f"Saturation distribution:")
for threshold in [0.05, 0.10, 0.20, 0.30, 0.40, 0.50]:
    count = np.sum(sat_vals > threshold)
    print(f"  sat > {threshold:.2f}: {count:8d} pixels")

# Find highly saturated pixels (the arrow and possibly the colored wedges visible through holes)
# Exclude very bright pixels (near white) since we want the colored/dark arrow
sat_mask = inside_disc & (saturation > 0.25) & (brightness < 230)

print(f"\nHighly saturated + not too bright: {np.sum(sat_mask)} pixels")

if np.sum(sat_mask) > 0:
    # Print top colors
    sat_pixels = arr[sat_mask]
    print("Sample colors (R,G,B,A):")
    # Quantize to 32-level and find top colors
    quantized = (sat_pixels[:, :3] // 32)
    unique, counts = np.unique(quantized, axis=0, return_counts=True)
    order = np.argsort(-counts)
    for i in order[:10]:
        approx_color = unique[i] * 32 + 16
        print(f"  RGB~({approx_color[0]:3d},{approx_color[1]:3d},{approx_color[2]:3d}): {counts[i]:6d} pixels")

# Try to detect the arrow by looking for a DARK region (the arrow outline/body)
# Arrow in PPTX designs often uses a dark or bold color
dark_mask = inside_disc & (brightness < 150) & (dist > 50)  # dark, inside disc, not at very center
print(f"\nDark pixels (brightness<150) inside disc: {np.sum(dark_mask)}")

# Non-white colored (moderate saturation)
colored_mask = inside_disc & (saturation > 0.10) & (brightness < 200)
print(f"Colored (sat>0.10, bright<200) inside disc: {np.sum(colored_mask)}")

# Let's look at all pixels at various radial distances
print("\n=== Radial scan for colored pixels ===")
for r_lo, r_hi in [(50,100),(100,150),(150,200),(200,250),(250,300),(300,350),(350,400),(400,450),(450,500)]:
    ring_mask = inside_disc & (dist >= r_lo) & (dist < r_hi) & (saturation > 0.10)
    n = np.sum(ring_mask)
    if n > 0:
        avg_r = np.mean(R[ring_mask])
        avg_g = np.mean(G[ring_mask])
        avg_b = np.mean(B[ring_mask])
        print(f"  r={r_lo:3d}-{r_hi:3d}: {n:6d} colored pixels, avg color ({avg_r:.0f},{avg_g:.0f},{avg_b:.0f})")
    else:
        print(f"  r={r_lo:3d}-{r_hi:3d}: 0 colored pixels")

# Look for the specific triangle arrow: it should be near where DEFAULT_ANGLE points
# Current DEFAULT_ANGLE = -2.673061 → pointing toward upper-left
# Let's scan a wedge around that direction
print("\n=== Wedge scan around expected arrow direction (-2.67 rad = -153°) ===")
angles = np.arctan2(ys - CY, xs - CX)
for a_center in [-2.673061, -2.5, -2.8, -3.0, -2.3, -2.0, -1.5, -1.0]:
    da = 0.2  # ±0.2 rad wedge
    wedge = inside_disc & (np.abs(angles - a_center) < da) & (saturation > 0.05)
    n = np.sum(wedge)
    if n > 0:
        avg_bright = np.mean(brightness[wedge])
        avg_sat = np.mean(saturation[wedge])
        avg_r = np.mean(R[wedge])
        avg_g = np.mean(G[wedge])
        avg_b = np.mean(B[wedge])
        print(f"  angle={math.degrees(a_center):7.1f}°: {n:6d} pixels, brightness={avg_bright:.0f}, sat={avg_sat:.3f}, color=({avg_r:.0f},{avg_g:.0f},{avg_b:.0f})")

print("\n=== Let's find the actual arrow by scanning for the most distinct color cluster ===")
# The arrow is likely the ONLY non-hole colored feature
# Compute angle for ALL opaque inside-disc pixels that are somewhat colored
all_colored = inside_disc & (saturation > 0.08)
if np.sum(all_colored) > 0:
    # Compute angle histogram (36 bins × 10°)
    angle_vals = np.arctan2((ys - CY)[all_colored], (xs - CX)[all_colored])
    bins = np.linspace(-math.pi, math.pi, 37)
    hist, edges = np.histogram(angle_vals, bins=bins)
    print("Angle histogram of colored pixels (10° bins):")
    for i in range(len(hist)):
        a_deg = math.degrees((edges[i] + edges[i+1]) / 2)
        bar = '#' * min(50, hist[i] // 200)
        print(f"  {a_deg:7.1f}°: {hist[i]:6d} {bar}")
