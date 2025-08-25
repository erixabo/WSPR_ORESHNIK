import pandas as pd

# Forrásfájl (a letöltött 259k soros CSV)
INPUT_FILE = "wspr_20241121_0200_0500.csv"
# Kimeneti fájl a nagy driftekkel
OUTPUT_FILE = "wspr_drifts_gt2.csv"

def main():
    print(f"Beolvasás: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)

    # Szűrés drift alapján
    big_drifts = df[df["drift"].abs() > 2]

    print(f"Eredeti sorok: {len(df)}")
    print(f"Nagy drift (>2 Hz) sorok: {len(big_drifts)}")

    # Mentés új CSV-be
    big_drifts.to_csv(OUTPUT_FILE, index=False)
    print(f"Mentve: {OUTPUT_FILE}")

    # Mutassuk az első pár sort
    print(big_drifts.head(10))

if __name__ == "__main__":
    main()
