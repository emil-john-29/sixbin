# Arbeitsanweisung: Automatische Recherche für SixBin

Diese Datei steuert die geplante Aufgabe, die regelmäßig neue Inhalte für die App SixBin
(inoffizielle Fan-App zu GTA VI) recherchiert und in `content.json` einträgt.
**Modus: vollautomatisch.** Gültige Änderungen werden ohne manuelle Freigabe veröffentlicht.
Deshalb gelten die Regeln unten streng.

## Zwei Sprachen
Es gibt zwei Inhaltsdateien mit **identischer Struktur**: `content.json` (Deutsch) und
`content.en.json` (Englisch). Jeder neue oder geänderte Eintrag wird in **beiden** Dateien
gepflegt: gleiche `id`, gleiche Zahlen, Preise, Codes und Zeitstempel, nur die Texte übersetzt
(name/title/text/effect/note/group/tag/facts). Eigennamen aus dem Spiel (z. B. Vice City,
Trophäen-Namen, App-Namen) bleiben unverändert. Die englischen Texte klingen natürlich, nicht
wörtlich übersetzt. Danach **beide** Dateien mit `tools/validate.py` prüfen.

## Ablauf bei jedem Lauf
1. `content.json` lesen und merken, was schon drin ist (Cheat-Namen, Datenbank-IDs, Tipp-Titel, News).
2. Im Web nach **Neuem seit dem letzten Lauf** suchen (deutsch und englisch):
   - Cheat-Codes für GTA VI (PS5, Xbox Series X|S, ggf. Handy-Cheats)
   - Fahrzeuge, Waffen, Immobilien/Geschäfte mit Preis, Händler und Klasse
   - Orte, Sammelobjekte, Fundorte
   - Offizielle News von Rockstar (Updates, Patches, Events, PC-Version, GTA Online)
   - Gute Einsteiger-Tipps
3. Für jeden Fund die **Regeln** unten prüfen. Was nicht passt, wird nicht eingetragen.
4. Neue Einträge hinzufügen, nie bestehende löschen. Korrekturen sind erlaubt, wenn mehrere Quellen
   einen Fehler belegen. Dann `added` nicht ändern und eine News-Zeile dazu schreiben.
5. `updatedAt` auf das heutige Datum setzen.
6. `python3 tools/validate.py content.json` und `python3 tools/validate.py content.en.json` ausführen. **Nur bei „✓ … gültig“ committen und pushen.**
   Bei Fehlern: korrigieren oder die betroffenen neuen Einträge wieder entfernen.
7. Commit-Nachricht: `Inhalte: +2 Cheats, +1 Fahrzeug, 1 News` (kurz, was dazukam).
8. Gibt es nichts Neues, wird nichts geändert und nichts committet.

## Regeln (Pflicht)
- **Zwei-Quellen-Regel:** Cheats, Preise und Werte nur eintragen, wenn **mindestens zwei voneinander
  unabhängige, seriöse Quellen** übereinstimmen (z. B. IGN, GameStar, GamePro, GIGA, PC Games,
  Eurogamer, GTABase, Rockstar Newswire). Foren und Social-Media-Posts allein reichen nicht.
- **Offizielle Rockstar-Infos** (Rockstar Newswire / rockstargames.com) reichen als einzige Quelle.
- **Keine Leaks**, keine Gerüchte als Fakt, keine Spekulationen. Gerüchte höchstens als News mit
  dem Wort „Gerücht“ und nur, wenn große Seiten berichten.
- **Eigene Worte:** Texte (Tipps, Notizen, News) immer selbst formulieren, auf Deutsch, nie
  fremde Guide-Texte kopieren. Fakten wie Codes, Preise und Namen dürfen übernommen werden.
- **Keine Bilder, Logos oder Dateien** von Rockstar oder anderen Seiten.
- **Datenbankrecht beachten:** Nie eine fremde Liste oder Tabelle (z. B. einen kompletten Guide)
  am Stück übernehmen. Nur einzelne Fakten, aus mehreren Quellen abgeglichen, mit eigener Struktur
  und eigenen Beschreibungen. Bevorzugt offizielle Rockstar-Angaben und Fakten, die im Spiel selbst
  sichtbar sind.
- **Keine Spoiler:** Keine Story-Missionsnamen, Wendungen oder Enden. Story-Bezüge nur als
  „Kapitel 3“ oder „Story-Mission in Kapitel 3“.
- **Keine Inhalte, die zum Schummeln online anleiten** (Glitches, Mods, Hacks, Geld-Exploits für
  GTA Online). Einzelspieler-Cheats von Rockstar sind in Ordnung.
- **`verified` immer `false`** setzen. Nur der App-Betreiber setzt nach eigenem Test `true`.
- **Keine erfundenen Werte.** Gibt es keine verlässlichen Zahlen für Tempo/Handling usw., lässt
  man `stats` weg und trägt nur Name, Klasse, Preis und Händler ein.
- Bei Unsicherheit: **weglassen.**

## Datenformat (Auszug)
Zeitstempel `added` immer in UTC: `"2026-11-19T08:30:00Z"` (Zeitpunkt des Eintragens).

Cheat:
```json
{ "name": "Unverwundbarkeit", "effect": "5 Minuten unverwundbar", "category": "Spieler",
  "ps": ["→","✕","→","←","R1"], "xbox": ["→","A","→","←","RB"], "phone": "1-999-…",
  "verified": false, "added": "2026-11-19T08:30:00Z" }
```
Kategorien für Cheats: `Spieler`, `Waffen`, `Fahrzeuge`, `Welt`.
Tasten: PlayStation `✕ ○ △ □ L1 L2 R1 R2 ← → ↑ ↓`, Xbox `A B X Y LB LT RB RT ← → ↑ ↓`.
`name` ist die ID und muss eindeutig sein.

Datenbank-Eintrag (in `database.categories[…].items`):
```json
{ "id": "fahrzeug-name-in-kleinbuchstaben", "name": "Fahrzeugname", "group": "Sportwagen",
  "price": 1250000, "source": "Händlername",
  "stats": { "speed": 92, "accel": 88, "handling": 81, "braking": 79 },
  "facts": [ { "label": "Sitze", "value": "2" } ],
  "note": "Kurzer eigener Satz.", "verified": false, "added": "2026-11-19T08:30:00Z",
  "map": { "x": 0.8, "y": 0.74 } }
```
- Kategorien und ihre Werte: `vehicles` (speed, accel, handling, braking),
  `weapons` (damage, firerate, accuracy, range), `properties` (keine Werte), `places` (keine Werte).
- `id`: klein, mit Bindestrichen, eindeutig über alle Kategorien.
- `map` nur, wenn der Ort auf der schematischen Karte sinnvoll ist (0–1, x = West→Ost, y = Nord→Süd).

News: `{ "date": "2026-11-19T10:00:00Z", "text": "Ein Satz in eigenen Worten." }`, neueste oben.
Tipp: `{ "tag": "Einsteiger", "title": "…", "text": "…", "added": "…" }`.
