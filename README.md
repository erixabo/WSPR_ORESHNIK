# WSPR-vizsgálat – Dnipro, 2024-11-21

## Eredmény röviden

A reprodukciós teszt **nem talált kimutatható drift-anomáliát** a Dniprohoz vezető, becsült rakétaútvonal közelében. A kevés releváns, ismétlődő adó–vevő útvonal miatt ez gyenge negatív eredmény: nem bizonyítja, hogy semmilyen kölcsönhatás nem történt. A teljes módszer és az eredménytábla az [elemzési jegyzőkönyvben](analysis-results-2024-11-21.md) olvasható.

Ez feltáró kísérlet volt, nem validált passzív radar. A WSPR `drift` mező önmagában nem rakéta-Doppler-mérés: az adatbázis egysége bizonytalan, a dekóder becsléséhez pedig az adó és a vevő frekvenciasodródása is hozzájárulhat.

## Vizsgálat

A [wspr.live](https://wspr.live/) nyilvános `wspr.rx` adatbázisából lekérdeztük a 40, 30 és 20 méteres sávokat (`band` 7, 10, 14) 2024-11-21 02:40–03:40 UTC között. A vizsgált eseményablak 03:00–03:20 UTC; ezt a reggeli támadás időzítéséből és a közölt, hozzávetőleg 15 perces repülési időből kerekítettük. A pontos 3D pálya és a rádióterjedési út nem ismert.

Az adó–vevő állomások földrajzi végpontjai közti nagy kört hasonlítottuk a Kapusztyin Jar–Dnipro hozzávetőleges felszíni szakaszához (786.8 km). A számítás 50, 100, 250 és 500 km-es folyosókkal készült. Ez csak geometriai szűrés: nem modellezi az ionoszférikus visszaverődést, a jel teljes térbeli útját vagy a rakéta 3D pályáját.

A 03:00–03:20 UTC eseményablakban az 50 km-es folyosó 36 spotot adott 32 adó–vevő–sáv kapcsolatból; csak 8 ilyen kapcsolat szerepelt az előtte és utána következő ablakban is. Az eseményablak medián driftje minden folyosón nulla volt; az eseményablakban nem volt `|drift| > 2` érték. A párosított kapcsolatok medián változása az előtte/utána ablakhoz képest nulla volt.

## Újrafuttatás

A `src/analyze_event.py` kizárólag Python alapkönyvtárat használ:

```bash
python3 src/analyze_event.py
```

A program lekéri az adatokat, és helyi gyorsítótárként a `data/wspr_20241121_0240_0340_utc.csv` fájlba menti őket. A CSV-ket a `.gitignore` kizárja; a repó ezért az elemzőkódot és az összesített eredményeket tartalmazza, nem a nyers adatmásolatot.

A `src/wspr_fetch.py`, `src/driftts_per_min_orig.py` és `src/filter_drifts.py` az eredeti, általános letöltési/ábrázolási próbák. A `Figure_1.png` az összes link percenkénti átlagát mutatja, nem az esemény útvonalára szűrt eredményt.

Az előző README egy hibás MDPI-hivatkozást tartalmazott: az a vállmerevség kezeléséről szólt, nem az MH370-ről. Az elavult PDF-et eltávolítottam. Az MH370-WSPR-kísérlet hátteréhez lásd a [szerzők műszaki jelentését](https://www.mh370search.com/2022/03/14/mh370-wspr-technical-report/); ez a szerzők saját beszámolója, nem független validáció, és a jelen vizsgálat nem támaszkodik rá.

## Források és korlátok

- [WSPR Live adatbázis és mezőleírás](https://wspr.live/) – a `drift` mezőt −3…+3 tartományúként írja le, egységét bizonytalannak jelöli.
- [WSPR technikai leírás](https://wsjt.sourceforge.io/WSPR_QST_Nov_2010.pdf) – a dekóder driftbecslése és az adó/vevő oszcillátorainak sodródása.
- [Ukrainska Pravda: az ukrán hírszerzés közlése a repülési időről](https://www.pravda.com.ua/eng/news/2024/11/22/7485828/).
- [Ukrainian Air Force Telegram-archívum](https://t.me/s/kpszsu?before=23391).

A következtetés csak ennyi: **a vizsgált WSPR-adatokból, ezzel a közelítő útvonal- és driftmódszerrel nem mutatható ki eseményhez köthető eltérés.**
