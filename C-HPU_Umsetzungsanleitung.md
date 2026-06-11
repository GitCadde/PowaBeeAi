# C-HPU Power BI Bericht – Schritt-für-Schritt Umsetzungsanleitung

**Stand:** 10.06.2026  
**Ziel:** Vollständige Umsetzung des C-HPU Berichts in Power BI Desktop (PBIP)

---

## Inhaltsverzeichnis

1. [Ausgangslage & Vorbereitung](#1-ausgangslage--vorbereitung)
2. [Report-Grundeinstellungen anpassen](#2-report-grundeinstellungen-anpassen)
3. [Seitenstruktur anlegen](#3-seitenstruktur-anlegen)
4. [Seite 1 – Management Summary](#4-seite-1--management-summary)
5. [Seite 2 – Cockpit Vollk. Kreis](#5-seite-2--cockpit-vollk-kreis)
6. [Seite 3 – C-HPU Entwicklung](#6-seite-3--c-hpu-entwicklung)
7. [Seite 4 – Abweichungsanalyse Vollk. Kreis](#7-seite-4--abweichungsanalyse-vollk-kreis)
8. [Seite 5 – Abweichungsanalyse DE Direkt](#8-seite-5--abweichungsanalyse-de-direkt)
9. [Seite 6 – Werk-Detail (Drill-Through)](#9-seite-6--werk-detail-drill-through)
10. [Seite 7 – Kostenstellen-Detail (Drill-Through)](#10-seite-7--kostenstellen-detail-drill-through)
11. [Bedingte Formatierung & Ampellogik](#11-bedingte-formatierung--ampellogik)
12. [Slicer & Filter](#12-slicer--filter)
13. [Theme & Design-Richtlinien](#13-theme--design-richtlinien)
14. [Measure-Referenz pro Seite](#14-measure-referenz-pro-seite)
15. [Abschluss-Checkliste](#15-abschluss-checkliste)
16. [Bekannte Stolperfallen](#16-bekannte-stolperfallen)

---

## 1. Ausgangslage & Vorbereitung

### 1.1 Aktueller Stand

| Aspekt | Ist-Zustand |
|---|---|
| Projektformat | PBIP mit PBIR |
| Semantic Model | 2 Tabellen: `fakt_chpu` (Werk), `fakt_chpu_kst` (Kostenstelle) |
| Datenquelle | Power Platform Dataflows |
| Theme | CHPU_IBCS_Theme (IBCS-konform) |
| Vorhandene Seiten | 4 Seiten (3× Debug-Tabellen, 1× Summary-Entwurf) |
| Berichtsgröße | 1280×720 (**muss auf 1920×1080 geändert werden**) |
| Measures | ~105 Measures vorhanden (alle Kategorien, YTD, VSI, Deltas, Ampeln) |
| Drill-Through | **Noch nicht konfiguriert** |
| Slicer | **Noch nicht vorhanden** |

### 1.2 Vor dem Start

1. **PBIP in Power BI Desktop öffnen**: Datei `Test.pbip` doppelklicken
2. **Daten aktualisieren**: Start → Aktualisieren (um sicherzustellen, dass Daten geladen sind)
3. **Measures prüfen**: Im Modell-Bereich → `fakt_chpu` und `fakt_chpu_kst` aufklappen → alle Measures sichtbar?
4. **Git-Stand sichern**: `git add . && git commit -m "Vor Berichtsumbau"`

### 1.3 Checkliste Datenmodell

Sicherstellen, dass folgende Spalten in beiden Tabellen vorhanden sind:

| Spalte | `fakt_chpu` | `fakt_chpu_kst` |
|---|:---:|:---:|
| `source_plant_id` | ✅ | ✅ |
| `kst_bezeichnung_kurz` | – | ✅ |
| `jahr_kw` | ✅ | ✅ |
| `ze_ist` / `ze_soll` | ✅ | ✅ |
| `anmin_ist` / `anmin_soll` | ✅ | ✅ |
| `anmin_ist_d` / `_di` / `_i` | ✅ | ✅ |
| `anmin_soll_d` / `_di` / `_i` | ✅ | ✅ |
| `anmin_soll_ohne_ratio` | ✅ | ✅ |
| `anmin_soll_ohne_ratio_d` / `_di` / `_i` | ✅ | ✅ |
| `ratio_ist` / `ratio_soll` | ✅ | ✅ |
| `chpu_ist` / `chpu_soll` | ✅ | ✅ |

---

## 2. Report-Grundeinstellungen anpassen

### 2.1 Berichtsgröße ändern (1920×1080)

1. **Ansicht** → **Seitengröße** → **Benutzerdefiniert**
2. Breite: `1920`, Höhe: `1080`
3. → Auf **allen Seiten** anwenden

> **Alternativ im JSON** (`report.json`):
> ```json
> "layoutOptimization": 0,
> "pageSize": { "width": 1920, "height": 1080 }
> ```

### 2.2 Berichtseinstellungen prüfen

Unter **Datei → Optionen → Aktuelle Datei → Berichtseinstellungen**:

- [x] **Visuelle Interaktionen** aktivieren
- [x] **Erweiterte QuickInfos** aktivieren
- [x] **Drill-Through über Visuals** aktivieren
- [x] **Standardmäßig Kreuzfilterung anderer Visuals beim Filtern** aktiv lassen

---

## 3. Seitenstruktur anlegen

### 3.1 Debug-Seiten aufräumen

Die vorhandenen Debug-Seiten (Seite 1, Seite 2, Seite 3) enthalten nur Rohdaten-Tabellen für die Entwicklung. Sie sollten:

- **Ausgeblendet** werden (Rechtsklick → Seite ausblenden) – sie bleiben als Entwicklungshilfe erhalten
- ODER am Ende des Berichts belassen und mit Präfix `[DEV]` benannt werden

### 3.2 Neue Seiten anlegen

Erstelle die 7 Berichtsseiten in folgender Reihenfolge. Die Summary-Seite existiert bereits und wird zur Seite 1:

| Nr. | Seitenname | Typ | Datenquelle |
|---|---|---|---|
| 1 | **Management Summary** | Normal | `fakt_chpu` |
| 2 | **Cockpit Vollk. Kreis** | Normal | `fakt_chpu` |
| 3 | **C-HPU Entwicklung** | Normal | `fakt_chpu` |
| 4 | **Abweichungsanalyse Vollk. Kreis** | Normal | `fakt_chpu` |
| 5 | **Abweichungsanalyse DE Direkt** | Normal | `fakt_chpu` |
| 6 | **Werk-Detail** | **Drill-Through** | `fakt_chpu_kst` |
| 7 | **Kostenstellen-Detail** | **Drill-Through** | `fakt_chpu_kst` |

**Vorgehen:**
1. Rechtsklick auf Seitenreiter → **Neue Seite**
2. Doppelklick auf Reiter → Namen eingeben
3. Wiederholen bis alle 7 Seiten stehen

### 3.3 Seitenreihenfolge festlegen

Seiten per Drag & Drop in die richtige Reihenfolge bringen. Die Debug-Seiten ans Ende schieben und ausblenden.

---

## 4. Seite 1 – Management Summary

### 4.1 Layout-Konzept

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo]  Insight Factory - C-HPU-Bericht          KSU 0.2      │
│         Management Summary                                    │
├──────────────┬─────────────────────────────────────────────────┤
│              │                                                 │
│  Management  │  ┌─── KPI-Block 1 ───┐  ┌─── KPI-Block 2 ───┐ │
│  Summary     │  │ Werke grün:  X/Y   │  │ YTD Ratio: X.X%   │ │
│              │  └────────────────────┘  └────────────────────┘ │
│  (Sidebar    │                                                 │
│   Dunkelblau)│  ┌─── Kontext / Hintergrund ──────────────────┐ │
│              │  │ • X von Y Werken YTD Ist grün              │ │
│              │  │ • Zielerreichung X.X% YTD Ist (Ampel)      │ │
│              │  └────────────────────────────────────────────┘ │
│              │                                                 │
│              │  ┌─── Entscheidungsbedarfe ────────────────────┐ │
│              │  │ • Kenntnisnahme des aktuellen Standes.     │ │
│              │  └────────────────────────────────────────────┘ │
├──────────────┴─────────────────────────────────────────────────┤
│ Version 0.9 | Stand DD.MM.YYYY              [Datenschutz-Link]│
└────────────────────────────────────────────────────────────────┘
```

### 4.2 Bestehende Summary-Seite umbauen

Die vorhandene Summary-Seite hat bereits: Logo, Titel, Sidebar, Kontext-Card, Entscheidungsbedarf-Card. Ergänze:

#### KPI-Cards (3 Stück, oben rechts neben der Sidebar)

**Card 1: Anzahl Werke grün**
1. Einfügen → Visual → **Karte (neu)**
2. Feld: `Anzahl Werke Grün YTD`
3. Titel: „Werke grün YTD"
4. Position: x=370, y=80, Breite=200, Höhe=100
5. Kategorie-Label: „von [Anzahl Werke] Werken"

**Card 2: YTD Zielerreichung**
1. Einfügen → Visual → **Karte (neu)**
2. Feld: `Ratio Ist YTD`
3. Titel: „Ratio YTD"
4. Format: Prozent (0.0%)
5. Position: x=590, y=80, Breite=200, Höhe=100

**Card 3: VSI Zielerreichung**
1. Einfügen → Visual → **Karte (neu)**
2. Feld: `Ratio Ist VSI`
3. Titel: „Ratio VSI"
4. Format: Prozent (0.0%)
5. Position: x=810, y=80, Breite=200, Höhe=100

#### Bedingte Formatierung der KPI-Cards

Für jede KPI-Card:
1. Visual auswählen → Format → **Callout-Wert** → Schriftfarbe → **fx (bedingte Formatierung)**
2. Regeln:
   - Wenn Wert ≥ Ratio Soll YTD → **#00A650** (Grün)
   - Wenn Wert ≥ 0 → **#FFB800** (Gelb)
   - Sonst → **#E63946** (Rot)

### 4.3 Verwendete Measures

| Visual | Measure |
|---|---|
| KPI-Card 1 | `Anzahl Werke Grün YTD`, `Anzahl Werke` |
| KPI-Card 2 | `Ratio Ist YTD` |
| KPI-Card 3 | `Ratio Ist VSI` |
| Kontext-Card | `Management Summary Kontext` |
| Entscheidungsbedarf-Card | `Management Summary Entscheidungsbedarf` |
| Ampel-Indikator | `Ampel Gesamt YTD` |

---

## 5. Seite 2 – Cockpit Vollk. Kreis

### 5.1 Layout-Konzept

```
┌────────────────────────────────────────────────────────────────┐
│ C-HPU Cockpit – Vollkostenkreis           [Slicer: Jahr/KW]   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─ Matrix/Tabelle ──────────────────────────────────────────┐ │
│  │ Werk  │Trend│ CHPU  │ Ratio │ Ratio │ CHPU │ CHPU │ CHPU │ │
│  │       │     │ Soll  │  KW   │  YTD  │  KW  │  YTD │  VSI │ │
│  │       │     │       │       │  VSI  │      │      │      │ │
│  │───────┼─────┼───────┼───────┼───────┼──────┼──────┼──────│ │
│  │Werk A │  ▼  │ 11.2  │ 2.1%  │ 3.5%  │10.9  │10.8  │10.9 │ │
│  │Werk B │  ▲  │ 12.0  │ -0.5% │ 1.2%  │12.1  │11.8  │11.9 │ │
│  │ ...   │     │       │       │       │      │      │      │ │
│  │───────┴─────┴───────┴───────┴───────┴──────┴──────┴──────│ │
│  │                   ● Ampel-Punkte je Zeile (bedingt)       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 5.2 Schritt-für-Schritt

#### Seitentitel

1. Einfügen → **Textfeld**
2. Text: „C-HPU Cockpit – Vollkostenkreis"
3. Schriftgröße: 20pt, Fett
4. Position: x=40, y=10, Breite=600

#### Cockpit-Matrix

1. Einfügen → Visual → **Matrix**
2. Konfiguration:
   - **Zeilen**: `fakt_chpu[source_plant_id]`
   - **Werte** (in dieser Reihenfolge):

| # | Feld/Measure | Titel im Header | Format |
|---|---|---|---|
| 1 | `Trend CHPU` | Trend | Text |
| 2 | `CHPU Soll` | C-HPU Soll | #,##0.0 |
| 3 | `Ratio Ist` | Ratio KW | 0.0% |
| 4 | `Ratio Ist YTD` | Ratio YTD | 0.0% |
| 5 | `Ratio Ist VSI` | Ratio VSI | 0.0% |
| 6 | `CHPU Ist` | C-HPU KW | #,##0.0 |
| 7 | `CHPU Ist YTD` | C-HPU YTD | #,##0.0 |
| 8 | `CHPU Ist VSI` | C-HPU VSI | #,##0.0 |
| 9 | `Ampel Werk YTD` | Ampel | Text |

3. Position: x=40, y=60, Breite=1840, Höhe=960
4. Layout → **Gestuftes Layout deaktivieren** (Tabellendarstellung)
5. Zeilensummen **deaktivieren**

#### Bedingte Formatierung der Matrix

Für **Ratio-Spalten** (KW, YTD, VSI):
1. Spalte auswählen → Format → Bedingte Formatierung → **Hintergrundfarbe**
2. Formatieren nach: **Regeln**
   - Wenn ≥ Ratio Soll YTD → Hintergrund **#00A650**, Schrift **Weiß**
   - Wenn ≥ 0 → Hintergrund **#FFB800**, Schrift **Schwarz**
   - Wenn < 0 → Hintergrund **#E63946**, Schrift **Weiß**

Für **Ampel-Spalte**:
1. → Bedingte Formatierung → **Symbole** (oder Hintergrundfarbe)
2. Grün/Gelb/Rot basierend auf dem Textwert

Für **Trend-Spalte**:
1. → Schriftfarbe bedingt:
   - ▼ (Dreieck runter) → Rot
   - ▲ (Dreieck hoch) → Grün
   - ► (Pfeil rechts) → Grau

### 5.3 Drill-Through aktivieren

In der Matrix eine **Drill-Through-Aktion** einrichten:
1. Visual auswählen → Format → Aktionen
2. Typ: **Drill-Through auf Seite** → Ziel: „Werk-Detail"
3. Das Feld `source_plant_id` wird automatisch als Drill-Through-Parameter übertragen

### 5.4 Verwendete Measures

| Measure | Quelle |
|---|---|
| `Trend CHPU` | `fakt_chpu` |
| `CHPU Soll` | `fakt_chpu` |
| `CHPU Ist` | `fakt_chpu` |
| `CHPU Ist YTD` | `fakt_chpu` |
| `CHPU Ist VSI` | `fakt_chpu` |
| `Ratio Ist` | `fakt_chpu` |
| `Ratio Ist YTD` | `fakt_chpu` |
| `Ratio Ist VSI` | `fakt_chpu` |
| `Ampel Werk YTD` | `fakt_chpu` |

---

## 6. Seite 3 – C-HPU Entwicklung

### 6.1 Layout-Konzept

```
┌────────────────────────────────────────────────────────────────┐
│ C-HPU Entwicklung – Vollkostenkreis       [Slicer: Werk]      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌── Gestapelte Säulen + Linie ──────────────────────────────┐ │
│  │                                                            │ │
│  │  █ D  █ DI  █ I          ─── C-HPU Soll                  │ │
│  │  ████████████████████████████████████████████████████████  │ │
│  │  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █   │ │
│  │  ────────────────── C-HPU Soll Linie ──────────────────── │ │
│  │                                                            │ │
│  │  KW01  KW02  KW03  ...                         KW52       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌── KPIs ─────────────┐  ┌── ZE-Vergleich ─────────────────┐ │
│  │ Ratio YTD:  3.5%    │  │ ZE Ist:   12.500                │ │
│  │ Ratio VSI:  3.2%    │  │ ZE Soll:  13.000                │ │
│  │ CHPU Ist YTD: 10.8  │  │ Delta:    -500                  │ │
│  │ CHPU Soll YTD: 11.2 │  │                                 │ │
│  └──────────────────────┘  └─────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### 6.2 Schritt-für-Schritt

#### Seitentitel

1. Einfügen → **Textfeld**: „C-HPU Entwicklung – Vollkostenkreis"
2. Schriftgröße: 20pt, Fett
3. Position: x=40, y=10

#### Slicer: Werk

1. Einfügen → Visual → **Datenschnitt (Slicer)**
2. Feld: `fakt_chpu[source_plant_id]`
3. Stil: **Dropdown**
4. Position: x=1500, y=10, Breite=380, Höhe=40
5. Einfachauswahl aktivieren (für Werkfokus) ODER Mehrfachauswahl (für Vergleich)

#### Gestapeltes Säulendiagramm mit Linie (Kombi-Chart)

1. Einfügen → Visual → **Linien- und gestapeltes Säulendiagramm**
2. Konfiguration:
   - **X-Achse**: `fakt_chpu[jahr_kw]`
   - **Säulenwerte (gestapelt)**:
     1. `CHPU Ist D` (Direkt VBZ) — Farbe: **#1B3A5C** (Dunkelblau)
     2. `CHPU Ist DI` (Direkt Indirekt) — Farbe: **#4A8DB7** (Mittelblau)
     3. `CHPU Ist I` (Indirekt) — Farbe: **#A8D0E6** (Hellblau)
   - **Linienwerte**:
     1. `CHPU Soll` — Farbe: **#333333** (Dunkelgrau), gestrichelt

3. Position: x=40, y=60, Breite=1840, Höhe=580
4. Format:
   - Y-Achse: Titel „min/ZE"
   - X-Achse: Titel „Kalenderwoche"
   - Legende: Oben, Horizontal
   - Datenbeschriftungen: Aus (zu viele Balken)

#### KPI-Cards (links unten)

| Card | Measure | Format |
|---|---|---|
| Ratio YTD | `Ratio Ist YTD` | 0.0% |
| Ratio VSI | `Ratio Ist VSI` | 0.0% |
| C-HPU Ist YTD | `CHPU Ist YTD` | #,##0.0 |
| C-HPU Soll YTD | `CHPU Soll YTD` | #,##0.0 |

Jede Card: Breite=200, Höhe=80, nebeneinander ab x=40, y=680

#### ZE-Vergleichsbox (rechts unten)

1. Einfügen → Visual → **Tabelle** (tableEx)
2. Spalten:
   - `ZE Ist YTD` (Titel: „ZE Ist")
   - `ZE Soll YTD` (Titel: „ZE Soll")
   - `Delta ZE YTD` (Titel: „Delta")
3. Position: x=900, y=680, Breite=500, Höhe=120
4. Bedingte Formatierung `Delta ZE YTD`:
   - Positiv → Grün
   - Negativ → Rot

### 6.3 Verwendete Measures

```
CHPU Ist D, CHPU Ist DI, CHPU Ist I
CHPU Soll
Ratio Ist YTD, Ratio Ist VSI
CHPU Ist YTD, CHPU Soll YTD
ZE Ist YTD, ZE Soll YTD, Delta ZE YTD
```

---

## 7. Seite 4 – Abweichungsanalyse Vollk. Kreis

### 7.1 Layout-Konzept

```
┌────────────────────────────────────────────────────────────────┐
│ Abweichungsanalyse – Vollkostenkreis      [Slicer: KW/Werk]   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌── Abweichungstabelle ─────────────────────────────────────┐ │
│  │ Werk │ AnMin │ AnMin │Delta │ AnMin │ AnMin │Delta │ ...  │ │
│  │      │ Ist   │ Soll  │ MA   │Ist D  │Soll D │ D    │      │ │
│  │──────┼───────┼───────┼──────┼───────┼───────┼──────┼──────│ │
│  │W-A   │12.000 │11.500 │ +500 │ 8.000 │ 7.800 │ +200 │      │ │
│  │W-B   │ 9.500 │ 9.800 │ -300 │ 6.500 │ 6.700 │ -200 │      │ │
│  │──────┴───────┴───────┴──────┴───────┴───────┴──────┴──────│ │
│  │  ████ Datenbalken für Deltas          Bedingte Farben     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌── Ratio-Vergleich ────┐  ┌── Delta-Wasserfall ────────────┐ │
│  │ Ratio Ist vs. Soll    │  │  D: +200                       │ │
│  │ (Clustered Bars)      │  │  DI: +50                       │ │
│  │                       │  │  I: +250                       │ │
│  │                       │  │  Gesamt: +500                  │ │
│  └───────────────────────┘  └────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### 7.2 Schritt-für-Schritt

#### Seitentitel + Slicer

Wie auf den vorherigen Seiten: Textfeld + Werk-Slicer + KW-Slicer

#### Abweichungstabelle (Matrix)

1. Einfügen → Visual → **Matrix**
2. **Zeilen**: `fakt_chpu[source_plant_id]`
3. **Werte**:

| # | Measure | Spaltenheader | Format |
|---|---|---|---|
| 1 | `AnMin Ist` | MA Ist | #,##0 |
| 2 | `AnMin Soll` | MA Soll | #,##0 |
| 3 | `Delta AnMin` | Δ MA | #,##0 |
| 4 | `AnMin Ist D` | MA Ist D | #,##0 |
| 5 | `AnMin Soll D` | MA Soll D | #,##0 |
| 6 | `Delta AnMin D` | Δ D | #,##0 |
| 7 | `AnMin Ist DI` | MA Ist DI | #,##0 |
| 8 | `AnMin Soll DI` | MA Soll DI | #,##0 |
| 9 | `Delta AnMin DI` | Δ DI | #,##0 |
| 10 | `AnMin Ist I` | MA Ist I | #,##0 |
| 11 | `AnMin Soll I` | MA Soll I | #,##0 |
| 12 | `Delta AnMin I` | Δ I | #,##0 |
| 13 | `Ratio Ist` | Ratio Ist | 0.0% |
| 14 | `Ratio Soll` | Ratio Soll | 0.0% |

4. Position: x=40, y=60, Breite=1840, Höhe=520

#### Bedingte Formatierung – Datenbalken

Für alle Delta-Spalten (Δ MA, Δ D, Δ DI, Δ I):
1. Spalte → Format → Bedingte Formatierung → **Datenbalken**
2. Positiv: **#00A650** (Grün) → ACHTUNG: Bei C-HPU ist negatives Delta BESSER (weniger AnMin)
3. **Umkehrlogik**: Negative Werte = Grün, Positive = Rot
   - Minimum-Farbe: **#00A650** (Grün)
   - Maximum-Farbe: **#E63946** (Rot)

> **Wichtig:** Da niedrigere AnMin besser ist, bedeutet ein **negativer** Delta (Ist < Soll) eine **gute** Performance. Die Farblogik muss invertiert sein!

#### Wasserfall-Diagramm (Delta-Zerlegung)

1. Einfügen → Visual → **Wasserfall**
2. Kategorie: Erstelle ein berechnetes Feld oder nutze 3 Cards nebeneinander:
   - `Delta AnMin D` → „Direkt VBZ"
   - `Delta AnMin DI` → „Direkt Indirekt"
   - `Delta AnMin I` → „Indirekt"
3. Position: x=1000, y=600, Breite=840, Höhe=420

**Alternative ohne Wasserfall:** 3 KPI-Cards nebeneinander mit Delta-Werten und bedingter Farbformatierung.

#### Ratio-Vergleich (Gruppierte Balken)

1. Einfügen → Visual → **Gruppiertes Balkendiagramm**
2. Y-Achse: `fakt_chpu[source_plant_id]`
3. X-Achse-Werte:
   - `Ratio Ist` (Farbe: **#1B3A5C**)
   - `Ratio Soll` (Farbe: **#B0B0B0**)
4. Position: x=40, y=600, Breite=920, Höhe=420

### 7.3 Verwendete Measures

```
AnMin Ist, AnMin Soll, Delta AnMin
AnMin Ist D, AnMin Soll D, Delta AnMin D
AnMin Ist DI, AnMin Soll DI, Delta AnMin DI
AnMin Ist I, AnMin Soll I, Delta AnMin I
Ratio Ist, Ratio Soll
```

---

## 8. Seite 5 – Abweichungsanalyse DE Direkt

### 8.1 Konzept

Diese Seite ist identisch mit Seite 4, aber **gefiltert auf Kategorie „Direkt"** (D). Sie zeigt nur die direkten AnMin und deren Abweichung.

### 8.2 Umsetzung

#### Option A: Seitenfilter (empfohlen)

Da die Daten nicht explizit eine Kategorie-Spalte haben, sondern die Kategorien als separate Spalten vorliegen (_d, _di, _i), ist ein Seitenfilter nicht direkt möglich. Stattdessen:

#### Option B: Eigene Measures verwenden

1. **Seite 4 duplizieren**: Rechtsklick auf Seite 4 → „Seite duplizieren"
2. **Seitentitel ändern**: „Abweichungsanalyse – DE Direkt"
3. **Matrix anpassen** – nur direkte Measures verwenden:

| # | Measure | Spaltenheader |
|---|---|---|
| 1 | `AnMin Ist D` | MA Ist Direkt |
| 2 | `AnMin Soll D` | MA Soll Direkt |
| 3 | `Delta AnMin D` | Δ Direkt |
| 4 | `Ratio Ist D` | Ratio Ist D |
| 5 | `Ratio Soll D` | Ratio Soll D |
| 6 | `CHPU Ist D` | C-HPU Ist D |
| 7 | `CHPU Soll D` | C-HPU Soll D |

4. **Ratio-Balkendiagramm** anpassen:
   - `Ratio Ist D` statt `Ratio Ist`
   - `Ratio Soll D` statt `Ratio Soll`

5. **YTD-Cards** anpassen:
   - `Ratio Ist D YTD`
   - `Delta AnMin D YTD`

### 8.3 Verwendete Measures

```
AnMin Ist D, AnMin Soll D, Delta AnMin D
Ratio Ist D, Ratio Soll D
CHPU Ist D, CHPU Soll D
Ratio Ist D YTD
Delta AnMin D YTD
```

---

## 9. Seite 6 – Werk-Detail (Drill-Through)

### 9.1 Drill-Through konfigurieren

1. Seite „Werk-Detail" auswählen
2. Im **Visualisierungsbereich** → Felder → **Drillthrough hinzufügen**:
   - `fakt_chpu[source_plant_id]` in den **Drill-Through-Filter** ziehen
3. „Berichtsseiten übergreifend" → **Ein**
4. Die Zurück-Schaltfläche wird automatisch eingefügt (oben links)

### 9.2 Layout-Konzept

```
┌────────────────────────────────────────────────────────────────┐
│ [← Zurück]   Werk-Detail: {source_plant_id}                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─ KPI-Leiste ──────────────────────────────────────────────┐ │
│  │ CHPU Ist │ CHPU Soll │ Ratio Ist │ Ratio Soll │ Ampel    │ │
│  │  10.8    │   11.2    │   3.5%    │   5.0%     │   🟢     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌── Kostenstellen-Tabelle (fakt_chpu_kst) ──────────────────┐ │
│  │ KST │ AnMin Ist │ AnMin Soll │ Δ │ CHPU Ist │ CHPU Soll │ │
│  │─────┼──────────┼───────────┼────┼─────────┼──────────────│ │
│  │ K01 │   2.500  │    2.300  │+200│  10.5   │   10.0      │ │
│  │ K02 │   1.800  │    1.900  │-100│  11.2   │   11.5      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌── C-HPU Entwicklung je KW ────────────────────────────────┐ │
│  │ Gestapelte Säulen D/DI/I + Soll-Linie (wie Seite 3)      │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### 9.3 Schritt-für-Schritt

#### Dynamischer Seitentitel

1. Einfügen → **Textfeld** (oder Card)
2. Measure erstellen (falls nicht vorhanden):
   ```
   Wird dynamisch durch Drill-Through-Kontext bestimmt
   ```
3. Alternativ: Textfeld „Werk-Detail" + Card mit `SELECTEDVALUE(fakt_chpu[source_plant_id])`

#### KPI-Leiste (5 Cards)

| Card | Measure (Tabelle `fakt_chpu`) | Format |
|---|---|---|
| C-HPU Ist YTD | `CHPU Ist YTD` | #,##0.0 |
| C-HPU Soll YTD | `CHPU Soll YTD` | #,##0.0 |
| Ratio Ist YTD | `Ratio Ist YTD` | 0.0% |
| Ratio Soll YTD | `Ratio Soll YTD` | 0.0% |
| Ampel | `Ampel Werk YTD` | Text (bedingte Hintergrundfarbe) |

Position: Nebeneinander, y=60, je 300×100

#### Kostenstellen-Tabelle

1. Einfügen → Visual → **Tabelle (tableEx)**
2. Datenquelle: `fakt_chpu_kst`
3. Spalten:

| # | Feld/Measure | Header |
|---|---|---|
| 1 | `fakt_chpu_kst[kst_bezeichnung_kurz]` | Kostenstelle |
| 2 | `AnMin Ist KST` | AnMin Ist |
| 3 | `AnMin Soll KST` | AnMin Soll |
| 4 | `Delta AnMin KST` | Δ AnMin |
| 5 | `CHPU Ist KST` | C-HPU Ist |
| 6 | `CHPU Soll KST` | C-HPU Soll |
| 7 | `Delta CHPU KST` | Δ C-HPU |
| 8 | `Ratio Ist KST` | Ratio Ist |
| 9 | `Ratio Soll KST` | Ratio Soll |
| 10 | `Ampel KST YTD` | Ampel |

4. Position: x=40, y=180, Breite=1840, Höhe=400
5. Bedingte Formatierung auf Delta-Spalten (Datenbalken) und Ampel-Spalte (Hintergrundfarbe)

#### Drill-Through-Aktion zur Kostenstellen-Detailseite

In der Kostenstellen-Tabelle kann per Rechtsklick auf eine Zeile ein Drill-Through zur Seite 7 erfolgen, sofern `kst_bezeichnung_kurz` dort als Drill-Through-Feld konfiguriert ist.

#### C-HPU Chart (unterer Bereich)

Wie auf Seite 3, aber mit Daten aus `fakt_chpu` (das Werk ist bereits durch Drill-Through gefiltert):
1. **Linien- und gestapeltes Säulendiagramm**
2. X-Achse: `fakt_chpu[jahr_kw]`
3. Säulen: `CHPU Ist D`, `CHPU Ist DI`, `CHPU Ist I`
4. Linie: `CHPU Soll`
5. Position: x=40, y=600, Breite=1840, Höhe=420

### 9.4 Verwendete Measures

```
-- Aus fakt_chpu (über Drill-Through-Kontext gefiltert):
CHPU Ist YTD, CHPU Soll YTD, Ratio Ist YTD, Ratio Soll YTD, Ampel Werk YTD
CHPU Ist D, CHPU Ist DI, CHPU Ist I, CHPU Soll

-- Aus fakt_chpu_kst:
AnMin Ist KST, AnMin Soll KST, Delta AnMin KST
CHPU Ist KST, CHPU Soll KST, Delta CHPU KST
Ratio Ist KST, Ratio Soll KST, Ampel KST YTD
```

---

## 10. Seite 7 – Kostenstellen-Detail (Drill-Through)

### 10.1 Drill-Through konfigurieren

1. Seite „Kostenstellen-Detail" auswählen
2. **Drill-Through-Filter** hinzufügen:
   - `fakt_chpu_kst[source_plant_id]`
   - `fakt_chpu_kst[kst_bezeichnung_kurz]`
3. „Berichtsseiten übergreifend" → **Ein**

### 10.2 Layout-Konzept

```
┌────────────────────────────────────────────────────────────────┐
│ [← Zurück]   Kostenstelle: {kst_bezeichnung_kurz} | {Werk}    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─ KPI-Leiste ──────────────────────────────────────────────┐ │
│  │ CHPU Ist│CHPU Soll│Ratio Ist│Ratio Soll│Ampel│ZE Ist     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌── KW-Detail-Tabelle ─────────────────────────────────────┐ │
│  │ KW │AnMin Ist│AnMin Soll│Δ AnMin│CHPU Ist│CHPU Soll│Ratio│ │
│  │────┼─────────┼──────────┼───────┼────────┼─────────┼─────│ │
│  │ 01 │  450    │   420    │  +30  │  10.5  │  10.0   │2.1% │ │
│  │ 02 │  430    │   420    │  +10  │  10.2  │  10.0   │1.5% │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌── Kategorie-Aufschlüsselung ─────────────────────────────┐ │
│  │ Kategorie │ AnMin Ist │ AnMin Soll │ Δ │ Ratio Ist       │ │
│  │ Direkt    │   xxx     │   xxx      │+xx│  x.x%           │ │
│  │ Dir.Ind.  │   xxx     │   xxx      │-xx│  x.x%           │ │
│  │ Indirekt  │   xxx     │   xxx      │+xx│  x.x%           │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### 10.3 Schritt-für-Schritt

#### KPI-Leiste (6 Cards)

| Card | Measure | Format |
|---|---|---|
| C-HPU Ist | `CHPU Ist KST` | #,##0.0 |
| C-HPU Soll | `CHPU Soll KST` | #,##0.0 |
| Ratio Ist | `Ratio Ist KST` | 0.0% |
| Ratio Soll | `Ratio Soll KST` | 0.0% |
| Ampel | `Ampel KST YTD` | bedingt |
| ZE Ist | `ZE Ist KST` | #,##0 |

#### KW-Detail-Tabelle

1. Einfügen → Visual → **Tabelle**
2. Datenquelle: `fakt_chpu_kst`
3. Spalten:

| # | Feld/Measure | Header |
|---|---|---|
| 1 | `fakt_chpu_kst[jahr_kw]` | KW |
| 2 | `AnMin Ist KST` | AnMin Ist |
| 3 | `AnMin Soll KST` | AnMin Soll |
| 4 | `Delta AnMin KST` | Δ AnMin |
| 5 | `CHPU Ist KST` | C-HPU Ist |
| 6 | `CHPU Soll KST` | C-HPU Soll |
| 7 | `Delta CHPU KST` | Δ C-HPU |
| 8 | `Ratio Ist KST` | Ratio Ist |

4. Sortierung: `jahr_kw` absteigend (neueste KW oben)
5. Bedingte Formatierung auf Deltas

#### Kategorie-Aufschlüsselung

1. Einfügen → Visual → **Tabelle** (manuell strukturiert)
2. Zeige 3 Zeilen (D, DI, I) – da keine Kategorie-Spalte existiert, verwende stattdessen **3 Card-Gruppen**:

**Direkt:**
- `AnMin Ist D KST` | `AnMin Soll D KST` | `Delta AnMin D KST` | `Ratio Ist D KST`

**Direkt Indirekt:**
- `AnMin Ist DI KST` | `AnMin Soll DI KST` | `Delta AnMin DI KST` | `Ratio Ist DI KST`

**Indirekt:**
- `AnMin Ist I KST` | `AnMin Soll I KST` | `Delta AnMin I KST` | `Ratio Ist I KST`

Gestalte dies als 3×4 Grid von kleinen Cards oder als manuell beschriftete Tabelle.

### 10.4 Verwendete Measures

```
CHPU Ist KST, CHPU Soll KST, Ratio Ist KST, Ratio Soll KST
Ampel KST YTD, ZE Ist KST
AnMin Ist KST, AnMin Soll KST, Delta AnMin KST, Delta CHPU KST
AnMin Ist D KST, AnMin Soll D KST, Delta AnMin D KST, Ratio Ist D KST
AnMin Ist DI KST, AnMin Soll DI KST, Delta AnMin DI KST, Ratio Ist DI KST
AnMin Ist I KST, AnMin Soll I KST, Delta AnMin I KST, Ratio Ist I KST
CHPU Ist D KST, CHPU Ist DI KST, CHPU Ist I KST
```

---

## 11. Bedingte Formatierung & Ampellogik

### 11.1 Ampellogik (für alle Ampel-Visuals)

| Bedingung | Farbe | Hex |
|---|---|---|
| Ratio Ist ≥ Ratio Soll | Grün | `#00A650` |
| Ratio Ist ≥ 0 | Gelb | `#FFB800` |
| Ratio Ist < 0 | Rot | `#E63946` |

### 11.2 Anwendung in Power BI

**Hintergrundfarbe nach Regeln:**
1. Visual/Spalte auswählen → Format → Bedingte Formatierung
2. „Basierend auf" → **Regeln**
3. Regel 1: Wenn `Ampel Werk YTD` **ist** „grün" → Hintergrund #00A650, Schrift Weiß
4. Regel 2: Wenn `Ampel Werk YTD` **ist** „gelb" → Hintergrund #FFB800, Schrift Schwarz
5. Regel 3: Wenn `Ampel Werk YTD` **ist** „rot" → Hintergrund #E63946, Schrift Weiß

**Für numerische Werte (Ratio direkt):**
1. Wenn Wert ≥ `Ratio Soll` (Measure als Referenz) → Grün
2. Wenn Wert ≥ 0 → Gelb
3. Sonst → Rot

### 11.3 Datenbalken für Deltas

**Konfiguration:**
1. Spalte → Bedingte Formatierung → **Datenbalken**
2. **Achtung C-HPU-spezifisch:** Weniger AnMin = besser, daher:
   - Negative Balken → **Grün** (unter Soll = gut)
   - Positive Balken → **Rot** (über Soll = schlecht)

### 11.4 Trend-Icon Formatierung

Das Measure `Trend CHPU` gibt Unicode-Zeichen zurück:
- ▲ (U+9650) = Anstieg → Schriftfarbe **Rot** (C-HPU steigt = schlecht)
- ▼ (U+9660) = Rückgang → Schriftfarbe **Grün** (C-HPU sinkt = gut)
- ► (U+9654) = Stabil → Schriftfarbe **Grau**

Bedingte Formatierung auf Schriftfarbe:
1. Formatieren nach → **Regeln**
2. Basierend auf Measure `CHPU Ist` - `CHPU Ist Vorwoche`:
   - Wenn < -0.05 → Grün
   - Wenn > 0.05 → Rot
   - Sonst → Grau

---

## 12. Slicer & Filter

### 12.1 Globale Slicer (auf jeder Seite außer Drill-Through)

#### Slicer 1: Kalenderwoche

1. Einfügen → Visual → **Datenschnitt**
2. Feld: `fakt_chpu[jahr_kw]`
3. Typ: **Dropdown** oder **Zwischen** (Bereich)
4. Position: Oben rechts (x=1600, y=10)
5. Standardwert: Letzte verfügbare KW

#### Slicer 2: Werk (nur auf Seite 3, 4, 5)

1. Einfügen → Visual → **Datenschnitt**
2. Feld: `fakt_chpu[source_plant_id]`
3. Typ: **Dropdown** mit Mehrfachauswahl
4. Position: Neben dem KW-Slicer

### 12.2 Slicer synchronisieren

1. **Ansicht** → **Slicer synchronisieren**
2. Den KW-Slicer auf Seiten 2–5 synchronisieren
3. Drill-Through-Seiten (6, 7) **NICHT** synchronisieren – dort wird über den Drill-Through gefiltert

### 12.3 Seitenlevel-Filter

Auf den Drill-Through-Seiten werden die Filter automatisch durch den Drill-Through-Kontext gesetzt. Keine manuellen Seitenfilter nötig.

---

## 13. Theme & Design-Richtlinien

### 13.1 Farbpalette (CHPU IBCS Theme)

| Verwendung | Farbe | Hex |
|---|---|---|
| Primär / Direkt VBZ | Dunkelblau | `#1B3A5C` |
| Sekundär / Direkt Indirekt | Mittelblau | `#4A8DB7` |
| Tertiär / Indirekt | Hellblau | `#A8D0E6` |
| Text / Soll-Linie | Dunkelgrau | `#333333` |
| Hintergrund-Elemente | Hellgrau | `#B0B0B0` |
| Mittelgrau | Grau | `#808080` |
| Ampel Grün | Grün | `#00A650` |
| Ampel Gelb | Gelb | `#FFB800` |
| Ampel Rot | Rot | `#E63946` |

### 13.2 Typografie

- **Seitentitel**: DIN, 20pt, Fett
- **Visual-Titel**: DIN, 14pt, Fett
- **Daten**: DIN, 10–12pt, Regular
- **KPI-Callout**: DIN, 24–32pt, Fett
- **Fußzeile**: DIN, 10pt, Grau

### 13.3 Layout-Regeln

- **Ränder**: 40px links/rechts, 10px oben
- **Abstand zwischen Visuals**: 16–20px
- **Rahmen**: 1px, `#B0B0B0` (oder über Theme gesteuert)
- **Hintergrund Cards**: Weiß mit leichtem Schatten
- **Sidebar** (Summary): `#4A8DB7` (ThemeDataColor 1) oder `#1B3A5C` (ThemeDataColor 0)

### 13.4 IBCS-Konformität

- Ist-Werte: **Gefüllte Balken** (solid)
- Soll-Werte: **Umriss / gestrichelt** (outline)
- Abweichungen: **Integrierte Datenbalken** in Tabellen
- Keine 3D-Effekte, keine Verläufe, keine unnötigen Dekorationen

---

## 14. Measure-Referenz pro Seite

### Komplett-Übersicht

| Seite | Measures aus `fakt_chpu` | Measures aus `fakt_chpu_kst` |
|---|---|---|
| **1 – Summary** | Anzahl Werke, Anzahl Werke Grün YTD, Ratio Ist YTD, Ratio Ist VSI, Ampel Gesamt YTD, Management Summary Kontext, Management Summary Entscheidungsbedarf | – |
| **2 – Cockpit** | Trend CHPU, CHPU Soll, Ratio Ist, Ratio Ist YTD, Ratio Ist VSI, CHPU Ist, CHPU Ist YTD, CHPU Ist VSI, Ampel Werk YTD | – |
| **3 – Entwicklung** | CHPU Ist D, CHPU Ist DI, CHPU Ist I, CHPU Soll, Ratio Ist YTD, Ratio Ist VSI, CHPU Ist YTD, CHPU Soll YTD, ZE Ist YTD, ZE Soll YTD, Delta ZE YTD | – |
| **4 – Abweichung Vollk.** | AnMin Ist/Soll, Delta AnMin, AnMin Ist/Soll D/DI/I, Delta AnMin D/DI/I, Ratio Ist, Ratio Soll | – |
| **5 – Abweichung Direkt** | AnMin Ist/Soll D, Delta AnMin D, Ratio Ist/Soll D, CHPU Ist/Soll D, Ratio Ist D YTD, Delta AnMin D YTD | – |
| **6 – Werk-Detail** | CHPU Ist/Soll YTD, Ratio Ist/Soll YTD, Ampel Werk YTD, CHPU Ist D/DI/I, CHPU Soll | AnMin Ist/Soll KST, Delta AnMin/CHPU KST, Ratio Ist/Soll KST, Ampel KST YTD |
| **7 – KST-Detail** | – | Alle KST-Measures inkl. D/DI/I Splits, YTD, Ampel |

---

## 15. Abschluss-Checkliste

### Funktionale Prüfung

- [ ] **Alle 7 Seiten** vorhanden und korrekt benannt
- [ ] **Berichtsgröße** 1920×1080
- [ ] **Slicer** auf Seiten 2–5 funktionieren und sind synchronisiert
- [ ] **Drill-Through** von Cockpit → Werk-Detail funktioniert
- [ ] **Drill-Through** von Werk-Detail → KST-Detail funktioniert
- [ ] **Zurück-Buttons** auf Drill-Through-Seiten vorhanden
- [ ] **Ampellogik** korrekt: Grün/Gelb/Rot stimmen mit Ratio-Werten überein
- [ ] **Bedingte Formatierung** auf allen Delta-Spalten aktiv
- [ ] **Trend-Pfeile** im Cockpit werden korrekt angezeigt

### Rechnerische Prüfung

- [ ] **CHPU = DIVIDE(AnMin, ZE)** – niemals SUM(chpu_ist)!
- [ ] **Ratio** wird über AnMin-Summen berechnet, nicht über AVERAGE
- [ ] **YTD** aggregiert über Summen, nicht über Mittelwerte
- [ ] **VSI** zeigt aktuell YTD-Werte (temporäre Logik)
- [ ] **KW-Extraktion** verwendet `MOD(jahr_kw, 100)`, nicht LEFT/MID
- [ ] **Jahr-Extraktion** verwendet `INT(jahr_kw / 100)`, nicht FORMAT
- [ ] **Delta-Farben** korrekt invertiert (negativ = gut bei C-HPU/AnMin)
- [ ] Stichprobe: CHPU Ist YTD manuell nachrechnen mit Rohdaten

### Design-Prüfung

- [ ] **Konsistente Farben** auf allen Seiten (IBCS Theme)
- [ ] **Einheitliche Schriftarten** und -größen
- [ ] **Alle Measures** haben passende Formatstrings (%, #,##0, etc.)
- [ ] **Titel** auf jeder Seite vorhanden
- [ ] **KSU-Klassifizierung** auf jeder Seite sichtbar
- [ ] **Version/Stand** auf Seite 1 aktuell

### Deployment-Prüfung

- [ ] Git-Status sauber: `git status`
- [ ] Aussagekräftiger Commit: `git commit -m "Bericht v1.0: alle 7 Seiten, Drill-Through, Ampellogik"`
- [ ] `.gitignore` enthält `**/.pbi/localSettings.json`
- [ ] Keine PBIX-Datei im Repository
- [ ] Semantic Model refresht ohne Fehler

---

## 16. Bekannte Stolperfallen

### Stolperfalle 1: CHPU / Ratio als Spalte aggregieren

❌ **Falsch**: `SUM(fakt_chpu[chpu_ist])` oder `AVERAGE(fakt_chpu[ratio_ist])`
✅ **Richtig**: `DIVIDE(SUM(anmin_ist), SUM(ze_ist))`

Die vorberechneten Spalten `chpu_ist`, `ratio_ist` in der Datenquelle dürfen **nicht** direkt summiert oder gemittelt werden. Sie dienen nur als Referenz auf Einzelzeilenebene.

### Stolperfalle 2: Delta-Farben bei C-HPU sind invertiert

Bei Umsatz-KPIs: Positives Delta = gut (grün).  
**Bei C-HPU: Negatives Delta = gut (grün)!** Weniger Minuten pro ZE ist besser.

Datenbalken und bedingte Formatierung müssen diese Umkehrlogik abbilden.

### Stolperfalle 3: YTD über einfachen Durchschnitt berechnen

❌ Die C-HPU YTD ist **nicht** der Durchschnitt der KW-C-HPUs.
✅ YTD = `SUM(AnMin aller KWs) / SUM(ZE aller KWs)`

Gleiches gilt für Ratio YTD – gewichtete Summenberechnung, kein Mittelwert.

### Stolperfalle 4: Drill-Through-Filter greifen nicht

Wenn der Drill-Through nicht funktioniert:
1. Prüfen, ob das Drill-Through-Feld (`source_plant_id`) korrekt in den Drill-Through-Bereich gezogen wurde
2. Prüfen, ob die Quellseite denselben Feldnamen verwendet
3. „Berichtsübergreifend" muss aktiviert sein
4. Das Feld muss **exakt denselben Datentyp** haben (String ↔ String)

### Stolperfalle 5: Slicer-Synchronisierung auf Drill-Through-Seiten

Slicer auf Drill-Through-Seiten sollten **nicht** mit den normalen Seiten synchronisiert sein, da sonst der Drill-Through-Kontext überschrieben wird.

### Stolperfalle 6: VSI-Logik ist temporär

Die aktuelle VSI-Implementierung ist `VSI = YTD`. Sobald die finale VSI-Logik abgestimmt ist, müssen alle `*VSI`-Measures umgestellt werden auf:
```
(Σ AnMin Ist KW1..m + Σ AnMin Soll KW(m+1)..n) / (Σ ZE Ist KW1..m + Σ ZE Soll KW(m+1)..n)
```

### Stolperfalle 7: Tabellen fakt_chpu und fakt_chpu_kst haben keine Beziehung

Die beiden Tabellen sind **nicht** über eine Beziehung verknüpft. Auf Drill-Through-Seiten müssen Visuals aus `fakt_chpu` und `fakt_chpu_kst` getrennt konfiguriert werden. Der Drill-Through-Filter wirkt nur auf die Tabelle, deren Feld im Drill-Through-Bereich liegt.

**Lösung:** Verwende auf Seite 6 das Feld `fakt_chpu_kst[source_plant_id]` (nicht aus `fakt_chpu`) als Drill-Through-Filter, damit es auf die KST-Tabelle wirkt. Für Werk-Level-KPIs aus `fakt_chpu` nutze zusätzlich einen visuellen Filter oder ein CALCULATE mit dem Drill-Through-Wert.

---

## Empfohlene Reihenfolge der Umsetzung

| Schritt | Aufgabe | Abhängigkeiten |
|---|---|---|
| 1 | Berichtsgröße auf 1920×1080 ändern | – |
| 2 | Seiten anlegen und benennen | – |
| 3 | Debug-Seiten ausblenden | – |
| 4 | Seite 1 (Summary) fertigstellen | KPI-Cards ergänzen |
| 5 | Seite 2 (Cockpit) bauen | Matrix + Ampeln |
| 6 | Seite 3 (Entwicklung) bauen | Chart + Cards |
| 7 | Seite 4 (Abweichung Vollk.) bauen | Matrix + Balken |
| 8 | Seite 5 (Abweichung Direkt) bauen | Seite 4 duplizieren + anpassen |
| 9 | Seite 6 (Drill-Through Werk) bauen | Drill-Through konfigurieren |
| 10 | Seite 7 (Drill-Through KST) bauen | Drill-Through konfigurieren |
| 11 | Slicer einrichten + synchronisieren | Seiten 2–5 fertig |
| 12 | Bedingte Formatierung auf allen Seiten | Alle Visuals fertig |
| 13 | Abschluss-Checkliste durchgehen | Alles fertig |
| 14 | Git Commit + Push | Finale Prüfung |

---

*Erstellt am 10.06.2026 – basierend auf C-HPU_PowerBI_Report_Requirements.md, C-HPU_Wissensdokumentation.md und dem aktuellen Projektstand.*
