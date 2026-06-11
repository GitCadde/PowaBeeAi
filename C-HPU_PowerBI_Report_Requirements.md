# C-HPU Power BI Bericht – Anforderungen & Zielbild

## Ziel des Projekts

Ziel ist die Entwicklung eines interaktiven Power BI Management- und Analyseberichts für den C-HPU Regelprozess im Volkswagen Group Components Umfeld.

Der Bericht soll:

- den aktuellen Status der Werke visualisieren
- Zielerreichungen transparent machen
- Abweichungen analysieren
- Drill-Through bis auf Kostenstellenebene ermöglichen
- Management Summary + operative Analyse kombinieren
- YTD- und VSI-Betrachtungen ermöglichen
- das bestehende Reporting-Layout möglichst 1:1 digital abbilden
- langfristig automatisiert aktualisiert werden

---

# Fachlicher Hintergrund

## Was ist C-HPU?

C-HPU = Cost per Handling Unit bzw. Minuten pro Zieleinheit.

Die Kennzahl basiert auf:

```text
CHPU = Anwesenheitsminuten / Zieleinheiten
```

Niedrigerer Wert = besser.

---

# Fachliche Logik

## Kategorien

Der Bericht unterscheidet drei Mitarbeiter-/Kostenkategorien:

| Kategorie | Suffix | Beschreibung |
|---|---|---|
| Direkte | `_d` | Direkt produktive Mitarbeitende |
| Direkt Indirekte / Direkt Fix | `_di` | Direkte Fixkosten / indirekte direkte Bereiche |
| Indirekte | `_i` | Indirekte Mitarbeitende |

---

# Datenmodell

## Tabellen

### `fakt_chpu`
Werksebene.

### `fakt_chpu_kst`
Kostenstellenebene.

Granularere Detaildaten für Drill-Through.

---

# Wichtige Rohdatenfelder

| Feld | Beschreibung |
|---|---|
| `anmin_ist` | Anwesenheitsminuten Ist |
| `anmin_soll` | Anwesenheitsminuten Soll |
| `anmin_soll_ohne_ratio` | Soll ohne Ratio-Effekt |
| `ze_ist` | Zieleinheiten Ist |
| `ze_soll` | Zieleinheiten Soll |
| `jahr_kw` | Kalenderwoche im Format YYYYWW (Integer) |
| `source_plant_id` | Werk |
| `kst_bezeichnung_kurz` | Kostenstelle |

---

# KPI-Logik

## CHPU

```text
CHPU = SUM(AnMin) / SUM(ZE)
```

## Ratio

```text
Ratio = (CHPU Ist - CHPU Soll) / CHPU Soll
```

## YTD

YTD = aktuelles Jahr bis aktuelle Kalenderwoche.

## VSI

Temporär:

```text
VSI = YTD
```

---

# Seitenstruktur

## Seite 1 – Management Summary

### Inhalte

- KPI-Blöcke
- Anzahl Werke grün
- YTD Zielerreichung
- VSI Zielerreichung
- Kontext/Hintergrund
- Entscheidungsbedarfe

---

## Seite 2 – Cockpit Vollk. Kreis

### Inhalte

Je Werk:

- Werkname
- Trendpfeil
- CHPU Soll
- Ratio KW
- Ratio YTD
- Ratio VSI
- CHPU KW
- CHPU YTD
- CHPU VSI
- Ampelstatus

---

## Seite 3 – C-HPU Entwicklung

### Inhalte

- Gestapelte Säulen
- CHPU Soll Linie
- ZE Ist/Soll
- Ratio YTD
- Ratio VSI

---

## Seite 4 – Abweichungsanalyse Vollk. Kreis

### Inhalte

- MA Ist
- MA Soll
- Delta MA
- Ratio Ist
- Ratio Soll
- Datenbalken
- Bedingte Formatierung

---

## Seite 5 – Abweichungsanalyse DE Direkt

### Fokus

Nur direkte Bereiche.

---

## Seite 6 – Werk-Detail (Drill-Through)

### Drill-Through Feld

```text
source_plant_id
```

---

## Seite 7 – Kostenstellen-Detail (Drill-Through)

### Drill-Through Felder

```text
source_plant_id
kst_bezeichnung_kurz
```

---

# Technische Anforderungen

## Berichtsgröße

```text
1920 x 1080
```

## Pflichtfeatures

- Drill-Through
- Bedingte Formatierung
- KPI-Texte
- Ampellogik
- YTD-Logik
- VSI-Logik
- Werk-Cockpit
- Kostenstellenanalyse

---

# DAX-Konventionen

## Niemals

```dax
SUM(chpu_ist)
SUM(chpu_soll)
SUM(ratio_ist)
```

## Immer

```dax
DIVIDE( SUM(anmin_...), SUM(ze_...) )
```

## Jahr/KW Regeln

### Niemals

```dax
LEFT()
MID()
FORMAT()
```

### Immer

```dax
INT(jahr_kw / 100)
MOD(jahr_kw,100)
```

---

# Offene Punkte

- finale VSI-Logik
- Feinlayout
- KPI-Abstimmung
- produktive Werkdaten
- automatische Aktualisierung
