"""Find coordination signals in collected YouTube comments.

Usage:
    python analyze.py data/rus_delfi_lv [data/rudelfi_lt ...] [--show-names]

Signals look at behaviour, not opinions:
  1. copy-paste: near-identical texts posted by different accounts;
  2. co-activity: account pairs that repeatedly comment on the same videos
     within a short time window;
  3. creation clusters: accounts in a group created within the same weeks.

Accounts are shown as short pseudonymous IDs unless --show-names is given.
The report is written next to the data (git-ignored).
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

MIN_TEXT_LEN = 40        # shorter texts ("согласен", "+") collide by chance
SHINGLE = 5
NUM_PERM = 64
BANDS = 16               # 16 bands x 4 rows -> ~0.7 Jaccard threshold
DUP_JACCARD = 0.7
CO_WINDOW_MIN = 15
CO_MIN_VIDEOS = 3


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def pseudo(author_id):
    return "a_" + hashlib.sha256(("bw:" + (author_id or "")).encode()).hexdigest()[:8]


def normalize(text):
    t = text.lower()
    t = re.sub(r"https?://\S+", " url ", t)
    t = re.sub(r"@\S+", " ", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def shingles(text, k=SHINGLE):
    return {text[i:i + k] for i in range(max(1, len(text) - k + 1))}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


_rng = random.Random(42)
_PERMS = [(_rng.randrange(1, 2**61 - 1), _rng.randrange(0, 2**61 - 1)) for _ in range(NUM_PERM)]
_P = 2**61 - 1


def minhash(sh):
    hs = [int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "big") for s in sh]
    return [min((a * h + b) % _P for h in hs) for a, b in _PERMS]


class DSU:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)

    def groups(self):
        g = defaultdict(list)
        for x in self.p:
            g[self.find(x)].append(x)
        return [v for v in g.values() if len(v) > 1]


def duplicate_clusters(comments):
    """Groups of near-identical comments written by at least 2 different accounts."""
    cands = []
    for i, c in enumerate(comments):
        n = normalize(c["text"])
        if len(n) >= MIN_TEXT_LEN and c.get("author_channel_id"):
            cands.append((i, shingles(n)))
    buckets = defaultdict(list)
    sigs = {}
    for i, sh in cands:
        sig = minhash(sh)
        sigs[i] = sh
        rows = NUM_PERM // BANDS
        for b in range(BANDS):
            buckets[(b, tuple(sig[b * rows:(b + 1) * rows]))].append(i)
    dsu = DSU()
    checked = set()
    for members in buckets.values():
        for a, b in itertools.combinations(members, 2):
            if (a, b) in checked:
                continue
            checked.add((a, b))
            if jaccard(sigs[a], sigs[b]) >= DUP_JACCARD:
                dsu.union(a, b)
    out = []
    for g in dsu.groups():
        rows = [comments[i] for i in g]
        authors = {r["author_channel_id"] for r in rows}
        if len(authors) >= 2:
            out.append(rows)
    return sorted(out, key=lambda rs: -len({r["author_channel_id"] for r in rs}))


def coactivity_pairs(comments, window_min=CO_WINDOW_MIN, min_videos=CO_MIN_VIDEOS):
    """Author pairs that commented within window_min of each other on >= min_videos videos."""
    by_video = defaultdict(list)
    for c in comments:
        if c.get("author_channel_id") and c.get("published_at"):
            by_video[c["video_id"]].append((parse_ts(c["published_at"]), c["author_channel_id"]))
    pair_videos = defaultdict(set)
    for vid, rows in by_video.items():
        rows.sort()
        for i, (t1, a1) in enumerate(rows):
            for t2, a2 in rows[i + 1:]:
                if (t2 - t1).total_seconds() > window_min * 60:
                    break
                if a1 != a2:
                    pair_videos[tuple(sorted((a1, a2)))].add(vid)
    return {p: v for p, v in pair_videos.items() if len(v) >= min_videos}


def coactivity_groups(pairs):
    dsu = DSU()
    for a, b in pairs:
        dsu.union(a, b)
    return sorted(dsu.groups(), key=len, reverse=True)


def creation_spread_days(authors_meta, group):
    dates = sorted(parse_ts(authors_meta[a]["created_at"]) for a in group if authors_meta.get(a, {}).get("created_at"))
    if len(dates) < 2:
        return None, dates
    return (dates[-1] - dates[0]).days, dates


def baseline_creation_spread(authors_meta, size, trials=200, seed=1):
    """Median creation-date spread of random groups of the same size (what 'normal' looks like)."""
    pool = [a for a, m in authors_meta.items() if m.get("created_at")]
    if len(pool) < size or size < 2:
        return None
    rng = random.Random(seed)
    spreads = [creation_spread_days(authors_meta, rng.sample(pool, size))[0] for _ in range(trials)]
    return statistics.median(spreads)


def load(dirs):
    comments, authors, videos = [], {}, {}
    for d in dirs:
        d = Path(d)
        for line in (d / "comments.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                comments.append(json.loads(line))
        if (d / "authors.jsonl").exists():
            for line in (d / "authors.jsonl").read_text(encoding="utf-8").splitlines():
                if line.strip():
                    m = json.loads(line)
                    authors[m["author_channel_id"]] = m
        if (d / "videos.jsonl").exists():
            for line in (d / "videos.jsonl").read_text(encoding="utf-8").splitlines():
                if line.strip():
                    v = json.loads(line)
                    videos[v["video_id"]] = v
    return comments, authors, videos


def report(comments, authors, videos, show_names=False):
    names = {c["author_channel_id"]: c["author_name"] for c in comments if c.get("author_channel_id")}
    label = (lambda a: f"{pseudo(a)} ({names.get(a, '?')})") if show_names else pseudo
    per_author = Counter(c["author_channel_id"] for c in comments if c.get("author_channel_id"))
    L = []
    L.append("# Coordination report\n")
    L.append(f"Comments: {len(comments)} · videos: {len({c['video_id'] for c in comments})} · accounts: {len(per_author)}\n")
    top = per_author.most_common(10)
    L.append("Most active accounts (activity alone is not a signal): " + ", ".join(f"{label(a)}={n}" for a, n in top) + "\n")

    dups = duplicate_clusters(comments)
    L.append(f"\n## 1. Copy-paste clusters: {len(dups)}\n")
    for rows in dups[:25]:
        accs = {r["author_channel_id"] for r in rows}
        vids = {r["video_id"] for r in rows}
        ts = sorted(r["published_at"] for r in rows)
        L.append(f"- **{len(accs)} accounts, {len(rows)} comments, {len(vids)} videos**, {ts[0][:16]} → {ts[-1][:16]}")
        L.append(f"  - accounts: {', '.join(sorted(label(a) for a in accs))}")
        L.append(f"  - text: «{rows[0]['text'][:200].replace(chr(10), ' ')}»")

    pairs = coactivity_pairs(comments)
    groups = coactivity_groups(pairs)
    L.append(f"\n## 2. Co-activity groups (≥{CO_MIN_VIDEOS} shared videos within {CO_WINDOW_MIN} min): {len(groups)}\n")
    for g in groups[:25]:
        gp = [(p, v) for p, v in pairs.items() if p[0] in g and p[1] in g]
        shared = set().union(*(v for _, v in gp))
        spread, _ = creation_spread_days(authors, g)
        base = baseline_creation_spread(authors, len(g))
        L.append(f"- **{len(g)} accounts**, {len(gp)} linked pairs, {len(shared)} videos; strongest pair shares {max(len(v) for _, v in gp)} videos")
        L.append(f"  - accounts: {', '.join(sorted(label(a) for a in g))}")
        if spread is not None:
            L.append(f"  - creation dates spread: {spread} days (random groups of this size: ~{base} days)")
        L.append(f"  - comments by these accounts: {sum(per_author[a] for a in g)}")

    L.append("\n## How to read this\n")
    L.append("- A cluster is a lead, not a verdict. Check the comments by hand before calling anything coordinated.")
    L.append("- Copy-paste can be innocent (quotes, slogans, repost of a link). Co-activity can be two regulars who watch every video.")
    L.append("- Strong cases combine signals: same text + same timing + accounts created together.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--show-names", action="store_true")
    a = ap.parse_args()
    comments, authors, videos = load(a.dirs)
    text = report(comments, authors, videos, a.show_names)
    out = Path(a.dirs[0]) / "report.md"
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {out}")


if __name__ == "__main__":
    main()
