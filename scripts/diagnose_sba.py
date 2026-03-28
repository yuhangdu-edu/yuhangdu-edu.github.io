"""
Diagnose the layer1_nuli.png: check alpha channel and hole sizes.
"""
import numpy as np
from PIL import Image
import math

IMG = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'

img = Image.open(IMG).convert('RGBA')
W, H = img.size
CX, CY = W // 2, H // 2
arr = np.array(img)
A = arr[:, :, 3]

ys, xs = np.mgrid[0:H, 0:W]
dist = np.sqrt((xs - CX)**2 + (ys - CY)**2)

print(f"Image size: {W}x{H}")
print(f"Total pixels: {W*H:,}")

# Alpha statistics
n_opaque = np.sum(A > 200)
n_transparent = np.sum(A < 50)
n_partial = np.sum((A >= 50) & (A <= 200))
print(f"\nAlpha channel:")
print(f"  Opaque (A>200): {n_opaque:,} = {n_opaque/W/H*100:.1f}%")
print(f"  Transparent (A<50): {n_transparent:,} = {n_transparent/W/H*100:.1f}%")
print(f"  Partial: {n_partial:,} = {n_partial/W/H*100:.1f}%")

# Disc coverage
disc_mask = dist < 1168
disc_pixels = np.sum(disc_mask)
disc_opaque = np.sum(disc_mask & (A > 200))
print(f"\nWithin disc (r<1168):")
print(f"  Total: {disc_pixels:,}")
print(f"  Opaque (A>200): {disc_opaque:,} = {disc_opaque/disc_pixels*100:.1f}%")
print(f"  Transparent (A<50): {np.sum(disc_mask & (A<50)):,}")

# Where are the transparent pixels within the disc?
inner = dist < 1020
inner_transparent = np.sum(inner & (A < 50))
print(f"\nInner disc (r<1020) transparent pixels: {inner_transparent:,}")
if inner_transparent > 0:
    print("  WARNING: There are unexpected transparent pixels inside r=1020!")
    # Where are they? Find their centroid
    ty = ys[inner & (A < 50)]
    tx = xs[inner & (A < 50)]
    print(f"  Centroid: ({np.mean(tx):.0f}, {np.mean(ty):.0f})")
    print(f"  x range: {tx.min()}-{tx.max()}, y range: {ty.min()}-{ty.max()}")

# Check the 6 holes - how big are they?
print("\nHole analysis (expected 6 rectangular transparent areas):")
# Find clusters of transparent pixels inside disc
trans_inside = inner & (A < 50)
print(f"Transparent pixels inside r=1020: {np.sum(trans_inside):,}")

# Radial sectors with most transparency
print("\nAngular distribution of transparent pixels inside r=1020:")
angles = np.arctan2(ys - CY, xs - CX)
bins = np.linspace(-math.pi, math.pi, 37)
hist, edges = np.histogram(angles[trans_inside], bins=bins)
for i in range(len(hist)):
    if hist[i] > 100:
        a_mid = math.degrees((edges[i]+edges[i+1])/2)
        print(f"  {a_mid:7.1f} deg: {hist[i]:6d} transparent pixels")
