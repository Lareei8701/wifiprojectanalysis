import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Read processed data
df = pd.read_csv("wifi_processed_with_coordinates.csv")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Read processed data
df = pd.read_csv("wifi_processed_with_coordinates.csv")

x = df["X"].values
y = df["Y"].values
z = df["Average"].values

# Create grid
xi = np.linspace(0, 18, 400)
yi = np.linspace(0, 22, 400)
xi, yi = np.meshgrid(xi, yi)

# Interpolation
zi = griddata((x, y), z, (xi, yi), method="cubic")

plt.figure(figsize=(10, 12))

heatmap = plt.contourf(xi, yi, zi, levels=20, cmap="RdYlGn")
cbar = plt.colorbar(heatmap)
cbar.set_label("RSSI Signal Strength (dBm)")

plt.scatter(x, y, c="black", s=18, label="Measurement Points")

# Label only important points to reduce crowding
important_points = ["P19", "P51", "P12", "P20", "P26", "P27", "P48", "P50", "P54", "P56"]

for _, row in df.iterrows():
    if row["Point"] in important_points:
        plt.text(row["X"], row["Y"], row["Point"], fontsize=9, fontweight="bold")

plt.xlabel("X Coordinate (m)")
plt.ylabel("Y Coordinate (m)")
plt.title("WiFi Coverage Heatmap Based on Average RSSI")
plt.xlim(0, 18)
plt.ylim(0, 22)
plt.legend(loc="upper right")
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig("wifi_heatmap_final.png", dpi=300)
plt.show()