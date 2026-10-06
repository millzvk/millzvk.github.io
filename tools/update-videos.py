"""Refresh videos.json from the channel's public YouTube feed (newest first)."""
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UC8hlK3mOPwd5intx5KcQkTA"
FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL_ID
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
OUT = pathlib.Path(__file__).resolve().parent.parent / "videos.json"

with urllib.request.urlopen(FEED, timeout=30) as res:
    root = ET.fromstring(res.read())

videos = [
    {
        "id": e.find("yt:videoId", NS).text,
        "title": e.find("a:title", NS).text,
        "published": e.find("a:published", NS).text,
    }
    for e in root.findall("a:entry", NS)
][:12]

if not videos:
    raise SystemExit("feed returned no videos; leaving videos.json untouched")

OUT.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {len(videos)} videos to {OUT.name}")
