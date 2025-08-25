# WSPR Doppler-kísérlet – 2024-11-21, Dnipro rakétacsapás

Ez a kísérlet annak vizsgálatára készült, hogy a WSPR (Weak Signal Propagation Reporter) 
globális amatőrrádiós hálózat adataiban felismerhetők-e olyan rendellenességek,
amelyek egy gyorsan mozgó objektum – például egy ballisztikus rakéta – által okozott 
**Doppler-eltolódásra** utalhatnak.

---

## Inspiráció és háttér

A kísérlet ötlete nem a semmiből jött.  
Először **Gőzse István kollégámtól** hallottam arról a kutatásról, amelyben a 
WSPR-hálózat adatait használták fel az eltűnt maláj utasszállító, a 
**Malaysia Airlines MH370** utolsó repülési szakaszának rekonstruálására.  

A kutatók több millió WSPR-spotot elemeztek, és ezekből következtettek arra, 
merre haladhatott a gép az Indiai-óceán felett, amikor a fedélzeti transzponderek 
már rég elnémultak.  
Ez volt az első olyan pillanat, amikor a WSPR mint **globális rádiós érzékelő hálózat** 
meghaladta eredeti, amatőr rádiós szerepét, és olyan információt szolgáltatott, amely 
világszinten is egyedi és megismételhetetlen.  

Ez inspirált arra, hogy megnézzük: vajon hasonló módon egy másik, jól dokumentált esemény, 
a **2024-11-21-i Dnipro elleni Oreshnik rakétacsapás** nyomot hagyott-e a WSPR adatokban.  

---

## Kísérlet célja

- A 2024-11-21 02:00–05:00 UTC közötti WSPR-spotok elemzése.  
- Vizsgálni, hogy az **Ukrajna felett áthaladó linkekben** van-e szokatlan `drift` (frekvenciaeltolódás).  
- Koncentráció a **20 m, 30 m és 40 m** sávokra, mert ezek jellemzően aktívak 
  EU–RU összeköttetésekben.  

A WSPR `drift` értéke általában ±1 Hz-en belül marad.  
A ±2 Hz feletti érték **szokatlan**, és lehet:
- instabil adó/vevő oszcillátor eredménye,  
- ionoszférikus anomália,  
- vagy egy **valódi gyors objektum Doppler-hatása**.

---

## Adatforrás

- **[wspr.live](https://wspr.live/)** – ClickHouse adatbázis, amely a teljes WSPR történelmet tartalmazza.  
- Tábla: `wspr.rx`  
- SQL-szerű lekérdezésekkel érhető el:  
  - `https://db1.wspr.live/?query=...`  
  - támogatott formátumok: `CSV`, `JSON`  

---

## Előkészületek (Ubuntu / Devuan Linux)

A kísérlet Ubuntu és Devuan Linux rendszereken készült.  
A futtatáshoz egy **virtuális környezet (venv)** létrehozása ajánlott.

### Virtuális környezet létrehozása

```bash
python3 -m venv venv
source venv/bin/activate
```

### Szükséges csomagok telepítése

```bash
pip install --upgrade pip
pip install pandas matplotlib requests
```

---

## Adatok lekérése

Példa lekérdezés 2024-11-21 02:00–05:00 UTC, 20/30/40 m sávokra:

```
SELECT time, band, tx_sign, tx_lat, tx_lon, rx_sign, rx_lat, rx_lon, frequency, snr, drift
FROM wspr.rx
WHERE time >= '2024-11-21 02:00:00'
  AND time < '2024-11-21 05:00:00'
  AND band IN (7,10,14)
FORMAT CSV
```

---

## Python szkript

`wspr_fetch.py`:

```python
import urllib.request, urllib.parse, json, pandas as pd

def wsprlive_get(query):
    url = "https://db1.wspr.live/?query=" + urllib.parse.quote_plus(query + " FORMAT JSON")
    contents = urllib.request.urlopen(url).read()
    return json.loads(contents.decode("UTF-8"))["data"]

query = """
SELECT time, band, tx_sign, tx_lat, tx_lon, rx_sign, rx_lat, rx_lon, frequency, snr, drift
FROM wspr.rx
WHERE time >= '2024-11-21 02:00:00'
  AND time < '2024-11-21 05:00:00'
  AND band IN (7,10,14)
"""

rows = wsprlive_get(query)
cols = ["time","band","tx_sign","tx_lat","tx_lon","rx_sign","rx_lat","rx_lon","frequency","snr","drift"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("wspr_20241121_0200_0500.csv", index=False)

print("Sorok száma:", len(df))
print("Mentve: wspr_20241121_0200_0500.csv")
```

---

## Következő lépések

1. A CSV elemzése Pandas segítségével.  
2. Geometriai szűrés: mely linkek haladnak át Ukrajna felett?  
3. Drift-anomáliák (`abs(drift) > 2`) kiemelése.  
4. Eredmények idő- és térképes ábrázolása.  

---

## Kapcsolódó kutatások

- **MH370 és a WSPR**  
  2021-ben és 2022-ben több kutatócsoport is vizsgálta az eltűnt maláj utasszállító, 
  a Malaysia Airlines MH370 útját.  
  A WSPR-hálózat több millió spotját elemezve próbálták meghatározni a repülőgép 
  utolsó útvonalát az Indiai-óceán felett.  
  Bár az eredmények vitatottak, a módszer egyedülálló példája annak, hogyan válhat a 
  globális amatőrrádiós infrastruktúra váratlanul egyfajta „passzív radarhálózattá”.

Forrás:  
- [MH370 WSPR Tracking Project – Scientific Reports](https://www.mdpi.com/2504-3900/83/1/18)

---

## Záró megjegyzés

Ez a kísérlet **szabad, önkéntes kutatás**, amely a nyílt rádiós adatok 
lehetőségeit vizsgálja.  

Érdemes megemlíteni, hogy több mint harminc éve **Linus Torvalds** publikálta a 
Linux rendszermag első verzióját a **GNU** közösség felé – aminek köszönhetően ma bárki,  
szabadon futtathat ilyen elemzéseket teljesen szabad, **UNIX**-like rendszereken.  

Szabadság és nyitottság, MIT, GNU.