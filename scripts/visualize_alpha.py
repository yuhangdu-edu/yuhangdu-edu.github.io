"""
Visualize Layer 1 alpha channel: white=opaque, black=transparent.
Also generate a corrected composite to see actual wheel appearance.
"""
import numpy as np
from PIL import Image, ImageDraw
import math

L1 = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'
L2 = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer2_nuli.png'
OUT_ALPHA = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\debug_alpha.png'
OUT_COMP = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\debug_composite.png'

l1 = Image.open(L1).convert('RGBA')
l2 = Image.open(L2).convert('RGBA')
W, H = l1.size
CX, CY = W//2, H//2
l1_arr = np.array(l1)
A = l1_arr[:, :, 3]

# Alpha visualization (white=opaque, black=transparent)
alpha_vis = Image.fromarray(A, 'L')
alpha_vis.save(OUT_ALPHA)
print(f"Alpha visualization saved: {OUT_ALPHA}")

# Count opaque vs transparent
print(f"Alpha=0 (transparent): {np.sum(A==0):,}")
print(f"Alpha=255 (opaque): {np.sum(A==255):,}")
print(f"Alpha in between: {np.sum((A>0)&(A<255)):,}")

# Show alpha at specific positions
test_points = [
    (1200, 600, "top center"),
    (1600, 400, "upper right"),
    (1200, 1200, "center"),
    (800, 800, "upper left"),
    (1058, 234, "hole 1 center"),
    (1519, 988, "hole 2 center"),
]
print("\nAlpha at specific positions:")
for (x, y, label) in test_points:
    if 0 <= x < W and 0 <= y < H:
        print(f"  ({x:4d},{y:4d}) {label}: alpha={A[y,x]}")

# Generate proper composite using canvas-like rendering
# White background
canvas = Image.new('RGBA', (W, H), (255, 255, 255, 255))
# Draw Layer 2
canvas.paste(l2, (0, 0), l2.split()[3])
# Draw Layer 1 (no rotation for natural position)
canvas.paste(l1, (0, 0), l1.split()[3])

# Save at 600x600
out_small = canvas.resize((600, 600), Image.LANCZOS).convert('RGB')
out_small.save(OUT_COMP)
print(f"\nComposite (no rotation) saved: {OUT_COMP}")
