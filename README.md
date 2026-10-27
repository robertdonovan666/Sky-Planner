# Riverbank Sky Planner

A web app for planning a night of observing from Riverbank, California, with a Seestar 50 and a Meade ETX 4".

Live at **https://robertdonovan666.github.io/sky-planner/**

## What it shows

- Tonight's sunset, full dark, dawn and moon-free dark window, with a time slider
- A panorama of the eastern (or western) sky with the Moon, planets, deep-sky objects and the ecliptic
- Moon phase, illumination, position, rise/set and next full/new moon
- Hourly cloud cover for tonight (low/mid/high), dew risk and wind, from [Open-Meteo](https://open-meteo.com/)
- What is up in your clear view right now, rated for the Seestar or the ETX, with moon-interference warnings
- What rises into view later tonight, and active or upcoming meteor showers
- Planet imaging for the ETX + ZWO camera: disk size in pixels, best window above 30°, jet-stream steadiness estimate, capture tips, and Jupiter's moons
- Comets within reach, from Minor Planet Center orbits refreshed daily
- Red-light mode to protect night vision

## Install on iPad or iPhone

Open the link in Safari, tap **Share**, then **Add to Home Screen**. It opens full screen and works offline (except the cloud forecast).

## How it's built

A single static page with no build step:

- `index.html`: the whole app (styles, catalog and logic)
- `astronomy.browser.min.js`: [Astronomy Engine](https://github.com/cosinekitty/astronomy) 2.1.19 (MIT) for all positions and rise/set times
- `sw.js`: offline cache. Bump `VERSION` when shell files change.
- `manifest.webmanifest`, `icons/`: home-screen install
- `comets.json`: comet orbits, rewritten daily by `.github/workflows/comets.yml` running `tools/update_comets.py`

To add a target, append a row to the `CATALOG` array in `index.html` (`[id, name, kind, RA hours J2000, Dec degrees, magnitude, size arcmin, note]`). Location, clear-view azimuth range and minimum altitude are editable in the app's settings and saved per device.
