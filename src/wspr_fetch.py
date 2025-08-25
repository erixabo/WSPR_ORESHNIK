import urllib.request, urllib.parse, json, pandas as pd

def wsprlive_get(query):
    url = "https://db1.wspr.live/?query=" + urllib.parse.quote_plus(query + " FORMAT JSON")
    contents = urllib.request.urlopen(url).read()
    return json.loads(contents.decode("UTF-8"))["data"]

# Lekérdezés 2024-11-21 02:00–05:00 UTC közötti időablakra, 20m/30m/40m sávok
query = """
SELECT time, band, tx_sign, tx_lat, tx_lon, rx_sign, rx_lat, rx_lon, frequency, snr, drift
FROM wspr.rx
WHERE time >= '2024-11-21 02:00:00'
  AND time < '2024-11-21 05:00:00'
  AND band IN (7,10,14)
"""

rows = wsprlive_get(query)

# Oszlopok definiálása
cols = ["time","band","tx_sign","tx_lat","tx_lon","rx_sign","rx_lat","rx_lon","frequency","snr","drift"]

# Adatok DataFrame-be töltése
df = pd.DataFrame(rows, columns=cols)

# CSV mentés
outfile = "wspr_20241121_0200_0500.csv"
df.to_csv(outfile, index=False)

print("Sorok száma:", len(df))
print("CSV fájl mentve ide:", outfile)
print(df.head())
