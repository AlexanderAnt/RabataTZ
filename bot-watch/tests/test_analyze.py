import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analyze  # noqa: E402

T0 = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)
ORGANIC_TEXTS = [
    "Интересно, а кто будет за это платить? Опять мы, налогоплательщики, как всегда.",
    "Спасибо за репортаж, давно хотел понять, что там происходит на самом деле.",
    "Цены в магазинах растут каждый месяц, зарплаты стоят на месте уже третий год.",
    "Хорошо бы сделать продолжение про транспорт, в Пурвциемсе автобусы ходят ужасно.",
    "Странно, что об этом не писали раньше, ситуация тянется с прошлой весны.",
]
BOT_TEXT = "Латвия давно потеряла суверенитет, всё решают в Брюсселе, а люди просто молчат и терпят"


def c(i, video, author, minutes, text):
    return {
        "video_id": video, "comment_id": f"c{i}", "parent_id": None,
        "author_channel_id": author, "author_name": author.upper(),
        "text": text, "published_at": (T0 + timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z"),
        "like_count": 0,
    }


def synthetic(seed=0):
    rng = random.Random(seed)
    comments, authors = [], {}
    n = 0
    # 40 organic users, random videos, random times, varied texts
    for u in range(40):
        aid = f"organic{u}"
        authors[aid] = {"author_channel_id": aid, "created_at": (T0 - timedelta(days=rng.randint(100, 4000))).isoformat()}
        for _ in range(rng.randint(1, 6)):
            v = rng.randrange(20)
            text = rng.choice(ORGANIC_TEXTS) + f" {rng.randint(0, 10**6)}"
            comments.append(c(n, f"v{v}", aid, v * 1440 + rng.randint(0, 1400), text)); n += 1
    # 5 bots, created within 10 days, all hit videos 2, 5, 9, 13 within minutes, near-identical text
    for b in range(5):
        aid = f"bot{b}"
        authors[aid] = {"author_channel_id": aid, "created_at": (T0 - timedelta(days=30 + b * 2)).isoformat()}
        for v in (2, 5, 9, 13):
            text = BOT_TEXT + ("!" * b)
            comments.append(c(n, f"v{v}", aid, v * 1440 + 30 + b * 2, text)); n += 1
    return comments, authors


def test_normalize_strips_noise():
    assert analyze.normalize("Привет!!! https://x.y/z @user  МИР") == "привет url мир"


def test_copy_paste_cluster_contains_exactly_the_bots():
    comments, _ = synthetic()
    clusters = analyze.duplicate_clusters(comments)
    bot_cluster = [cl for cl in clusters if any(r["author_channel_id"].startswith("bot") for r in cl)]
    assert len(bot_cluster) == 1
    assert {r["author_channel_id"] for r in bot_cluster[0]} == {f"bot{b}" for b in range(5)}


def test_short_texts_are_ignored():
    comments = [c(i, "v1", f"u{i}", i, "согласен") for i in range(10)]
    assert analyze.duplicate_clusters(comments) == []


def test_same_author_repeating_is_not_a_cluster():
    comments = [c(i, f"v{i}", "u1", i * 100, BOT_TEXT) for i in range(5)]
    assert analyze.duplicate_clusters(comments) == []


def test_coactivity_finds_bot_group_and_no_organic():
    comments, _ = synthetic()
    groups = analyze.coactivity_groups(analyze.coactivity_pairs(comments))
    assert {frozenset(g) for g in groups} == {frozenset(f"bot{b}" for b in range(5))}


def test_coactivity_respects_window():
    comments = []
    for v in range(5):
        comments.append(c(2 * v, f"v{v}", "a", v * 1000, "x"))
        comments.append(c(2 * v + 1, f"v{v}", "b", v * 1000 + 60, "y"))  # 60 min apart
    assert analyze.coactivity_pairs(comments, window_min=15) == {}
    assert len(analyze.coactivity_pairs(comments, window_min=90)[("a", "b")]) == 5


def test_bot_creation_spread_is_tighter_than_baseline():
    _, authors = synthetic()
    bots = [f"bot{b}" for b in range(5)]
    spread, _ = analyze.creation_spread_days(authors, bots)
    assert spread == 8
    assert analyze.baseline_creation_spread(authors, 5) > 100


def test_report_hides_names_by_default():
    comments, authors = synthetic()
    text = analyze.report(comments, authors, {})
    assert "BOT0" not in text and "bot0" not in text
    assert analyze.pseudo("bot0") in text
    assert "BOT0" in analyze.report(comments, authors, {}, show_names=True)
