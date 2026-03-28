"""
Generate a preview of the wheel at selected=18 to see what it looks like.
Also verify the disc center and mask alignment.
"""
import numpy as np
from PIL import Image
import math

L2 = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer2_nuli.png'
L1 = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'
OUT = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\preview_composite.png'

W = 2400
CX = CY = 1200
N = 22
ASTEP = 2 * math.pi / N
A0 = -math.pi / 2
DEFAULT_ANGLE = -2.552613
selected = 18

rotation = (A0 + selected * ASTEP + ASTEP / 2) - DEFAULT_ANGLE
print(f"Rotation for selected={selected}: {math.degrees(rotation):.2f} deg")

# Load images
l2 = Image.open(L2).convert('RGBA')
l1 = Image.open(L1).convert('RGBA')
print(f"Layer 2 size: {l2.size}")
print(f"Layer 1 size: {l1.size}")

# Check alpha channel of Layer 1
l1_arr = np.array(l1)
A = l1_arr[:, :, 3]
ys, xs = np.mgrid[0:W, 0:W]
dist = np.sqrt((xs - CX)**2 + (ys - CY)**2)
inner = dist < 1020
print(f"\nLayer 1 inner disc (r<1020) transparent pixels: {np.sum(inner & (A < 50)):,}")
print(f"Layer 1 inner disc opaque pixels: {np.sum(inner & (A > 200)):,}")

# Composite: draw L2, then rotate L1 and draw on top
canvas = l2.copy().convert('RGBA')
l1_rotated = l1.rotate(math.degrees(-rotation), resample=Image.BICUBIC, expand=False)

# Composite
canvas.paste(l1_rotated, (0, 0), l1_rotated)

# Save at 600x600 for quick viewing
out_small = canvas.resize((600, 600), Image.LANCZOS).convert('RGB')
out_small.save(OUT)
print(f"\nComposite preview saved: {OUT}")
print(f"(Rotation: {math.degrees(rotation):.1f} deg = {math.degrees(-rotation):.1f} deg for PIL rotate)")
