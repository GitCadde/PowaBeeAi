# C-HPU IBCS Layout Tokens (1920×1080)

Zentrale Konstanten für den Power-BI-Bericht. Werden von `apply_ibcs_layout.py` angewendet.

## Canvas

| Token | Wert |
|-------|------|
| Breite | 1920 px |
| Höhe | 1080 px |
| Außenrand | 24 px |
| Gutter | 24 px |

## Zonen

| Zone | Y-Bereich | Beschreibung |
|------|-----------|--------------|
| Header | 0–96 | Logo, Titel, Navigation |
| Akzentlinie | 100 | 2 px, `#5B7D96` |
| Filter-Band | 108–168 | Slicer rechtsbündig |
| Content | 184–1012 | 12-Spalten-Raster |
| Footer | 1024–1068 | Vertraulich / Version |

## 12-Spalten-Raster

- Spaltenbreite: **134 px**
- Formel Breite: `n × 134 + (n−1) × 24`
- Formel X: `24 + col × 158`

## Chrome-Elemente

| Element | Position | Größe |
|---------|----------|-------|
| Logo | (24, 16) | 64×64 |
| Titel | (104, 8) | 520×80 |
| Nav-Buttons | y=24, x=656…1696 | 200×48, Gutter 8 |
| Slicer | y=112, rechtsbündig | 220×56 |
| Datenschutz | (400, 1024) | 288×44 |
| Footer links | (24, 1032) | 360×36 |
| Footer rechts | (1496, 1032) | 400×36 |

## Typografie

| Rolle | Größe | Gewicht |
|-------|-------|---------|
| Berichtstitel | 20 pt | bold |
| Seitenuntertitel | 13 pt | normal |
| Visualtitel | 12 pt | bold |
| KPI-Wert | 30 pt | normal |
| KPI-Label | 11 pt | normal |
| Tabellen-Header | 11 pt | bold |
| Tabellen-Wert | 10 pt | normal |
| Achsen | 10 pt | normal |
| Datenlabels | 9 pt | normal |
| Footer | 9 pt | normal |

## IBCS-Farben

| Semantik | Hex |
|----------|-----|
| Ist / AC | `#404040`, `#5B7D96` |
| Soll / PL | `#BCD5E3` |
| Gut | `#44C088` |
| Schlecht | `#ED7373` |
| Neutral | `#C8C8C8` |
| Akzent | `#5B7D96` |
| Hintergrund | `#FFFFFF` |
