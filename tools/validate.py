#!/usr/bin/env python3
"""Prüft content.json, bevor sie veröffentlicht wird.

Aufruf:  python3 tools/validate.py content.json
Exit-Code 0 = alles gut, 1 = Fehler (dann NICHT veröffentlichen).
Die App stürzt bei kaputten Daten nicht ab, zeigt dann aber keine Updates –
deshalb muss jede Änderung hier durch.
"""
import json
import sys
from datetime import datetime

errors: list[str] = []
warnings: list[str] = []

KNOWN_KEYS = {"✕", "○", "△", "□", "A", "B", "X", "Y", "←", "→", "↑", "↓",
              "L1", "L2", "L3", "R1", "R2", "R3", "LB", "LT", "LS", "RB", "RT", "RS"}


def err(msg: str) -> None:
    errors.append(msg)


def check_date(value, where: str, required: bool = False) -> None:
    if value is None:
        if required:
            err(f"{where}: Datum fehlt")
        return
    try:
        if "T" in value:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            datetime.strptime(value, "%Y-%m-%d")
    except (ValueError, TypeError):
        err(f"{where}: ungültiges Datum {value!r} (erwartet 2026-11-19 oder 2026-11-19T08:30:00Z)")


def need(obj: dict, key: str, typ, where: str) -> None:
    if key not in obj:
        err(f"{where}: Feld '{key}' fehlt")
    elif not isinstance(obj[key], typ):
        err(f"{where}: Feld '{key}' hat falschen Typ")


def main(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"FEHLER: Datei nicht lesbar oder kein gültiges JSON: {e}")
        return 1

    for key, typ in [("releaseDate", str), ("news", list), ("infos", list), ("tips", list),
                     ("cheats", list), ("checklists", list)]:
        need(data, key, typ, "Datei")
    check_date(data.get("releaseDate"), "releaseDate", required=True)
    check_date(data.get("updatedAt"), "updatedAt")

    for i, n in enumerate(data.get("news", [])):
        need(n, "date", str, f"news[{i}]")
        need(n, "text", str, f"news[{i}]")
        check_date(n.get("date"), f"news[{i}]")

    for i, info in enumerate(data.get("infos", [])):
        need(info, "title", str, f"infos[{i}]")
        need(info, "text", str, f"infos[{i}]")

    tip_titles = set()
    for i, t in enumerate(data.get("tips", [])):
        for k in ("tag", "title", "text"):
            need(t, k, str, f"tips[{i}]")
        check_date(t.get("added"), f"tips[{i}]")
        if t.get("title") in tip_titles:
            err(f"tips[{i}]: doppelter Titel {t.get('title')!r}")
        tip_titles.add(t.get("title"))

    cheat_names = set()
    for i, c in enumerate(data.get("cheats", [])):
        where = f"cheats[{i}] ({c.get('name')})"
        need(c, "name", str, where)
        need(c, "effect", str, where)
        check_date(c.get("added"), where)
        if c.get("name") in cheat_names:
            err(f"{where}: doppelter Name – der Name ist die ID und muss eindeutig sein")
        cheat_names.add(c.get("name"))
        if not c.get("ps") and not c.get("xbox") and not c.get("phone"):
            err(f"{where}: weder PS-, Xbox- noch Handy-Code angegeben")
        for platform in ("ps", "xbox"):
            for key in c.get(platform) or []:
                if key not in KNOWN_KEYS:
                    warnings.append(f"{where}: unbekannte Taste {key!r} bei {platform}")
        if not c.get("added"):
            warnings.append(f"{where}: kein 'added'-Zeitstempel – erscheint nicht im Neueste-Feed")

    seen_ids = set()
    for ci, cat in enumerate((data.get("database") or {}).get("categories", [])):
        cwhere = f"database.categories[{ci}] ({cat.get('id')})"
        for k in ("id", "title", "icon"):
            need(cat, k, str, cwhere)
        stat_ids = {s.get("id") for s in cat.get("stats", [])}
        for ii, item in enumerate(cat.get("items", [])):
            where = f"{cwhere}.items[{ii}] ({item.get('name')})"
            need(item, "id", str, where)
            need(item, "name", str, where)
            if item.get("id") in seen_ids:
                err(f"{where}: doppelte id {item.get('id')!r}")
            seen_ids.add(item.get("id"))
            check_date(item.get("added"), where)
            price = item.get("price")
            if price is not None and (not isinstance(price, int) or price < 0):
                err(f"{where}: price muss eine ganze Zahl ≥ 0 sein")
            for sid, value in (item.get("stats") or {}).items():
                if sid not in stat_ids:
                    err(f"{where}: Wert {sid!r} gibt es in dieser Kategorie nicht")
                if not isinstance(value, (int, float)) or not 0 <= value <= 100:
                    err(f"{where}: Wert {sid!r} muss zwischen 0 und 100 liegen")
            m = item.get("map")
            if m is not None and not (0 <= m.get("x", -1) <= 1 and 0 <= m.get("y", -1) <= 1):
                err(f"{where}: map.x/map.y müssen zwischen 0 und 1 liegen")

    size = len(json.dumps(data).encode())
    if size > 2_000_000:
        warnings.append(f"Datei ist groß ({size // 1024} KB) – Ladezeit beachten")

    for w in warnings:
        print("WARNUNG:", w)
    for e in errors:
        print("FEHLER:", e)
    if errors:
        print(f"\n✗ {len(errors)} Fehler – NICHT veröffentlichen.")
        return 1
    print(f"✓ content.json ist gültig ({len(data.get('cheats', []))} Cheats, "
          f"{sum(len(c.get('items', [])) for c in (data.get('database') or {}).get('categories', []))} Datenbank-Einträge).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "content.json"))
