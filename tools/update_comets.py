#!/usr/bin/env python3
"""Refresh comets.json from the Minor Planet Center's comet elements file.

Runs daily in GitHub Actions. Keeps comets that could plausibly be within reach of a
small telescope (perihelion within ~2 years of today, absolute magnitude H <= 16) so the
page stays small. The page itself computes positions and brightness.

Format: https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/comet-orbit-format/
("Ephemerides and Orbital Elements" layout, 1-based columns).
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone

URL = "https://www.minorplanetcenter.net/iau/MPCORB/CometEls.txt"
OUT = "comets.json"


def col(line, a, b):
    return line[a - 1:b].strip()


def jd_from_ymd(y, m, d):
    # Day may be fractional (TT). Standard Meeus algorithm, Gregorian calendar.
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5


def parse(text):
    out = []
    for line in text.splitlines():
        if len(line) < 103:
            continue
        try:
            tp = jd_from_ymd(int(col(line, 15, 18)), int(col(line, 20, 21)), float(col(line, 23, 29)))
            rec = {
                "name": col(line, 103, 158),
                "tp": round(tp, 5),
                "q": float(col(line, 31, 39)),
                "e": float(col(line, 42, 49)),
                "w": float(col(line, 52, 59)),
                "node": float(col(line, 62, 69)),
                "i": float(col(line, 72, 79)),
            }
            h, k = col(line, 92, 95), col(line, 97, 100)
            rec["H"] = float(h) if h else None
            rec["K"] = float(k) if k else 4.0
        except ValueError:
            continue
        out.append(rec)
    return out


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "sky-planner (github.com/robertdonovan666/sky-planner)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode("utf-8", "replace")
    allc = parse(text)
    if len(allc) < 100:
        sys.exit(f"Only parsed {len(allc)} comets; refusing to overwrite {OUT}")
    now = datetime.now(timezone.utc)
    jd_now = now.timestamp() / 86400 + 2440587.5
    keep = [c for c in allc
            if c["H"] is not None and c["H"] <= 16 and c["q"] <= 8 and abs(c["tp"] - jd_now) <= 730]
    keep.sort(key=lambda c: c["H"])
    with open(OUT, "w") as f:
        json.dump({"updated": now.strftime("%Y-%m-%dT%H:%MZ"), "source": URL, "comets": keep}, f, separators=(",", ":"))
        f.write("\n")
    print(f"Parsed {len(allc)} comets, kept {len(keep)}")


if __name__ == "__main__":
    main()
