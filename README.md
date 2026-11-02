# YouTube data without the API quota (Python)

Collect YouTube search results, channels and full video stats (views, likes, comments, publish date) without the YouTube Data API quota, and rank channels in a niche. Uses the YouTube Scraper on Apify.

▶️ **Actor:** [rt-solutions/youtube-scraper](https://apify.com/rt-solutions/youtube-scraper) · runs on Apify's free plan

The YouTube Data API is free — until you hit the 10,000-unit daily quota. A single search costs 100 units, so you get about 100 searches a day. For research, influencer lists or trend tracking that's not enough.

In this tutorial we'll collect YouTube search results, whole channels and full video stats **without an API key or quota**, then turn them into a ranked list of channels.


## What you get

- **Search results**: videos, Shorts, channels or playlists, with YouTube's filters (upload date, length, sort by views)
- **Videos**: views, likes, comment count, exact publish date, duration, description, tags, category
- **Channels**: subscribers, total views, video count, country, joined date, links, plus their videos, Shorts, live streams and playlists

## 1. Try it without code

Open [YouTube Scraper](https://apify.com/rt-solutions/youtube-scraper), click **Try for free** and run:

```json
{ "searchQueries": ["home workout"], "maxResults": 50, "uploadDate": "week", "sortBy": "views" }
```

You get the 50 most viewed "home workout" videos of the week. Export to CSV/Excel or JSON.

## 2. Whole channels

Paste channel URLs (`@handle`, `/channel/ID`, `/c/name`) in `startUrls`:

```json
{
  "startUrls": ["https://www.youtube.com/@mkbhd", "https://www.youtube.com/@veritasium"],
  "channelTabs": ["videos", "shorts"],
  "maxVideosPerChannel": 100,
  "includeChannelInfo": true
}
```

You get one row per channel (subscribers, total views, country, links…) and its latest videos and Shorts.

## 3. From Python: find the fastest-growing channels in a niche

```bash
pip install -r requirements.txt
export APIFY_TOKEN=your_token   # free account: https://apify.com
python top_channels.py
```

```python
import os
from apify_client import ApifyClient
from collections import defaultdict

client = ApifyClient(os.environ["APIFY_TOKEN"])

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
```

A video item (shortened):

```json
{
  "type": "video", "id": "2reQut8WNGc",
  "title": "Macbook PROLED XDR Impressions: They Said They Wouldn't!",
  "viewCount": 10027295, "likeCount": 129851, "commentCount": 11000,
  "publishedAt": "2026-10-28T19:50:34-07:00", "duration": "10:54",
  "channelName": "Marques Brownlee", "channelUrl": "https://www.youtube.com/@mkbhd"
}
```

## 4. Next steps

- Need what is *said* in the videos? Feed the video URLs to [YouTube Transcript](https://apify.com/rt-solutions/youtube-transcript).
- Need audience reactions? Use [YouTube Comments Scraper](https://apify.com/rt-solutions/youtube-comments-scraper).
- Schedule the run daily in Apify Console to track a niche over time.

## Cost

$0.50 per 1,000 results (cheaper on paid plans), full video details included. Missing or private videos are free. The example above (~300 videos) costs about $0.15.

## Notes

- Comment counts are rounded the way YouTube shows them (e.g. 11K).
- Channel business emails are hidden behind a YouTube login and are not collected.

Questions? Open an issue on the [Actor page](https://apify.com/rt-solutions/youtube-scraper).

## License

MIT — the example code is free to use. The data comes from the [youtube-scraper](https://apify.com/rt-solutions/youtube-scraper) Actor (pay per result on Apify).
