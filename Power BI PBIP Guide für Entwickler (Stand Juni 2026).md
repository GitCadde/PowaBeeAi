# Power BI PBIP Guide für Entwickler (Stand Juni 2026)

## Überblick

Power BI Project Files (PBIP) bilden seit 2024/2025 den zentralen Baustein für moderne, entwicklerfreundliche Power-BI-Workflows und werden in 2026 in Richtung Standard weiterentwickelt. PBIP speichert Berichte und semantische Modelle nicht mehr als monolithische, binäre PBIX-Datei, sondern als textbasierte Dateien und Ordnerstruktur und ermöglicht damit Git-Workflows, Code-Reviews und automatisierte Pipelines. Parallel wird das neue PBIR-Format für Berichte eingeführt, das PBIR-Legacy bis spätestens GA in 2026 ablösen soll.[^1][^2][^3][^4][^5][^6]

Dieser Guide richtet sich an Entwickler, die Power BI wie ein Softwareprojekt behandeln wollen (Git, Branching, CI/CD) und fokussiert auf das Arbeiten mit PBIP-Projekten im Dateisystem, insbesondere auf sinnvolles Bearbeiten, Versionieren und Automatisieren der Inhalte.

## Zielgruppe und Voraussetzungen

Der Guide setzt voraus:

- Erfahrung mit Power BI Desktop (Modellierung, DAX, M, Berichte).
- Grundkenntnisse in Git (Commit, Branch, Merge, Pull Request).
- Bereitschaft, Power BI-Projekte ähnlich wie Code zu behandeln (Repository-Struktur, Reviews, Pipelines).

Für Full-Stack-Developer oder Data Engineers mit VS Code, GitHub/GitLab/Azure DevOps ist der Einstieg besonders naheliegend.[^7][^8]

## PBIP – Konzept und Rolle im Power-BI-Ökosystem

PBIP ist kein anderer Berichtstyp, sondern eine alternative Repräsentation eines Power-BI-Projekts: Die gleiche Kombination aus Bericht und semantischem Modell wird in eine klare Ordnerstruktur und textbasierte Artefakte (JSON, TMDL, M, usw.) zerlegt. Diese Repräsentation ist explizit dafür entworfen, in Versionskontrolle, CI/CD und externe Tools integriert zu werden.[^2][^3][^4][^5]

Wichtige Punkte:

- PBIP ≙ Projektansicht eines Berichts + Semantic Model im Dateisystem.[^4][^2]
- PBIX bleibt vorerst nutzbar, wird aber intern zunehmend ebenfalls die neuen PBIR-Strukturen verwenden.[^1]
- PBIR beschreibt den Berichtsteil (Report) als textbasiertes Format; PBIP umschließt Bericht und Modell.[^9][^1]

## Aktueller Stand (Juni 2026)

- PBIP ist in Power BI Desktop verfügbar und auf dem Weg zur GA, mit offizieller GA-Planung im Verlauf des Jahres 2026.[^3][^1]
- PBIR ist seit Anfang 2026 das Standardreportformat im Power-BI-Service; Desktop-Umstellung läuft bis Mitte 2026, GA ist für Q3 2026 angekündigt.[^6][^1]
- PBIR-Legacy wird mit GA von PBIR obsolet, alle Reports werden beim Speichern migriert.[^1]
- Git-Integration via Microsoft Fabric Workspaces steht für GitHub und Azure DevOps zur Verfügung, benötigt aber entsprechende Lizenzen.[^10]

## Grundstruktur eines PBIP-Projekts

Ein typisches PBIP-Projekt besteht aus:

- `<Projektname>.pbip` (Entry-Point-Datei für Power BI Desktop).
- `<Projektname>.Report/` (Berichtsartefakte).
- `<Projektname>.SemanticModel/` (semantisches Modell in TMDL/M-Form).

Die `.pbip`-Datei enthält eine JSON-Struktur, die auf die Report- und ggf. weitere Artefaktordner verweist. Die Ordnerstruktur und Dateitypen sind in Microsoft Learn detailliert beschrieben.[^11][^2][^9][^4]

