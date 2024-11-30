---
title: "Markdown"
thema: "Anwendung von Markdown-Techniken für Dokumentationen"
runningtitle: "Dokumentation mit Markdown"
keywords: "\\textbf{Keywords:} Markdown, Pandoc, Latex, Python, Git"
abstract: |
  Markdown
  Ein 2004 von Gruber/Swartz entwickeltes leichtgewichtiges Auszeichnungsformat für menschen- und maschinenlesbare formatierte Texte. Ideal für technische Dokumentation.

  Pandoc
  Ein von MacFarlane entwickelter universeller Dokumentenkonverter für verschiedene Markup-Formate. Open-Source-Tool für akademische und technische Dokumentation.

  LaTeX
  Ein 1984 von Lamport entwickeltes Textsatzsystem (basierend auf Knuths TeX, 1978). Standard für wissenschaftliche Publikationen mit hochwertiger Typografie und Formelsatz.

  Python
  Eine 1991 von van Rossum entwickelte Programmiersprache mit klarer Syntax. Anwendung in Wissenschaft, Datenanalyse, KI und Webentwicklung.

  Git
  Ein 2005 von Torvalds entwickeltes verteiltes Versionskontrollsystem. Standard für Softwareprojekte mit Branch-Konzept für parallele Entwicklung.
