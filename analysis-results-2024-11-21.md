# WSPR-vizsgálat: Dnipro, 2024-11-21

**Állapot: feltáró teszt; a rakétához köthető WSPR-anomáliát nem mutatott ki.** Ez nem bizonyítja, hogy semmilyen fizikai kölcsönhatás nem történt. A mintavétel ritka, a rádiós terjedési útvonal nem rekonstruálható a spot végpontjaiból, a pálya pedig csak közelítő földfelszíni vonalként szerepel.

## Kérdés

Található-e a WSPR-adatokban a Kapusztyin Jar–Dnipro vonal közelében, az esemény becsült idején olyan drifteltérés, amelyet az esemény előtti és utáni, ugyanazon rádiókapcsolatokhoz lehetne viszonyítani?

Az ukrán katonai hírszerzés 15 perces repülési időt közölt az Asztraháni területről Dnipróba; a korabeli hírek a támadást november 21-én reggelre, helyi idő szerint 05:00–07:00 közé tették. A rádiós adatbázis UTC-időt használ. Ezért az előzetesen választott, kerekített **03:00–03:20 UTC** ablak csak közelítés, nem ismert pontos rakéta- vagy Doppler-idősor. Források: [Ukrainska Pravda – az ukrán hírszerzés közlése](https://www.pravda.com.ua/eng/news/2024/11/22/7485828/), [Ukrainian Air Force bejegyzései és időbélyegei](https://t.me/s/kpszsu?before=23391).

## Módszer

- Adatforrás: nyilvános `wspr.rx` tábla a [wspr.live](https://wspr.live/) szolgáltatásból.
- Sávok: 40, 30 és 20 méter (`band` értékei 7, 10, 14; a WSPR Live mezője a frekvencia első számjegyét tárolja).
- Letöltött idő: 2024-11-21 02:40–03:40 UTC; **80 725 spot**.
- Térbeli közelítés: Kapusztyin Jar (48.58°N, 45.74°E) és Dnipro (48.46°N, 35.05°E) közötti, kb. 786.8 km-es nagy kör. Minden WSPR-adó–vevő nagy kör minimális távolságát számoltuk ehhez a szakaszhoz.
- Időablakok: előtte 02:40–03:00, esemény-becslés 03:00–03:20, utána 03:20–03:40 UTC.
- A térbeli érzékenységet 50, 100, 250 és 500 km-es folyosóval számoltuk. Ezek elemzői küszöbök, nem a rakéta tényleges pályájának hibasávjai.
- A kapcsolati összehasonlítás kulcsa azonos adóhívójel + vevőhívójel + sáv. Csak az mindhárom időablakban előforduló kapcsolatok kerültek a páros összehasonlításba.

A megvalósítás: [`src/analyze_event.py`](src/analyze_event.py). Első futáskor letölti az adatokat; a helyi CSV-t a `.gitignore` kizárja, ezért a repó csak a lekérdező és elemző kódot, valamint az összesített eredményt tartalmazza.

## Eredmény

| Útvonaltól számított folyosó | Eseményablak spotjai | Eseményablak egyedi adó-vevő-sáv kapcsolatai | Mindhárom ablakban ismétlődő párok | `|drift| > 2` az eseményablakban | Esemény medián driftje |
|---:|---:|---:|---:|---:|---:|
| 50 km | 36 | 32 | 8 | 0 | 0 |
| 100 km | 54 | 50 | 16 | 0 | 0 |
| 250 km | 76 | 72 | 26 | 0 | 0 |
| 500 km | 98 | 93 | 31 | 0 | 0 |

Mind a négy folyosószélességnél az eseményablak és az előtte/utána ablak közötti **párosított medián driftkülönbség 0** volt. Az 50 km-es folyosó 36 esemény-spotjából mind a 36 driftértéke 0; a 100 km-es folyosóban az értékek eloszlása 0:50, −1:3, +1:1. Egyetlen eseményablakbeli `|drift| > 2` értéket sem találtunk a vizsgált folyosókban.

A közeli, 50 km-es folyosóban tehát kevés és ritkán ismétlődő adat volt: 36 spot 32 kapcsolatból, és mindössze 8 kapcsolat fordult elő mindhárom 20 perces ablakban. Ez alacsony erejű vizsgálat. A tágabb folyosók növelik a mintát, de egyre kevésbé jelentenek érdemi geometriai közelséget.

## Mit jelent — és mit nem

Ez a futás **nem talált kimutatható drift-anomáliát** az egyszerű földfelszíni útvonalfolyosókban. Nem alkalmas annak kijelentésére, hogy a rakéta nem befolyásolt egyetlen rádióutat sem: a WSPR-adatbázis nem tartalmazza a teljes rádiós terjedési nyalábot, az ionoszférikus visszaverődést, a rakéta pontos 3D pályáját, vagy az érintett jel lokális spektrumát.

A WSPR `drift` mező önmagában nem rakéta-Doppler-mérés. A [WSPR Live mezőleírása](https://wspr.live/) a mező egységét bizonytalannak jelzi; a [WSPR technikai leírása](https://wsjt.sourceforge.io/WSPR_QST_Nov_2010.pdf) a dekóder driftsebességéről és az adó/vevő oszcillátorának hozzájárulásáról ír. A README korábbi `|drift| > 2` állítása ezért nem tekinthető validált anomáliaküszöbnek.

**Következtetés:** az eredeti hipotézist ez az adat és ez az eljárás nem támasztja alá. Az eredmény negatív és korlátozott; nem bizonyíték fizikai kölcsönhatásra, és nem is annak kizárására.