### PBIP-Datei (Top-Level)

Beispiel (vereinfachte Struktur aus der Praxis):[^11]

```json
{
  "version": "1.0",
  "artifacts": [
    {
      "report": {
        "path": "MyProject.Report"
      }
    }
  ],
  "settings": {
    "enableAutoRecovery": true
  }
}
```

Die `artifacts`-Liste kann bei komplexeren Projekten mehrere Reports oder andere Artefakte enthalten. In der Praxis verweist ein PBIP aber üblicherweise auf genau einen Report und darüber indirekt auf ein Semantic Model.[^11]

### Report-Ordner

Der Report-Ordner `<Projektname>.Report` enthält laut Microsoft-Dokumentation verschiedene Dateien und Unterordner:[^9]

- `.pbi/localSettings.json` – Benutzer- und maschinenspezifische Einstellungen, **nicht** für Git geeignet.[^9]
- `definition.pbir` – zentrale Definitionsdatei für den Report im neuen PBIR-Format (Pfad, Metadaten, Zielmodell).[^9]
- `report.json` – für PBIR-Legacy; bei neuen PBIR-Projekten wird stattdessen der `definition`-Ordner verwendet.[^9]
- `definition/` – Ordner mit der eigentlichen Reportdefinition im PBIR-Format (Seiten, Visuals, Layout, Filter etc.).[^1][^9]
- `CustomVisuals/`, `StaticResources/`, `RegisteredResources/`, `semanticModelDiagramLayout.json`, `mobileState.json` – optional, abhängig von verwendeten Features.[^9]

Mit dem neuen PBIR-Format wandert die Reportdefinition aus der monolithischen `report.json` in eine modulare Struktur im `definition`-Ordner.[^1][^9]

### Semantic-Model-Ordner

Der Ordner `<Projektname>.SemanticModel` enthält das Modell in TMDL (Tabular Model Definition Language), ergänzt um M-Skripte und weitere Metadaten:[^2]

- TMDL-Dateien für Tabellen, Beziehungen, Measures, Rollen usw.[^2]
- Query-Definitionen (Power Query M) für Datenquellen und Transformationsschritte.[^2]
- Model-Metadaten (z. B. Annotations, Formatierung, Sortierreihenfolgen).

TMDL wurde 2024 als textbasierte Sprache für Tabular-Modelle eingeführt und ist deutlich git-freundlicher als TMSL.[^2]

## PBIP aktivieren und erstellen

### PBIP in Power BI Desktop aktivieren

In älteren Desktop-Versionen musste die PBIP-Funktion in den Preview-Features aktiviert werden; in neueren Versionen ist sie standardmäßig vorhanden oder wird über die Projekt-Funktion aktiviert.[^10][^4]

Vorgehen (je nach Version leicht abweichend):

1. Power BI Desktop öffnen.
2. `Datei → Optionen und Einstellungen → Optionen`.
3. Unter `Preview Features` die Option **Power BI Project (.pbip) save option** aktivieren (falls vorhanden).[^10]
4. Desktop neu starten.

In aktuellen Versionen steht beim Speichern direkt eine „Projekt speichern“-Option zur Verfügung.[^4]

### Neues PBIP-Projekt anlegen

Vorgehensweise:

1. Neues oder bestehendes PBIX in Power BI Desktop öffnen.
2. `Datei → Speichern unter` und als **Power BI-Projekt (.pbip)** speichern.[^4][^10]
3. Zielordner auswählen – typischerweise ein Git-Repository.
4. Power BI legt `.pbip`, `.Report`- und `.SemanticModel`-Ordner im Zielordner an.[^4][^2]

Ab diesem Zeitpunkt ist das Projekt vollständig textbasiert versionierbar.

### PBIP aus bestehendem Repo erzeugen

Wenn der Workspace über Fabric Git mit einem Repository verknüpft ist, können Projekte direkt aus dem Service ins Repo synchronisiert werden.[^10][^11]

Spezialfall: Existiert nur der Ordner mit Report und SemanticModel im Repo, aber keine `.pbip`, lässt sich die PBIP-Datei manuell erstellen:[^11]

