# 🎙️ Podcast — Repozytorium

## Struktura

```
podcast/
├── episodes/
│   └── {numer}-{slug}/
│       ├── index.md          ← opis, timestamps, linki, sponsor
│       ├── transcript.md     ← transkrypcja (opcjonalnie)
│       └── assets/
│           ├── cover.jpg
│           └── thumbnail.jpg
├── guests/
│   ├── {slug}.md             ← bio i lista odcinków gościa
│   └── GUESTS.md             ← generowany automatycznie
├── templates/
│   ├── episode.md            ← szablon nowego odcinka
│   └── guest.md              ← szablon nowego gościa
├── scripts/
│   └── generate-index.py     ← generuje INDEX, STATUS, TAGS, GUESTS
├── INDEX.md                  ← generowany automatycznie
├── STATUS.md                 ← generowany automatycznie
└── TAGS.md                   ← generowany automatycznie
```

## Nowy odcinek — krok po kroku

```bash
# 1. Skopiuj szablon
cp templates/episode.md episodes/1416-tytul-odcinka/index.md

# 2. Stwórz folder na assets
mkdir -p episodes/1416-tytul-odcinka/assets

# 3. Uzupełnij index.md

# 4. Jeśli gość jest nowy — dodaj profil
cp templates/guest.md guests/imie-nazwisko.md

# 5. Wygeneruj indeksy
python3 scripts/generate-index.py
```

## Statusy odcinków

| Status | Znaczenie |
|--------|-----------|
| `draft` | Temat zaplanowany, brak nagrania |
| `recorded` | Nagrane, czeka na edycję |
| `editing` | W trakcie edycji audio/wideo |
| `published` | Opublikowane na wszystkich platformach |

## Generowanie indeksów

```bash
pip install pyyaml
python3 scripts/generate-index.py
```

Generuje 4 pliki: `INDEX.md`, `STATUS.md`, `TAGS.md`, `guests/GUESTS.md`.

> 💡 Dodaj to jako GitHub Action żeby indeksy aktualizowały się automatycznie przy każdym pushu.
