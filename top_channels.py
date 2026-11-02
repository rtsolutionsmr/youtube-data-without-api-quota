"""YouTube data without the API quota (Python)

Collect YouTube search results, channels and full video stats (views, likes, comments, publish date) without the YouTube Data API quota, and rank channels in a niche. Uses the YouTube Scraper on Apify.
Actor: https://apify.com/rt-solutions/youtube-scraper
"""
import os
from apify_client import ApifyClient
from collections import defaultdict

client = ApifyClient(os.environ["APIFY_TOKEN"])  # Apify Console → Settings → API & Integrations

run = client.actor("rt-solutions/youtube-scraper").call(run_input={
    "searchQueries": ["ai agents tutorial", "n8n automation", "claude code"],
    "maxResults": 100,
    "resultType": "video",
    "uploadDate": "month",
    "includeVideoDetails": True,   # exact date, likes, comment count, tags
})

views = defaultdict(int); videos = defaultdict(int)
for v in client.dataset(run.default_dataset_id).iterate_items():
    if v.get("type") != "video":
        continue
    views[v["channelName"]] += v.get("viewCount") or 0
    videos[v["channelName"]] += 1

top = sorted(views.items(), key=lambda kv: kv[1], reverse=True)[:15]
for name, total in top:
    print(f"{name:35} {videos[name]:3} videos  {total:>12,} views this month")
