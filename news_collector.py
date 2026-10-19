
import csv
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent

FEED_URL = (
    "https://pib.gov.in/RssMain.aspx"
    "?ModId=6&Lang=1&Regid=3"
)

OUTPUT_FILE = BASE_DIR / "collected_news.csv"

KEYWORDS = [
    "india", "foreign affairs", "foreign minister",
    "bilateral", "diplomatic", "geopolitical",
    "border", "defence", "defense", "military",
    "security", "terrorism", "sanctions",
    "trade", "tariff", "export", "import",
    "energy", "petroleum", "natural gas",
    "oil", "shipping", "supply chain",
    "china", "pakistan", "bangladesh", "nepal",
    "bhutan", "sri lanka", "maldives", "myanmar",
    "united states", "russia", "iran", "israel",
    "west asia", "middle east", "indian ocean",
    "cyber", "semiconductor", "critical minerals",
]

def clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()

def main():
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "IndiaRiskIntelligence/1.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    items = root.findall(".//item")

    collected_at = datetime.now(timezone.utc).isoformat()
    matches = []

    for item in items:
        title = clean_text(item.findtext("title"))
        link = clean_text(item.findtext("link"))
        description = clean_text(item.findtext("description"))
        published = clean_text(item.findtext("pubDate"))

        searchable = f"{title} {description}".lower()
        matched_keywords = [
            keyword for keyword in KEYWORDS
            if keyword in searchable
        ]

        if not title or not link or not matched_keywords:
            continue

        matches.append({
            "collected_at_utc": collected_at,
            "published_date": published,
            "headline": title,
            "source": "Press Information Bureau, Government of India",
            "source_url": link,
            "matched_keywords": "; ".join(matched_keywords),
            "verification_status": "Unverified - review source",
        })

    fields = [
        "collected_at_utc",
        "published_date",
        "headline",
        "source",
        "source_url",
        "matched_keywords",
        "verification_status",
    ]

    # Preserve earlier collected records and avoid duplicate URLs.
    existing = {}
    if OUTPUT_FILE.exists():
        with OUTPUT_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                if row.get("source_url"):
                    existing[row["source_url"]] = row

    for row in matches:
        existing[row["source_url"]] = row

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"Feed items received: {len(items)}")
    print(f"Relevant headlines matched this run: {len(matches)}")
    print(f"Unique headlines saved: {len(existing)}")
    print(f"Output file: {OUTPUT_FILE.name}")

if __name__ == "__main__":
    main()
