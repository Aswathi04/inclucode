"""
build_office_json.py — reads your manually-verified coordinates from
office_coords.txt (one line per district: "District: lat, lon") and
combines them with the verified addresses in data_office_locations.py
to produce data_office_locations.json, the file app.py actually reads.

This exists so the only manual step is the actual look-and-confirm on
openstreetmap.org — not hand-typing JSON syntax, which is an easy place
to introduce a silent typo (trailing comma, mismatched bracket, etc.).

Usage:
    python build_office_json.py
"""

import json
import sys
from data_office_locations import DISTRICT_SOCIAL_JUSTICE_OFFICES, KSHPWC_HEAD_OFFICE

COORDS_FILE = "office_coords.txt"
OUTPUT_FILE = "data_office_locations.json"


def parse_coords_file(path):
    coords = {}
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                print(f"⚠️  Line {line_num} has no ':' — skipping: {line}")
                continue
            district, rest = line.split(":", 1)
            district = district.strip()
            try:
                lat_str, lon_str = rest.strip().split(",")
                lat, lon = float(lat_str.strip()), float(lon_str.strip())
            except ValueError:
                print(f"⚠️  Line {line_num} couldn't be parsed as 'lat, lon' — skipping: {line}")
                continue
            coords[district] = (lat, lon)
    return coords


def main():
    try:
        coords = parse_coords_file(COORDS_FILE)
    except FileNotFoundError:
        print(f"❌ {COORDS_FILE} not found. Create it in the project root first — see the fill-in sheet.")
        sys.exit(1)

    output = {}
    skipped = []

    for district, info in DISTRICT_SOCIAL_JUSTICE_OFFICES.items():
        if district not in coords:
            skipped.append(district)
            continue
        lat, lon = coords[district]
        if lat == 0.0 and lon == 0.0:
            skipped.append(district)
            continue
        output[district] = {
            "address": info["address"],
            "phone": info["phone"],
            "lat": lat,
            "lon": lon,
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Wrote {len(output)} of {len(DISTRICT_SOCIAL_JUSTICE_OFFICES)} district offices to {OUTPUT_FILE}")

    if "KSHPWC" in coords and coords["KSHPWC"] != (0.0, 0.0):
        lat, lon = coords["KSHPWC"]
        output["KSHPWC"] = {
            "address": KSHPWC_HEAD_OFFICE["address"],
            "phone": KSHPWC_HEAD_OFFICE["phone"],
            "lat": lat,
            "lon": lon,
        }
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("✅ KSHPWC head office included")
    else:
        print("⚠️  KSHPWC head office not yet filled in office_coords.txt — add a 'KSHPWC: lat, lon' line")

    if skipped:
        print(f"\n⚠️  Skipped (missing or still 0.0, 0.0 placeholder): {', '.join(skipped)}")
        print("   These districts won't show a map on the detail page until you fill them in.")

    # Sanity check: flag any coordinates that look wildly outside Kerala's
    # actual bounding box (roughly 8.2–12.8 lat, 74.8–77.4 lon) — catches
    # an obvious mistyped digit before it ships.
    KERALA_LAT_RANGE = (8.0, 13.0)
    KERALA_LON_RANGE = (74.5, 77.6)
    for district, data in output.items():
        lat, lon = data["lat"], data["lon"]
        if not (KERALA_LAT_RANGE[0] <= lat <= KERALA_LAT_RANGE[1]) or \
           not (KERALA_LON_RANGE[0] <= lon <= KERALA_LON_RANGE[1]):
            print(f"🚨 {district}: ({lat}, {lon}) looks OUTSIDE Kerala's bounding box — double-check this one!")


if __name__ == "__main__":
    main()