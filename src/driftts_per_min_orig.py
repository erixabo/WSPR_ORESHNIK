import pandas as pd
import matplotlib.pyplot as plt

# Beolvasás
df = pd.read_csv("wspr_20241121_0200_0500.csv")

# Idő oszlop konvertálása
df["time"] = pd.to_datetime(df["time"])

# Átlagos drift percenként
drift_time = df.groupby(pd.Grouper(key="time", freq="1min"))["drift"].mean()

# Ábrázolás
plt.figure(figsize=(12,6))
plt.plot(drift_time.index, drift_time.values, marker=".", linestyle="-")
plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.title("Drift időbeli eloszlása (minden kapcsolat, percenkénti átlag)", fontsize=14)
plt.xlabel("Idő (UTC)")
plt.ylabel("Átlagos drift [Hz]")
plt.grid(True)
plt.tight_layout()
plt.show()
