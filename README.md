# WSPR Doppler Kísérlet – 2024-11-21, Dnipro Oreshnik csapás

Ez a kísérlet azt vizsgálja, hogy a WSPR (Weak Signal Propagation Reporter) hálózat
nyers adataiban kimutatható-e a 2024. november 21-i Dnipro elleni rakétacsapás
(Oreshnik / ballisztikus rakéta) okozta Doppler-eltolódás.

## Cél

- WSPR linkek vizsgálata, amelyek **keresztezik Ukrajna feletti légteret**.
- A kritikus időablak: **2024-11-21 02:00–05:00 UTC**  
  (becsapódás ~03:30 UTC ± 1 óra).
- Sávok: **20 m, 30 m, 40 m** (leggyakoribb EU–RU forgalom).
- Kérdés: előfordul-e ±2 Hz-nél nagyobb `drift`, ami a rakéta Doppler-hatására utalhat?

## Adatforrás

- Adatok a [wspr.live](https://wspr.live/) ClickHouse adatbázisából.
- Táblázat: `wspr.rx`  
- Elérés: `https://db1.wspr.live/?query=...`
- Az adatbázis minden valaha rögzített WSPR spotot tartalmaz.  
- Lekérdezés SQL-szerű nyelven történik, `FORMAT JSON` vagy `FORMAT CSV` kimenettel.

## Lekérdezés

Példa lekérdezés:

```sql
SELECT time, band, tx_sign, tx_lat, tx_lon, rx_sign, rx_lat, rx_lon, frequency, snr, drift
FROM wspr.rx
WHERE time >= '2024-11-21 02:00:00'
  AND time < '2024-11-21 05:00:00'
  AND band IN (7,10,14)
FORMAT CSV
