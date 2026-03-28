"""
Find the arrow specifically: look for the dark-blue pointed shape in Layer 1.
The arrow (Triangle 6 in PPTX) should be a dark/saturated colored region
NOT coinciding with the 6 transparent holes.
"""
import numpy as np
from PIL import Image, ImageDraw
import math

IMG = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\layer1_nuli.png'
OUT = r'c:\Users\ydu\Documents\GitHub\yuhangdu-edu.github.io\assets\images\sba-wheel\arrow_debug.png'

img = Image.open(IMG).convert('RGBA')
W, H = img.size
CX, CY = W // 2, H // 2
arr = np.array(img)

R = arr[:, :, 0].astype(float)
G = arr[:, :, 1].astype(float)
B = arr[:, :, 2].astype(float)
A = arr[:, :, 3].astype(float)

ys, xs = np.mgrid[0:H, 0:W]
dist = np.sqrt((xs - CX)**2 + (ys - CY)**2)
angles = np.arctan2(ys - CY, xs - CX)

# Disc body: opaque pixels inside disc boundary
inside_disc = (A > 200) & (dist < 520)

# The arrow is specifically the dark blue/navy triangle shape
# From sample: (37,69,238) and (37,59,247) - dark blue
# Criteria: B > R+G (more blue than sum of others), NOT too bright
blue_dominant = (B > 150) & (B > R + 50) & (B > G + 50)
arrow_mask = inside_disc & blue_dominant

print(f"Blue-dominant pixels inside disc: {np.sum(arrow_mask)}")

if np.sum(arrow_mask) > 0:
    ay = ys[arrow_mask].astype(float)
    ax = xs[arrow_mask].astype(float)
    ad = dist[arrow_mask]

    # Centroid angle
    cy_c = np.mean(ay) - CY
    cx_c = np.mean(ax) - CX
    centroid_angle = math.atan2(cy_c, cx_c)

    # Tip: pixel furthest from center
    tip_idx = np.argmax(ad)
    tip_x = ax[tip_idx]
    tip_y = ay[tip_idx]
    tip_angle = math.atan2(tip_y - CY, tip_x - CX)

    print(f"Arrow centroid: ({cx_c + CX:.1f}, {cy_c + CY:.1f})")
    print(f"  Centroid angle: {centroid_angle:.6f} rad = {math.degrees(centroid_angle):.2f} deg")
    print(f"Arrow tip: ({tip_x:.0f}, {tip_y:.0f}), r={ad[tip_idx]:.1f}")
    print(f"  Tip angle: {tip_angle:.6f} rad = {math.degrees(tip_angle):.2f} deg")
    print(f"\nCurrent DEFAULT_ANGLE = -2.673061 rad = {math.degrees(-2.673061):.2f} deg")
    print(f"Difference (centroid): {centroid_angle - (-2.673061):.4f} rad = {math.degrees(centroid_angle - (-2.673061)):.2f} deg")

    # Also look for the outermost cluster in that direction
    # Filter to pixels in a wedge around centroid_angle
    da = 0.35  # +-20 deg
    wedge = arrow_mask & (np.abs(angles - centroid_angle) < da)
    print(f"\nPixels in wedge +-20 deg around centroid: {np.sum(wedge)}")
    if np.sum(wedge) > 0:
        wd = dist[wedge]
        wy = ys[wedge].astype(float)
        wx = xs[wedge].astype(float)
        # Find the "tip" cluster: outermost 10% of pixels
        threshold = np.percentile(wd, 90)
        outer = wedge & (dist >= threshold)
        if np.sum(outer) > 0:
            oy = np.mean(ys[outer].astype(float))
            ox = np.mean(xs[outer].astype(float))
            outer_angle = math.atan2(oy - CY, ox - CX)
            print(f"Outer-10% tip centroid: ({ox:.1f}, {oy:.1f})")
            print(f"  Outer tip angle: {outer_angle:.6f} rad = {math.degrees(outer_angle):.2f} deg")
            print(f"\n==> Recommended DEFAULT_ANGLE = {outer_angle:.6f}")

# Create debug visualization
debug = img.copy().convert('RGB')
debug_arr = np.array(debug)

# Highlight arrow pixels in red
debug_arr[arrow_mask, 0] = 255
debug_arr[arrow_mask, 1] = 0
debug_arr[arrow_mask, 2] = 0

# Draw centre cross
draw = ImageDraw.Draw(Image.fromarray(debug_arr))
# Save the debug image
from PIL import Image as PILImage
debug_img = PILImage.fromarray(debug_arr)
draw = ImageDraw.Draw(debug_img)
draw.line([(CX-30, CY), (CX+30, CY)], fill=(0,255,0), width=3)
draw.line([(CX, CY-30), (CX, CY+30)], fill=(0,255,0), width=3)

# Draw line at DEFAULT_ANGLE
da_rad = -2.673061
for r_step in range(0, 400, 5):
    px = int(CX + r_step * math.cos(da_rad))
    py = int(CY + r_step * math.sin(da_rad))
    if 0 <= px < W and 0 <= py < H:
        if debug_arr[py, px, 0] != 255:  # don't overwrite arrow highlight
            draw.point([(px, py)], fill=(255, 255, 0))

debug_img.save(OUT)
print(f"\nDebug image saved to: {OUT}")
print("(Arrow highlighted red, DEFAULT_ANGLE direction in yellow)")
