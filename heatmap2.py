import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from PIL import Image as PILImage

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("wifi_processed_with_coordinates.csv")
x = df["X"].values
y = df["Y"].values
z = df["Average"].values

# ── Load floor plan ───────────────────────────────────────────────────────────
pil_img = PILImage.open("floorplan.png").convert("RGB")
img = np.array(pil_img)
IMG_H, IMG_W = img.shape[:2]

# ── Calibration ───────────────────────────────────────────────────────────────
LEFT_PX   = 7
RIGHT_PX  = 587
TOP_PX    = 8
BOTTOM_PX = 712
FLOOR_W   = 18.0
FLOOR_H   = 22.0

scale_x = FLOOR_W / (RIGHT_PX - LEFT_PX)
scale_y = FLOOR_H / (BOTTOM_PX - TOP_PX)

x_min_m = -LEFT_PX * scale_x
x_max_m = (IMG_W - LEFT_PX) * scale_x
y_min_m = -(IMG_H - BOTTOM_PX) * scale_y
y_max_m = (BOTTOM_PX - TOP_PX) * scale_y + y_min_m

# ── Interpolation ─────────────────────────────────────────────────────────────
xi = np.linspace(0, FLOOR_W, 600)
yi = np.linspace(0, FLOOR_H, 600)
xi, yi = np.meshgrid(xi, yi)
zi = griddata((x, y), z, (xi, yi), method="cubic")

# ── Figure ────────────────────────────────────────────────────────────────────
fig_h = 13
fig_w = fig_h * (IMG_W / IMG_H)
fig, ax = plt.subplots(figsize=(fig_w, fig_h))

# 1. Floor plan background
ax.imshow(img, extent=[x_min_m, x_max_m, y_min_m, y_max_m],
          origin="upper", aspect="equal", zorder=0)

# 2. Heatmap overlay
heatmap = ax.contourf(xi, yi, zi, levels=20, cmap="RdYlGn", alpha=0.50, zorder=1)
cbar = plt.colorbar(heatmap, ax=ax, pad=0.02, fraction=0.03)
cbar.set_label("RSSI (dBm)", fontsize=11)

# 3. Router only
ROUTER_X, ROUTER_Y = 9.5, 6.5
ax.plot(ROUTER_X, ROUTER_Y, marker="*", color="blue",
        markersize=18, zorder=5, label="WiFi Router", linestyle="None")
ax.annotate("Router", (ROUTER_X, ROUTER_Y),
            xytext=(ROUTER_X + 0.3, ROUTER_Y + 0.4),
            fontsize=9, color="blue", fontweight="bold")

# 4. Axes
ax.set_xlim(0, FLOOR_W)
ax.set_ylim(0, FLOOR_H)
ax.set_xlabel("X (m)", fontsize=11)
ax.set_ylabel("Y (m)", fontsize=11)
ax.set_title("WiFi Coverage Heatmap — 18m × 22m Floor Plan", fontsize=13, fontweight="bold")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.12)

plt.tight_layout()
plt.savefig("wifi_heatmap_on_floorplan.png", dpi=300, bbox_inches="tight")
print("Saved.")
plt.show()