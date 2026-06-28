#!/usr/bin/env python3
"""
generate-index.py
-----------------
Skanuje wszystkie odcinki w episodes/ i generuje:
  - INDEX.md        — pełna tabela odcinków
  - STATUS.md       — odcinki według statusu produkcji
  - TAGS.md         — odcinki pogrupowane po tagach
  - guests/GUESTS.md — lista gości z liczbą odcinków

Użycie:
    python3 scripts/generate-index.py
"""

import os
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Instaluję PyYAML...")
    os.system("pip install pyyaml -q")
    import yaml


ROOT = Path(__file__).parent.parent
EPISODES_DIR = ROOT / "episodes"
OUTPUT_INDEX = ROOT / "INDEX.md"
OUTPUT_STATUS = ROOT / "STATUS.md"
OUTPUT_TAGS = ROOT / "TAGS.md"
OUTPUT_GUESTS = ROOT / "guests" / "GUESTS.md"


def parse_frontmatter(filepath: Path) -> dict:
    """Wyciąga YAML frontmatter z pliku markdown."""
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def load_all_episodes() -> list[dict]:
    """Wczytuje wszystkie odcinki, sortuje malejąco po numerze."""
    episodes = []
    if not EPISODES_DIR.exists():
        return episodes

    for folder in EPISODES_DIR.iterdir():
        if not folder.is_dir():
            continue
        index_file = folder / "index.md"
        if not index_file.exists():
            continue
        data = parse_frontmatter(index_file)
        if not data:
            continue
        data["_folder"] = folder.name
        episodes.append(data)

    return sorted(episodes, key=lambda e: e.get("episode", 0), reverse=True)


def format_date(val) -> str:
    if not val:
        return "—"
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d")
    return str(val)


def status_emoji(status: str) -> str:
    return {
        "published": "✅",
        "editing":   "✂️",
        "recorded":  "🎙️",
        "draft":     "📝",
    }.get(status, "❓")


# ──────────────────────────────────────────────
# INDEX.md — pełna lista odcinków
# ──────────────────────────────────────────────
def generate_index(episodes: list[dict]):
    lines = [
        "# Wszystkie odcinki\n",
        f"_Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        f"Łącznie odcinków: **{len(episodes)}**\n",
        "",
        "| # | Tytuł | Gość | Data | Czas | Status |",
        "|---|-------|------|------|------|--------|",
    ]
    for ep in episodes:
        num     = ep.get("episode", "?")
        title   = ep.get("title", "Brak tytułu")
        guest   = ep.get("guest", "—")
        date    = format_date(ep.get("date"))
        dur     = ep.get("duration", "—")
        status  = ep.get("status", "draft")
        folder  = ep.get("_folder", "")
        link    = f"[{title}](episodes/{folder}/index.md)"
        lines.append(f"| {num} | {link} | {guest} | {date} | {dur} | {status_emoji(status)} {status} |")

    OUTPUT_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ INDEX.md — {len(episodes)} odcinków")


# ──────────────────────────────────────────────
# STATUS.md — odcinki według statusu
# ──────────────────────────────────────────────
def generate_status(episodes: list[dict]):
    groups: dict[str, list] = {}
    for ep in episodes:
        s = ep.get("status", "draft")
        groups.setdefault(s, []).append(ep)

    order = ["draft", "recorded", "editing", "published"]
    lines = [
        "# Status produkcji\n",
        f"_Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
    ]
    for s in order:
        eps = groups.get(s, [])
        if not eps:
            continue
        lines.append(f"\n## {status_emoji(s)} {s.capitalize()} ({len(eps)})\n")
        for ep in eps:
            num   = ep.get("episode", "?")
            title = ep.get("title", "Brak tytułu")
            folder = ep.get("_folder", "")
            lines.append(f"- **#{num}** [{title}](episodes/{folder}/index.md)")

    OUTPUT_STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ STATUS.md — {sum(len(v) for v in groups.values())} odcinków w {len(groups)} statusach")


# ──────────────────────────────────────────────
# TAGS.md — odcinki według tagów
# ──────────────────────────────────────────────
def generate_tags(episodes: list[dict]):
    tag_map: dict[str, list] = {}
    for ep in episodes:
        for tag in ep.get("tags") or []:
            tag_map.setdefault(tag, []).append(ep)

    lines = [
        "# Odcinki według tagów\n",
        f"_Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
    ]
    for tag in sorted(tag_map):
        eps = tag_map[tag]
        lines.append(f"\n## `{tag}` ({len(eps)})\n")
        for ep in eps:
            num    = ep.get("episode", "?")
            title  = ep.get("title", "Brak tytułu")
            folder = ep.get("_folder", "")
            lines.append(f"- **#{num}** [{title}](episodes/{folder}/index.md)")

    OUTPUT_TAGS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ TAGS.md — {len(tag_map)} unikalnych tagów")


# ──────────────────────────────────────────────
# GUESTS.md — lista gości z liczbą wystąpień
# ──────────────────────────────────────────────
def generate_guests(episodes: list[dict]):
    guest_map: dict[str, list] = {}
    for ep in episodes:
        guest = ep.get("guest")
        if guest:
            guest_map.setdefault(guest, []).append(ep)

    lines = [
        "# Goście\n",
        f"_Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        f"Unikalnych gości: **{len(guest_map)}**\n",
        "",
        "| Gość | Odcinki | Ostatni |",
        "|------|---------|---------|",
    ]
    for guest, eps in sorted(guest_map.items(), key=lambda x: -len(x[1])):
        count   = len(eps)
        last_ep = eps[0]  # już posortowane malejąco po numerze
        last    = f"#{last_ep.get('episode')} {last_ep.get('title', '')}"
        folder  = last_ep.get("_folder", "")
        guest_file = f"[{guest}](../{guest}.md)" if (ROOT / "guests" / f"{guest}.md").exists() else guest
        lines.append(f"| {guest_file} | {count} | [{last}](../episodes/{folder}/index.md) |")

    OUTPUT_GUESTS.parent.mkdir(exist_ok=True)
    OUTPUT_GUESTS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ GUESTS.md — {len(guest_map)} gości")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("🎙️  Generuję indeksy podcastu...\n")
    episodes = load_all_episodes()
    if not episodes:
        print("⚠️  Brak odcinków w episodes/")
    else:
        generate_index(episodes)
        generate_status(episodes)
        generate_tags(episodes)
        generate_guests(episodes)
        print(f"\n🎉 Gotowe! Przetworzono {len(episodes)} odcinków.")