1. Projektordner im Git-Repo identifizieren (z. B. `LakehouseLocalDS.Report`/`LakehouseLocalDS.SemanticModel`).
2. Neue Datei `LakehouseLocalDS.pbip` mit passender `artifacts`-Definition anlegen (siehe PBIP-Beispiel).[^11]
3. Datei committen und pushen.
4. PBIP in Power BI Desktop öffnen – Desktop erkennt die Report- und Modellordner und lädt sie.

## Arbeiten mit PBIP im Alltag

### Typischer Entwickler-Workflow

Ein moderner Workflow mit PBIP und Git sieht häufig so aus:[^8][^7][^10]

1. Repo mit PBIP-Projekt klonen.
2. Feature-Branch erstellen.
3. PBIP in Power BI Desktop öffnen, Änderungen an Modell und Bericht vornehmen.
4. Speichern – Power BI aktualisiert die JSON/TMDL-Dateien im Projektordner.[^4][^2]
5. Änderungen in Git prüfen (`git status`, `git diff`, Review in GUI-Client).[^7]
6. Commits erstellen, Pull Request öffnen.
7. Nach Review mergen und optional CI/CD-Pipeline ausführen (Deployment in Test/Prod).

Durch die Textrepräsentation lassen sich Änderungen an Measures, Queries, Layouts oder Metadaten in Pull Requests sauber nachvollziehen.[^8][^7]

### Dateien, die man nicht manuell anfassen sollte

Obwohl PBIP textbasiert ist, eignet sich nicht jede Datei für manuelle Bearbeitung:

- `localSettings.json` – maschinenspezifisch, gehört in `.gitignore`.[^12][^9]
- Caches, temporäre Dateien und generierte Inhalte.
- Autogenerierte Layoutdateien (z. B. `semanticModelDiagramLayout.json`) – nur ändern, wenn bewusst gewünscht.[^9]

Manuelle Änderungen sind primär für:

- DAX- und M-Code (wo sinnvoll und sicher).
- TMDL-Strukturen (Tabellen, Beziehungen, Measures) mit Tool-Unterstützung.
- Metadaten wie Ordnerstrukturen, Anzeigeordnungen, Beschriftungen.

## Git-Setup und .gitignore für PBIP

### Grundlegende Struktur im Repository

Empfohlene Repo-Struktur für PBIP-basierte Projekte:[^13][^12]

- `/powerbi/`
  - `/sales-report/`
    - `SalesReport.pbip`
    - `SalesReport.Report/`
    - `SalesReport.SemanticModel/`
    - `README.md` (Projekt-Dokumentation)
    - ggf. `docs/` für technisch-fachliche Dokumentation

Alternative ist ein Repo pro Bericht oder „Mono-Repo“ für mehrere Projekte, je nach Organisationsgröße.[^13]

### .gitignore für Power-BI-Projekte

Ein korrektes `.gitignore` ist essenziell, um lokale Settings und temporäre Dateien aus der Versionskontrolle fernzuhalten. Wichtige Punkte:[^12]

- `*.pbix` optional ignorieren, wenn nur PBIP als Entwicklungsformat genutzt wird.
- `**/.pbi/localSettings.json` ignorieren.[^12][^9]
- Caches, temporäre Dateien und ggf. Export-Artefakte ignorieren.[^12]

In der Praxis erzeugt Power BI beim Speichern eines PBIP-Projekts häufig selbst eine `.gitignore`, die als Basis dienen kann.[^12][^11]

## Inhaltliche Bearbeitung von PBIP-Artefakten

### Arbeiten am Report (PBIR)

Mit PBIR wird der Bericht in eine modulare JSON-Struktur im `definition`-Ordner aufgeteilt. Für Entwickler sind hierbei relevant:[^1][^9]

- Seiten-Definitionen (Pages) mit Visual-Instanzen, Layout, Bookmarks.[^9]
- Filter- und Slicer-Konfigurationen.[^9]
- Referenzen auf das semantische Modell (Felder, Measures).

Manuelle Bearbeitung empfiehlt sich vor allem für:

