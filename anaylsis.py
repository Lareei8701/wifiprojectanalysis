import pandas as pd

# Read CSV file
df = pd.read_csv("data.csv")

# Clean column names from hidden spaces
df.columns = df.columns.str.strip()

# Show columns to make sure names are correct
print("Columns:")
print(df.columns)

# Calculate Average again from the 3 readings
df["Average"] = df[["Reading1", "Reading2", "Reading3"]].mean(axis=1)

# Classify signal quality
def classify_signal(rssi):
    if rssi >= -60:
        return "Excellent"
    elif rssi >= -70:
        return "Good"
    elif rssi >= -80:
        return "Fair"
    else:
        return "Poor"

df["Quality"] = df["Average"].apply(classify_signal)

# Strongest and weakest points
strongest = df.loc[df["Average"].idxmax()]
weakest = df.loc[df["Average"].idxmin()]

print("\nFirst 5 rows:")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nStrongest signal point:")
print(strongest)

print("\nWeakest signal point:")
print(weakest)

print("\nSignal quality count:")
print(df["Quality"].value_counts())

print("\nOverall average RSSI:")
print(round(df["Average"].mean(), 2), "dBm")

# Save processed file
df.to_csv("data_processed.csv", index=False)

print("\nProcessed file saved as data_processed.csv")

# Coordinates for each measurement point
coords = {
    "P1": (0.0002, 0.0004), "P2": (3.0002, 0.0004), "P3": (6.0002, 0.0004),
    "P4": (9.0002, 0.0004), "P5": (12.0002, 0.0004), "P6": (15.0002, 0.0004),
    "P7": (18.0002, 0.0004),

    "P8": (0.0002, 3.0004), "P9": (3.0002, 3.0004), "P10": (6.0002, 3.0004),
    "P11": (9.0002, 3.0004), "P12": (12.0002, 3.0004), "P13": (15.0002, 3.0004),
    "P14": (18.0002, 3.0004),

    "P15": (0.0002, 6.0004), "P16": (3.0002, 6.0004), "P17": (6.0002, 6.0004),
    "P18": (9.0002, 6.0004), "P19": (12.0002, 6.0004), "P20": (15.0002, 6.0004),
    "P21": (18.0002, 6.0004),

    "P22": (0.5162, 8.1022), "P23": (3.0002, 9.0004), "P24": (6.0002, 9.0004),
    "P25": (9.0002, 9.0004), "P26": (12.0002, 9.0004), "P27": (15.0002, 9.0004),
    "P28": (18.0002, 9.0004),

    "P29": (1.8167, 12.0004), "P30": (3.0002, 12.0004), "P31": (6.0002, 12.0004),
    "P32": (9.0002, 12.0004), "P33": (12.0002, 12.0004), "P34": (15.0002, 12.0004),
    "P35": (18.0002, 12.0004),

    "P36": (0.0002, 15.0004), "P37": (3.0002, 15.0004), "P38": (6.0002, 15.0004),
    "P39": (9.0002, 15.0004), "P40": (12.0002, 15.0004), "P41": (15.0002, 15.0004),
    "P42": (18.0002, 15.0004),

    "P43": (0.0002, 18.0004), "P44": (3.0002, 18.0004), "P45": (6.0002, 18.0004),
    "P46": (9.0002, 18.0004), "P47": (12.0002, 18.0004), "P48": (15.0002, 18.0004),
    "P49": (18.0002, 18.0004),

    "P50": (0.0002, 21.0004), "P51": (3.0002, 21.0004), "P52": (4.2932, 21.0004),
    "P53": (10.3423, 18.0004), "P54": (12.7175, 21.0004),
    "P55": (15.0002, 21.0004), "P56": (18.0002, 21.0004)
}

df["X"] = df["Point"].map(lambda p: coords[p][0])
df["Y"] = df["Point"].map(lambda p: coords[p][1])

print("\nData with coordinates:")
print(df.head())

df.to_csv("wifi_processed_with_coordinates.csv", index=False)

print("\nFile saved as wifi_processed_with_coordinates.csv")