date: \today
---
<!-------------------------------------------------------------------------------------------------------------
ju 26-11-24 mein-dokument.md
Quelle [@spanner:2019:robotik].
Fußnote.[^1]
[^1]: Text der Fußnote.
[Google](https://www.google.com)
![Logo 2](images/Logo/Logo2.pdf){width=60%}
---------------------------------------------------------------------------------------------------------------->

## Git

![Was ist Git?](images/Mindmap-Git.pdf){width=60%}

```bash
# GitHub-Anmeldung und Zugangsdaten zwischenspeichern
gh auth login
git config --global credential.helper cache

# Remote-Verbindungen anzeigen
git remote -v

# Lokales Backup-Repository einrichten
git init --bare
git remote add local /Users/jan/notizen_latex_html_python_v1.3.git
git remote rename localBackup local
git push local main
git pull local main

# GitHub-Repository einrichten
git init
git remote add origin git@github.com:ju1-eu/notizen_latex_html_python_v1.3.git
git branch -M main
git push -u origin main
git pull origin main

# Standardbefehle für Synchronisation
git push  # Änderungen hochladen
git pull  # Änderungen herunterladen
git st    # Status anzeigen
git ls    # Dateien auflisten

# Repository klonen
git clone https://github.com/ju1-eu/notizen_latex_html_python_v1.3.git
git clone /Users/jan/notizen_latex_html_python_v1.3.git notizen_klon
```

## Latex

```bash
# TeX Live Manager und Updates
wget https://mirror.ctan.org/systems/texlive/tlnet/update-tlmgr-latest.sh # Manager herunterladen
sudo sh update-tlmgr-latest.sh -- --accept # Update ausführen
sudo chown -R $(whoami) /usr/local/texlive/ # Nutzerrechte setzen

# Paket-Management
tlmgr install pgf # PGF/TikZ-Paket installieren
tlmgr update --all # Alle Pakete aktualisieren

# System-Überprüfung
tlmgr --version # Version anzeigen
tlmgr list --installed # Installierte Pakete auflisten
```

# Markdown

## Quellenangabe

- Fachbuchautor [@dalwigk:2024:fachbuchautor].
- Online Kurse [@schaffranek:2024:kurse].
- Hacking und Cyber Security mit KI [@dalwigk:2023:hacking].
- Python für Einsteiger [@dalwigk:2022:python].
- Mikrocontroller ESP32 [@brandes:2023:mikrocontroller].
- Roboterauto [@brandes:2022:esp32].
- Daten mit Raspberry Pi im Netz speichern und visualisieren [@brandes:2023:daten].

Hier ist ein Text, der eine Fußnote benötigt.[^2]

[^2]: Text der Fußnote.

## Liste

1. eins
2. zwei

- neu
- [ ] check
- [x] gecheckt


## Tabelle

**Tabelle 1:** Diese Tabelle gibt eine übersichtliche Darstellung der ausgeführten Skripte, ihrer jeweiligen Funktionen.

| Skriptname                      | Beschreibung                          |
| :------------------------------ | :------------------------------------ |
| `html1_konverter_pandoc.py`     | Konvertiert HTML-Dokumente mit Pandoc |
| `html2_dateien_verarbeiten.py`  | Verarbeitet HTML-Dateien              |
| `html3_navigation.py`           | Erzeugt Navigationsseiten             |
| `html4_entfernen.py`            | Entfernt HTML-Markup                  |
| `latex_convert1.py`             | Konvertiert LaTeX-Dokumente           |
| `latexcode_entfernen2.py`       | Entfernt LaTeX-Markup                 |
| `dokumentation.py`              | Erstellt Projekt-Dokumentation        |
| `dateien_inhaltsverzeichnis.py` | Generiert Datei-Index                 |
| `git_hilfsprogramm.py`          | Git-Hilfsfunktionen                   |
| `scriptauswahl.py`              | Skript-Auswahlmenü                    |
| `suchen_ersetzen.py`            | Text suchen/ersetzen                  |
| `sync_tex.py`                   | Synchronisiert TeX-Dateien            |
| `image_resizer.py`              | Bildgrößen anpassen                   |
| `create_gallery.py`             | Erstellt Bildergalerie                |
| `extract_pdf_images.py`         | Extrahiert Bilder aus PDFs            |
| `pdf_extractor.py`              | PDF-Daten extrahieren                 |
| `youtube_text_extraktor.py`     | YouTube-Untertitel extrahieren        |


## Bilder

![Logo 2](images/Logo/Logo2.pdf){width=40%}

![Was ist eine Mindmap?](images/Mindmap.pdf){width=60%}

![Was ist Python?](images/Mindmap-Python.pdf){width=60%}

## Links

Website [Google](https://www.google.com) und GitHub <https://github.com/ju1-eu> und meine Website <https://bw-ju.de/>

\newpage
## Quellcode

```c
/* Quellcode: HalloWelt.c */
#include <stdio.h>

int main() {
   printf("Hallo Welt\n");
   return 0;
}
```

```cpp
// Quellcode: HalloWelt.cpp
#include <iostream>

int main() {
    std::cout << "Hallo Welt" << std::endl;
    return 0;
}
```

```markdown
// Markdown
[Google](https://www.google.com)

![Logo 2](images/Logo/Logo2.pdf){width=50%}
```

# Dokumentenverarbeitung LaTeX/HTML/Python

Toolset zur automatisierten Dokumentenverarbeitung mit LaTeX, HTML und Python.

## Projektstruktur

- `/content`: Vorlagen für Makefile, LaTeX und CSS
- `/python-scripte`: Automatisierungsskripte
- `/venv`: Isolierte Python-Umgebung

```plaintext
# Projektstruktur anzeigen
tree -L 2 --dirsfirst
# Projektstruktur erfolgt nach Python-Projektstandards
# Ausgabe kommentieren
.
├── Mindmap/          # Mindmap-Vorlagen und -Dateien
│   └── Mindmap-Vorlage.tex
├── Tabellen/         # PDF-Tabellen und Inputlisten
│   ├── PDF/
│   └── input-PDFs.txt
├── content/          # Projektvorlagen & -Ressourcen
│   ├── Makefile
│   ├── *.tex        # LaTeX-Vorlagen
│   ├── *.html       # HTML-Vorlagen
│   ├── *.bib        # Literaturverzeichnisse
│   └── *.css        # Stylesheets
├── html/            # HTML-Ausgabedateien
├── images/          # Bilder und Mindmaps
├── md/              # Markdown-Quelldateien
├── python-scripte/  # Automatisierungsskripte
├── tex/             # LaTeX-Ausgabedateien
└── venv/            # Python virtuelle Umgebung
```

## Tools

- Dokumentenverarbeitung: Markdown, LaTeX, HTML
- Medien: Bild-/PDF-Extraktion, Video-Transkription
- Code-Qualität: pre-commit hooks, Linting
- Versionierung: Git-Integration


```bash
# Python Setup
python3 -m venv venv
source venv/bin/activate
./update_python_packages.sh      # Python-Pakete aktualisieren

# LaTeX
tlmgr install pgf
sudo tlmgr update --all

# Repository initialisieren
git init
# Speichert Git-Zugangsdaten temporär im Speicher, sodass sie nicht bei jedem Push/Pull erneut eingegeben werden müssen.
git config --global credential.helper cache
# GitHub CLI-Tool zur Authentifizierung
gh auth login

# Repository Setup
git remote add origin https://github.com/ju1-eu/notizen_latex_html_python_v1.3.git
git remote add local /Users/jan/notizen_latex_html_python_v1.3.git

# Workflow
git status              # Status prüfen
git add .               # Änderungen stagen
git commit -m "Update"  # Committen
git push origin main    # Nach GitHub pushen
git push backup main    # Lokales Backup

# Branches
git checkout -b feature # Neuen Branch erstellen
git merge feature      # In main mergen
git branch -d feature  # Branch löschen

# Weitere Befehle
git pull               # Updates holen
git log               # Historie anzeigen
git diff               # Änderungen zeigen
git reset --hard HEAD  # Auf letzten Commit zurück


# Pre-commit Setup
pip install pre-commit            # Tool installieren
pre-commit --version             # Version prüfen
# Installation/Update der Hooks
pre-commit clean                 # Cache leeren
pre-commit install              # Hooks installieren
pre-commit autoupdate           # Hooks aktualisieren
pre-commit run --all-files      # Alle Hooks testen
```

Konfigurationsdateien:

```plaintext
.pre-commit-config.yaml    # Pre-commit Hook-Konfiguration
pyproject.toml            # Python Projekt & Tool-Konfiguration
setup.cfg                # Python Package-Konfiguration
config.yaml             # Skript-Konfiguration
requirements.txt        # Python Abhängigkeiten
requirements-dev.txt    # Entwickler-Abhängigkeiten
```

Die wichtigsten Konfigurationen erfolgen in `.pre-commit-config.yaml` für Hooks und `config.yaml` für Skript-Optionen.

## Python Scripte

```bash
# Update & Qualitätssicherung
./update_python_packages.sh           # Python-Pakete aktualisieren
./check_pythoncode_quality.sh         # Code-Qualität prüfen (black, isort, flake8, mypy)

# Projekt-Tools
python scriptauswahl.py               # Menü für LaTeX/HTML-Befehle

# Bildverarbeitung
python image_resizer.py               # Bildoptimierung
python create_gallery.py              # Responsive Bildergalerie
python extract_pdf_images.py          # PDF-Bild-Extraktion

# PDF/Video
python pdf_extractor.py               # PDF-Kapitel extrahieren
python youtube_text_extraktor.py      # YouTube-Untertitel/Transkription
```

## Hauptfunktionen

- LaTeX/HTML-Konvertierung
- Dokumentenformatierung
- Bildverarbeitung
- Git-Integration
- Navigationsaufbau

## Installation

```bash
python -m venv venv
source venv/bin/activate
```

## Verwendung

```bash
python scriptauswahl.py
```

## Voraussetzungen

- Python 3.x
- LaTeX
- Pandoc
- Git

## Lizenz

MIT

# Python Package Update Script

Automatisiertes Update-Tool für Python-Pakete in einer virtuellen Umgebung.

## Features

- Update von Produktions- und Entwicklungspaketen
- Backup bestehender Requirements
- Detailliertes Update-Logging
- Fehlerbehandlung
- Farbige Konsolenausgabe

## Voraussetzungen

- Python 3.x Installation
- Virtuelle Umgebung (venv)
- requirements.txt / requirements-dev.txt
- Bash/zsh Shell

## Verwendung

```bash
chmod +x update_python_packages.sh
./update_python_packages.sh
```

## Output

- Backup-Dateien (.backup.txt)
- Aktualisierte Requirements
- Update-Log (update_log.txt)

## Version
2.0 (2024-11-26)

# Python Code Quality Check Script

Automatisierte Code-Qualitätsprüfung für Python-Skripte.

## Tools

- black (Formatierung)
- isort (Imports)
- flake8 (Style)
- mypy (Typen)

## Verwendung

```bash
chmod +x check_pythoncode_quality.sh
./check_pythoncode_quality.sh
```

## Features

- Virtuelle Umgebung Check/Setup
- Tool-Verfügbarkeit Check
- Dateiprüfung
- Farbige Konsolenausgabe
- Fehlerbehandlung

## Voraussetzungen

- Python 3.7+
- Virtuelle Umgebung (venv)
- Code-Qualitäts-Tools

## Version
1.0 (2024-11-26)


# PDF Kapitel Extraktor

Ein Python-Skript zum Extrahieren und Speichern von PDF-Seitenbereichen.

## Features
- Extraktion von Seitenbereichen
- Metadaten-Übertragung
- Optionale Komprimierung
- Fortschrittsanzeige
- Fehlerbehandlung

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install pypdf2
```

## Verwendung
```python
# Als Skript
python pdf_extraktor.py

# Als Modul
from pdf_extraktor import extrahiere_kapitel
extrahiere_kapitel("input.pdf", "output.pdf", 1, 5)
```

## Funktionen
- `get_pdf_info()`: Liest PDF-Metadaten
- `validiere_eingaben()`: Prüft Benutzereingaben
- `extrahiere_kapitel()`: Extrahiert Seitenbereich

## Version
1.0 (2024-11-26)


# PDF Bilder Extraktor

Python-Tool zur Extraktion von Bildern aus PDF-Dateien.

## Features
- Multi-Format-Extraktion (JPEG, PNG, WebP)
- Qualitätsfilterung
- Bildoptimierung
- Fortschrittsanzeige
- Ausführliches Logging

## Installation
```bash
pip install PyMuPDF Pillow rich tqdm
```

## Hauptfunktionen
- `PDFImageExtractor`: Hauptklasse für Extraktion
- `ImageConfig`: Konfigurationseinstellungen
- Qualitäts- und Größenprüfung
- Bildoptimierung
- Metadatenextraktion

## Verwendung
```python
config = ImageConfig(
    min_width=200,
    min_height=200,
    max_size_mb=10.0,
    quality=90,
    optimize=True
)

extractor = PDFImageExtractor(
    pdf_path="input.pdf",
    output_dir="images",
    project_name="project",
    image_format="png",
    config=config
)

stats = extractor.extract_images()
```

## Version
1.0 (2024-11-26)


# HTML Galerie Generator

Python-Tool zur Erstellung responsiver Bildergalerien.

## Features
- Grid-Layout & Lightbox
- Theme-Optionen
- Bildoptimierung
- Thumbnails
- Sortierung/Filter
- Lazy Loading

## Installation
```bash
pip install pillow
```

## Hauptkomponenten
- `GalleryConfig`: Galerie-Einstellungen
- `GalleryGenerator`: Galerie-Generierung
- Theme-Generator
- Thumbnail-Erstellung
- Responsive Design

## Verwendung
```python
config = GalleryConfig(
    title="Meine Galerie",
    theme="light",
    columns_desktop=4,
    thumbnail_size=(300, 300)
)

generator = GalleryGenerator(
    image_dir="images",
    project_name="project",
    output_dir="gallery",
    config=config
)

generator.generate_gallery()
```

## Version
1.0 (2024-11-26)


# YouTube Text Extraktor

Tool zur Extraktion von Text aus YouTube-Videos.

## Features
- Untertitel-Extraktion
- Audio-Download
- Whisper-Transkription
- Automatische Formatbereinigung
- Mehrsprachig (DE/EN)

## Installation
```bash
pip install youtube-transcript-api pytube whisper
```

## Funktionen
```python
prüfe_url(url: str) -> bool
hole_video_id(url: str) -> str
hole_untertitel(video_id: str) -> str|None
extrahiere_audio(url: str) -> str|None
transkribiere_audio(audio_pfad: str) -> str|None
extrahiere_text_aus_video(url: str) -> str
speichere_text(text: str) -> None
```

## Verwendung
```python
from youtube_text_extraktor import extrahiere_text_aus_video

url = "http://youtu.be/VIDEO_ID"
text = extrahiere_text_aus_video(url)
```

## Version
1.0 (2024-11-26)
