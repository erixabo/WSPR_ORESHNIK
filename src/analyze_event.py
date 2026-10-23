#!/usr/bin/env python3
"""Exploratory geometry-screened WSPR drift comparison for the Dnipro event.

Uses only public wspr.live spots and a straight surface great-circle corridor
between approximate launch and impact locations. This is not a missile
trajectory or an HF propagation-ray reconstruction.
"""

import csv
import json
import math
import statistics
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


START = "2024-11-21 02:40:00"
END = "2024-11-21 03:40:00"
EVENT_START = datetime(2024, 11, 21, 3, 0, tzinfo=timezone.utc)
EVENT_END = datetime(2024, 11, 21, 3, 20, tzinfo=timezone.utc)
KAPUSTIN_YAR = (48.58, 45.74)
DNIPRO = (48.46, 35.05)
BANDS = (7, 10, 14)
EARTH_KM = 6371.0088
FIELDS = ("time", "band", "tx_sign", "tx_lat", "tx_lon", "rx_sign", "rx_lat",
          "rx_lon", "frequency", "snr", "drift", "version", "code")


def vector(lat_lon):
    lat, lon = map(math.radians, lat_lon)
    return (math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    length = norm(a)
    if length < 1e-14:
        return None
    return tuple(x / length for x in a)


def angle(a, b):
    return math.acos(max(-1.0, min(1.0, dot(a, b))))


def on_minor_arc(p, a, b):
    return abs(angle(a, p) + angle(p, b) - angle(a, b)) < 1e-7


def point_arc_angle(p, a, b):
    normal = unit(cross(a, b))
    if normal is None:
        return min(angle(p, a), angle(p, b))
    projected = unit(tuple(p[i] - dot(p, normal) * normal[i] for i in range(3)))
    if projected is not None:
        for candidate in (projected, tuple(-x for x in projected)):
            if on_minor_arc(candidate, a, b):
                return angle(p, candidate)
    return min(angle(p, a), angle(p, b))


def arc_distance_km(a, b, c, d):
    """Minimum distance between two minor great-circle arcs on a sphere."""
    n1, n2 = unit(cross(a, b)), unit(cross(c, d))
    if n1 is not None and n2 is not None:
        intersection = unit(cross(n1, n2))
        if intersection is not None:
            for p in (intersection, tuple(-x for x in intersection)):
                if on_minor_arc(p, a, b) and on_minor_arc(p, c, d):
                    return 0.0
    distances = (point_arc_angle(a, c, d), point_arc_angle(b, c, d),
                 point_arc_angle(c, a, b), point_arc_angle(d, a, b))
    return min(distances) * EARTH_KM


def parse_time(value):
    return datetime.fromisoformat(value.replace(" ", "T")).replace(tzinfo=timezone.utc)


def load_or_fetch(path):
    if path.exists():
        with path.open(newline="", encoding="utf-8") as source:
            return list(csv.DictReader(source))
    query = (
        "SELECT " + ",".join(FIELDS) + " FROM wspr.rx "
        f"WHERE time >= '{START}' AND time < '{END}' "
        "AND band IN (7,10,14) FORMAT JSONEachRow"
    )
    url = "https://db1.wspr.live/?query=" + urllib.parse.quote(query)
    request = urllib.request.Request(url, headers={"User-Agent": "WSPR-Oreshnik-exploratory-analysis/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        lines = response.read().decode("utf-8").splitlines()
    records = [json.loads(line) for line in lines if line.strip()]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    return records


def main():
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "wspr_20241121_0240_0340_utc.csv"
    records = load_or_fetch(data_path)
    route_start, route_end = vector(KAPUSTIN_YAR), vector(DNIPRO)
    print(f"Fetched/stored spots: {len(records)}")
    print(f"Date window UTC: {START} to {END}")
    print(f"Approximate surface route: {KAPUSTIN_YAR} to {DNIPRO}; "
          f"{angle(route_start, route_end) * EARTH_KM:.1f} km")
    print("Corridor counts are sensitivity checks, not a measured missile path.")

    measured = []
    for row in records:
        try:
            tx = vector((float(row["tx_lat"]), float(row["tx_lon"])))
            rx = vector((float(row["rx_lat"]), float(row["rx_lon"])))
            separation = arc_distance_km(tx, rx, route_start, route_end)
            t = parse_time(row["time"])
            band = int(row["band"])
            drift = int(row["drift"])
        except (KeyError, TypeError, ValueError):
            continue
        period = "before" if t < EVENT_START else "event" if t < EVENT_END else "after"
        pair = (band, row["tx_sign"], row["rx_sign"])
        measured.append((separation, period, pair, drift))

    for width in (50, 100, 250, 500):
        groups = defaultdict(list)
        row_counts = Counter()
        unique_pairs = defaultdict(set)
        for separation, period, pair, drift in measured:
            if separation > width:
                continue
            row_counts[period] += 1
            unique_pairs[period].add(pair)
            groups[(period, pair)].append(drift)

        print(f"\nCorridor <= {width} km")
        for period in ("before", "event", "after"):
            vals = [v for (p, _), drifts in groups.items() if p == period for v in drifts]
            print(f"  {period:6s}: spots={row_counts[period]:5d}, "
                  f"pairs={len(unique_pairs[period]):4d}, "
                  f"median_drift={statistics.median(vals) if vals else 'NA'}, "
                  f"abs_drift_gt2={sum(abs(v) > 2 for v in vals)}")

        common = unique_pairs["event"] & unique_pairs["before"] & unique_pairs["after"]
        changes = []
        for pair in common:
            before = statistics.median(groups[("before", pair)])
            event = statistics.median(groups[("event", pair)])
            after = statistics.median(groups[("after", pair)])
            changes.append((event - before, event - after))
        print(f"  matched tx/rx/band pairs in all windows: {len(common)}")
        if changes:
            e_b = [x[0] for x in changes]
            e_a = [x[1] for x in changes]
            print(f"  event-before median pair drift change: {statistics.median(e_b):+.2f} drift-unit")
            print(f"  event-after  median pair drift change: {statistics.median(e_a):+.2f} drift-unit")


if __name__ == "__main__":
    main()