- Globale Suchen/Ersetzen von Feldnamen, wenn beispielsweise Spalten umbenannt wurden.
- Batch-Anpassungen von Visual-Eigenschaften, z. B. Theme-IDs, Standardformatierungen.
- Refactoring von Wiederholungen (z. B. konsistente Titles, Tooltips).

Die offizielle Dokumentation liefert JSON-Schemas für die PBIR-Definitionen, die in VS Code für IntelliSense und Validierung eingesetzt werden können.[^4][^9]

### Arbeiten am semantischen Modell (TMDL)

Der größte Mehrwert von PBIP liegt in der Bearbeitung des Modells:[^2][^4]

- Tabellen und Spalten als TMDL-Dateien.
- Measures (DAX) als textbasierte Definitionen.
- Beziehungen, Rollen, Partitions.

Szenarien:

- Hinzufügen oder Bearbeiten von Measures direkt in TMDL.
- Review von DAX-Code im Pull Request (Code-Review für BI).[^7][^8]
- Strukturänderungen (z. B. neue Tabellen, Entfernen von Objekten) programmatisch oder per Texteditor.

TMDL ist Hierarchie-basiert; Änderungen sollten im Zweifel immer in Desktop verifiziert werden, bevor sie in Produktionspipelines laufen.[^2]

### M-Skripte (Power Query)

Power Query M-Skripte werden im Projekt ebenfalls textbasiert abgelegt (z. B. als Teil der TMDL-Beschreibung oder separater Artefakte). Entwickler können damit:[^4][^2]

- M-Skripte in VS Code bearbeiten.
- Wiederverwendbare Funktionen versionieren.
- Strukturierte Reviews für Datenaufbereitung implementieren.

Auch hier gilt: Nach Änderungen immer Test-Refresh in Power BI Desktop oder einer CI-Umgebung durchführen.

## Best Practices für Versionskontrolle und Zusammenarbeit

### Commits und Branches

Empfehlungen aus der Praxis:[^8][^7][^10]

- Feature-Branches für jede größere Änderung (z. B. `feature/add-profit-measures`).
- Kleine, thematisch saubere Commits (z. B. „Add margin measures“, „Refactor date dimension“).
- Commit-Nachrichten so formulieren, dass Nicht-Developer (z. B. BI-Lead) Änderungen nachvollziehen können.

Durch textbasierte PBIP-Dateien können Git-Diffs anzeigen, welche Measures, Tabellen oder Visuals geändert wurden.[^7][^8]

### Parallelentwicklung und Konfliktlösung

PBIP reduziert, aber eliminiert nicht alle Merge-Konflikte. Typische Konfliktquellen:

- Zwei Entwickler ändern dasselbe Measure.
- Änderungen an derselben Seite/Visual im PBIR-Report.

Empfehlungen:[^8][^7]

- Klare Ownership von Bereichen (z. B. Developer A verantwortet Modell, Developer B Bericht).
- Häufiges Pullen vom Main-Branch, um Divergenz zu reduzieren.
- Konflikte in TMDL/JSON mit einem geeigneten Merge-Tool lösen und anschließend im Desktop validieren.

### Code-Review für BI-Artefakte

PBIP macht Code-Review für BI-Projekte praktikabel:[^7][^8]

- DAX-Review (Naming, Performance, Lesbarkeit).
- M-Review (Effizienz, Fehlerbehandlung, Source Governance).
- Prüfung von Modelländerungen (Star-Schema, Normalisierung, KPI-Konventionen).

Pull Requests können Screenshots, fachliche Beschreibung und Testhinweise enthalten, ähnlich wie in Softwareprojekten.[^8]

## Integration mit GitHub, Azure DevOps und Fabric

### Lokale Git-Repositories

Einfachster Start:

- GitHub/GitLab/Azure DevOps Repo aufsetzen.
- Repo lokal klonen.
- PBIP direkt in dieses Repo speichern.[^10][^7]
- Änderungen wie gewohnt committen und pushen.

### Fabric Workspace Git-Integration

Für Power BI/Fabric Workspaces mit Premium-Kapazität steht eine direkte Git-Integration zur Verfügung:[^10]

