"""Collect YouTube comments for a channel via the official YouTube Data API v3.

Usage:
    python collect.py --handle rus_delfi_lv --max-videos 200 --since 2026-07-01

Needs an API key in YOUTUBE_API_KEY, unless the environment injects it as a
network secret. Output goes to data/<handle>/ (git-ignored): videos.jsonl,
comments.jsonl, authors.jsonl. Re-running resumes: already fetched videos
are skipped.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.googleapis.com/youtube/v3/"


class QuotaExceeded(Exception):
    pass


def api_get(endpoint, params, retries=3):
    params = dict(params)
    key = os.environ.get("YOUTUBE_API_KEY")
    if key:
        params["key"] = key
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code == 403 and "quotaExceeded" in body:
                raise QuotaExceeded(body) from e
            if e.code == 403 and "commentsDisabled" in body:
                return {"items": [], "commentsDisabled": True}
            if e.code == 404:
                return {"items": [], "notFound": True}
            if e.code >= 500 and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"{e.code} {endpoint}: {body[:500]}") from e
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise


def paged(endpoint, params):
    token = None
    while True:
        p = dict(params)
        if token:
            p["pageToken"] = token
        data = api_get(endpoint, p)
        yield from data.get("items", [])
        token = data.get("nextPageToken")
        if not token:
            return


def resolve_channel(handle):
    data = api_get("channels", {"part": "snippet,contentDetails", "forHandle": handle})
    items = data.get("items") or []
    if not items:
        sys.exit(f"channel @{handle} not found")
    ch = items[0]
    return ch["id"], ch["contentDetails"]["relatedPlaylists"]["uploads"], ch["snippet"]["title"]


def list_videos(uploads_playlist, since, max_videos):
    out = []
    for it in paged("playlistItems", {"part": "contentDetails,snippet", "playlistId": uploads_playlist, "maxResults": 50}):
        published = it["contentDetails"].get("videoPublishedAt") or it["snippet"]["publishedAt"]
        if since and published < since:
            break  # uploads playlist is newest-first
        out.append({"video_id": it["contentDetails"]["videoId"], "title": it["snippet"]["title"], "published_at": published})
        if len(out) >= max_videos:
            break
    return out


def comment_row(video_id, snippet, comment_id, parent_id=None):
    return {
        "video_id": video_id,
        "comment_id": comment_id,
        "parent_id": parent_id,
        "author_channel_id": (snippet.get("authorChannelId") or {}).get("value"),
        "author_name": snippet.get("authorDisplayName"),
        "text": snippet.get("textOriginal") or snippet.get("textDisplay") or "",
        "published_at": snippet.get("publishedAt"),
        "like_count": snippet.get("likeCount", 0),
    }


def fetch_comments(video_id):
    rows = []
    for th in paged("commentThreads", {"part": "snippet,replies", "videoId": video_id, "maxResults": 100, "textFormat": "plainText", "order": "time"}):
        top = th["snippet"]["topLevelComment"]
        rows.append(comment_row(video_id, top["snippet"], top["id"]))
        total_replies = th["snippet"].get("totalReplyCount", 0)
        shown = (th.get("replies") or {}).get("comments", [])
        if total_replies > len(shown):
            shown = list(paged("comments", {"part": "snippet", "parentId": top["id"], "maxResults": 100, "textFormat": "plainText"}))
        for r in shown:
            rows.append(comment_row(video_id, r["snippet"], r["id"], parent_id=top["id"]))
    return rows


def fetch_authors(channel_ids):
    out = []
    ids = list(channel_ids)
    for i in range(0, len(ids), 50):
        data = api_get("channels", {"part": "snippet,statistics", "id": ",".join(ids[i:i + 50]), "maxResults": 50})
        for ch in data.get("items", []):
            st = ch.get("statistics", {})
            out.append({
                "author_channel_id": ch["id"],
                "created_at": ch["snippet"].get("publishedAt"),
                "country": ch["snippet"].get("country"),
                "subscriber_count": None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount", 0)),
                "video_count": int(st.get("videoCount", 0)),
            })
    return out


def read_jsonl(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path, rows):
    with path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", required=True, help="channel handle without @")
    ap.add_argument("--max-videos", type=int, default=200)
    ap.add_argument("--since", help="ISO date, e.g. 2026-07-01")
    ap.add_argument("--out", default="data")
    a = ap.parse_args()

    out = Path(a.out) / a.handle
    out.mkdir(parents=True, exist_ok=True)
    channel_id, uploads, title = resolve_channel(a.handle)
    print(f"@{a.handle}: {title} ({channel_id})")

    videos = list_videos(uploads, a.since, a.max_videos)
    (out / "videos.jsonl").write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in videos), encoding="utf-8")
    done_file = out / "done.txt"
    done = set(done_file.read_text().split()) if done_file.exists() else set()
    print(f"{len(videos)} videos, {len(done)} already fetched")

    try:
        for i, v in enumerate(videos, 1):
            if v["video_id"] in done:
                continue
            rows = fetch_comments(v["video_id"])
            append_jsonl(out / "comments.jsonl", rows)
            with (out / "done.txt").open("a") as f:
                f.write(v["video_id"] + "\n")
            print(f"[{i}/{len(videos)}] {v['video_id']}: {len(rows)} comments")
    except QuotaExceeded:
        print("daily quota exhausted; re-run tomorrow to resume")

    known = {r["author_channel_id"] for r in read_jsonl(out / "authors.jsonl")}
    wanted = {r["author_channel_id"] for r in read_jsonl(out / "comments.jsonl") if r["author_channel_id"]} - known
    if wanted:
        try:
            append_jsonl(out / "authors.jsonl", fetch_authors(wanted))
        except QuotaExceeded:
            print("quota exhausted before author metadata; re-run to finish")
    print("done")


if __name__ == "__main__":
    main()