- Workspace mit GitHub oder Azure DevOps verbinden.
- Branch und Ordner im Repo angeben.
- Workspace-Objekte (Reports, Modelle) werden in Projektstruktur ins Repo synchronisiert.
- Änderungen können über Pull Requests, Pipelines, etc. verwaltet werden.

Dies erleichtert das Zusammenspiel zwischen Service und Repo erheblich.[^10]

## CI/CD und automatisierte Deployments

### Grundidee

Mit PBIP als textbasiertem Format können CI/CD-Pipelines:

- Änderungen am Modell und Bericht validieren (z. B. Linting, DAX-Checks).
- Artefakte automatisiert in Test-Workspaces deployen.
- Prüfen, ob Refreshs erfolgreich sind.

Viele Best Practices stammen aus der Zusammenarbeit von PBIP mit Fabric, Azure DevOps und GitHub Actions.[^7][^10]

### Typische Pipeline-Schritte (High-Level)

1. Checkout des Repos.
2. Optional: statische Analysen (z. B. Power BI Helper, DAX-Stilchecker, benutzerdefinierte Skripte).
3. Deployment in einen Test-Workspace (mittels REST-APIs, Fabric-Deployment-Pipelines oder Tools von Drittanbietern).
4. Test-Refresh und Smoke-Tests.
5. Promotion nach Produktion nach Freigabe.

Die konkrete Umsetzung hängt stark vom Tooling ab; PBIP stellt primär die Grundlage in Form gut versionierbarer Artefakte bereit.[^7][^10]

## Umstieg von PBIX auf PBIP/PBIR

### Gründe für den Wechsel

- Bessere Nachvollziehbarkeit von Änderungen.[^5][^7]
- Saubere Versionshistorie je Measure, Tabelle und Visual.[^7]
- Ermöglicht echte Teamarbeit mit Branches und PRs.
- Vorbereitung auf die Zukunft, da PBIR/PBIP langfristig PBIX als Entwicklungsformat ergänzen bzw. ablösen.[^6][^1]

### Migrationspfad

1. Bestehende PBIX in Desktop öffnen.
2. Als PBIP-Projekt speichern.[^10][^4]
3. PBIP-Projekt in Git übernehmen.
4. PBIX optional weiter als Export-/Backup-Format nutzen, aber Entwicklung auf PBIP konzentrieren.

Mit der Umstellung von PBIX-internen Reportstrukturen auf PBIR durch Microsoft wird die Angleichung der Formate weiter vereinfacht.[^1]

## Typische Stolperfallen und wie man sie vermeidet

### Zu viele Binärdateien im Repo

Wenn zusätzlich zu PBIP große PBIX-Dateien eingecheckt werden, kann das Repository schnell wachsen und Diffs verlieren an Wert. Empfehlung:[^5][^12]

- PBIX nur dann versionieren, wenn es explizit benötigt wird (z. B. für Legacy-Tools).
- Schwerpunkt auf PBIP legen.

### Lokale Settings und Caches in Git

Werden `localSettings.json` und temporäre Dateien eingecheckt, produziert dies unnötige Konflikte und Noise. Eine sorgfältige `.gitignore` ist Pflicht.[^12][^9]

### Direkte Bearbeitung ohne Validierung

Direkte Eingriffe in TMDL/JSON ohne anschließenden Test in Desktop oder Test-Workspace können zu schwer auffindbaren Fehlern führen. Grundregel: Nach manuellen Änderungen immer laden, refreshen und visuell prüfen.[^2][^10]

## Best Practices (Kurzcheckliste)

- PBIP als Standardformat für Entwicklung verwenden, PBIX nur noch für spezielle Szenarien.[^5][^1]
- Projekte klar strukturieren (ein Ordner pro Bericht/Modell, README, ggf. `docs/`).[^13]
- `.gitignore` sorgfältig pflegen (`localSettings.json`, Caches, temporäre Dateien ausschließen).[^12][^9]
- Änderungen in kleinen, fachlich sinnvollen Commits erfassen und via Pull Requests reviewen.[^8][^7]
- Merge-Konflikte bewusst in TMDL/JSON lösen und anschließend in Desktop validieren.[^8][^2]
- Git-Integration von Fabric nutzen, wenn Premium-Kapazitäten vorhanden sind.[^10]
- Langfristig auf PBIR als Reportformat vorbereiten, da PBIR-Legacy ausläuft.[^6][^1]

## Weiterführende Ressourcen

- Microsoft Learn: Übersicht zu Power BI Desktop Projekten (PBIP) und JSON-Schemas.[^4][^9]
- Microsoft Blog: Roadmap für PBIR als Default-Reportformat und PBIP-GA in 2026.[^1]
- Fachartikel und Blogs zu PBIP, Git und Team-Collaboration.[^11][^8][^12][^7]
- Einführungen zu Power BI-Dateitypen (PBIX, PBIT, PBIP).[^5]

---

## References

1. [PBIR will become the default Power BI Report Format](https://powerbi.microsoft.com/en-us/blog/pbir-will-become-the-default-power-bi-report-format-get-ready-for-the-transition/) - Starting in January 2026, all new reports created in both Power BI Service and Desktop will use the ...

2. [Understanding Power BI Project Files - Directions on Microsoft](https://www.directionsonmicrosoft.com/charts-illustrations/understanding-power-bi-project-files/) - Power BI's new Project (PBIP) file allows developers to save reports and semantic models into a fold...

3. [PBIP vs PBIX: the future of Power BI development - Bravent](https://www.bravent.net/en/news/from-pbix-to-pbip-the-new-development-oriented-power-bi-format/) - Discover how PBIP transforms Power BI with version control, DevOps integration, and AI-ready develop...

4. [Power BI Desktop projects (PBIP) - Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview) - AI Skills Fest. June 8-12, 2026. Build your AI skills with chances to earn prizes and certification ...

5. [Power BI File Types Demystified: Your Guide to PBIX, PBIT, and PBIP](https://doyensys.com/blogs/power-bi-file-types-demystified-your-guide-to-pbix-pbit-and-pbip/) - Understanding the different Power BI file types—PBIX, PBIT, and PBIP—can be confusing for users. Thi...

6. [PBIR Format Power BI: Guide für Entwickler & Git-Integration](https://www.rstefan.at/blog/power-bi-pbir-format-erklaert/) - PBIR Format verstehen: Der neue Standard für Power BI Berichte 2026. Git-Workflows ✓ JSON-Struktur ✓...

7. [Version Control with Git for Power BI Projects: A New Approach](https://cloudfuel.eu/blog/version-control-with-git-for-power-bi-projects-a-new-approach/) - Want to collaborate on a Power BI report? Explore how you can set up version control for Power BI pr...

8. [Power BI projects, Git, and Team Collaboration - Medium](https://medium.com/@sam.campitiello/power-bi-projects-git-and-team-collaboration-97d9e6a64d81) - A new approach with .pbip files and Git integration for developers

9. [Pbir Folder And Files](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report) - Learn about the Power BI Desktop project report folder.

10. [Power BI - Data Models & Reports Version Control in Github and the ...](https://www.thedataschool.co.uk/carol-mhlanga/versioning-data-models-reports-on-github-and-the-pbi-service-fabric-2/) - Power BI does not have built-in version control features but can be integrated with source control s...

11. [Reverse Creating the PBIP file from Source Control - Redgate](https://www.red-gate.com/simple-talk/blogs/reverse-creating-the-pbip-file-from-source-control/) - I illustrate how to use the PBIP file format to include Power BI reports and semantic models in a so...

12. [.gitignore for Power BI Projects: A Simple Guide for the Modern BI ...](https://jihwanpowerbifabric.wixsite.com/supplychainflow/post/gitignore-for-power-bi-projects-a-simple-guide-for-the-modern-bi-developer) - pbip and Git is a major step forward for any serious Power BI developer. It enables true collaborati...

13. [How do you organize your Power BI projects and files? - Reddit](https://www.reddit.com/r/PowerBI/comments/1mcm38k/how_do_you_organize_your_power_bi_projects_and/) - Use the power bi project file type, one folder per report, contianing the pbip file, the documentati...

