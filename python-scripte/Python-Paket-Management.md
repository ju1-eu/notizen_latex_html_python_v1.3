---
title: "Python-Paket-Management"
author: "Jan Unger"
date: "2024-11-26"
---

# Python Paket-Management unter macOS

## Virtuelle Umgebung einrichten

```bash
# Terminal öffnen und zum Projektverzeichnis navigieren
# Virtuelle Umgebung deaktivieren
deactivate
# Optional: Virtuelle Umgebung löschen
rm -rf venv
# Virtuelle Umgebung erstellen
python3 -m venv venv
# Virtuelle Umgebung aktivieren
source venv/bin/activate
```

## Pakete installieren

| **Paket**                  | **Funktionalität**                                                    |
| -------------------------- | --------------------------------------------------------------------- |
| `PyPDF2`                   | Verarbeitung von PDF-Dateien (z. B. Extraktion von Inhalten).         |
| `pytube`                   | Herunterladen von Videos von YouTube.                                 |
| `whisper`                  | Sprach-zu-Text-Transkription (z. B. OpenAI Whisper).                  |
| `youtube-transcript-api`   | Abrufen von Transkripten von YouTube-Videos.                          |
| `black`, `isort`, `flake8` | Tools für Code-Formatierung, Import-Sortierung und Linting.           |
| `mypy`                     | Statische Typprüfung für Python-Code.                                 |
| `Pillow`                   | Bildbearbeitung (z. B. Extraktion und Verarbeitung von Bildern).      |
| `PyMuPDF`                  | Verarbeitung von PDFs (Extraktion von Bildern, Texten etc.).          |
| `rich`                     | Formatierte Konsolenausgabe (z. B. Fortschrittsbalken, farbige Logs). |
| `Jinja2`                   | Template-Engine für Python (z. B. HTML-Generierung).                  |
| `PyYAML`                   | Verarbeitung von YAML-Dateien (Konfiguration, Datenaustausch).        |
| `tqdm`                     | Fortschrittsanzeigen für Schleifen und Iterationen.                   |
| `requests`                 | HTTP-Bibliothek für API-Anfragen und Webzugriffe.                     |
| `certifi`                  | Zertifikate für sichere HTTPS-Verbindungen.                           |
| `typing_extensions`        | Erweiterte Typhinweise für Python < 3.10.                             |

Die Pakete bilden ein kohärentes Set:

- Medienverarbeitung (Video, Audio, PDF, Bilder)
- Entwicklungswerkzeuge (Formatierung, Linting, Typing)
- Webinteraktion (Downloads, API-Zugriffe)
- Ausgabeformatierung und Benutzerinteraktion


```bash
# pip aktualisieren
pip install --upgrade pip
# Benötigte Pakete installieren
pip install PyPDF2 pytube whisper youtube-transcript-api PyMuPDF Pillow rich
# HTML & PDF
pip install Jinja2 MarkupSafe PyYAML tqdm
# Tools installieren
pip install black isort flake8 mypy pipdeptree
```

## Pakete in requirements.txt speichern

```bash
# Alle installierten Pakete in requirements.txt speichern
pip freeze > requirements.txt
# Inhalt anzeigen
cat requirements.txt
# Alle Pakete aus der requirements.txt installieren
pip install -r requirements.txt
```

## Pakete aktualisieren

```bash
# Aktuelle Paketliste anzeigen
pip list
# Veraltete Pakete anzeigen
pip list --outdated
# Alle Pakete aktualisieren
pip list --outdated | cut -d ' ' -f1 | tail -n +3 | xargs -n1 pip install -U
# Nach der Aktualisierung requirements.txt erneuern
pip freeze > requirements.txt
```

## Troubleshooting

```bash
# Cache leeren bei Problemen
pip cache purge

# Paket neu installieren
pip uninstall PyPDF2
pip install PyPDF2

# Konfliktprüfung
pip check

# Requirements als Graph visualisieren
pip install pipdeptree
pipdeptree
```

## Code-Qualität prüfen

```bash
pip install black isort flake8 mypy
# black: Gibt aus, welche Dateien neu formatiert wurden.
black create_gallery.py extract_pdf_images.py pdf_extractor.py
# isort: Ändert die Importreihenfolge oder zeigt fehlerhafte Sortierungen an.
isort create_gallery.py extract_pdf_images.py pdf_extractor.py
# flake8: Gibt Warnungen oder Fehler basierend auf PEP8-Konventionen aus
flake8 create_gallery.py extract_pdf_images.py pdf_extractor.py
# mypy: Gibt Typfehler aus, falls die Typannotationen nicht korrekt sind.
mypy create_gallery.py extract_pdf_images.py pdf_extractor.py

# PDF Kapitel Extraktor *.pdf, Seiten von bis?
python pdf_extractor.py
# Extrahiere Bilder aus *.pdf
python extract_pdf_images.py
# Gallerie: gallery/*_gallery.html
python create_gallery.py

# aktuelle Verzeichnis ($(pwd)) wird zum Python-Suchpfad hinzugefügt. Python Module und Pakete, die sich in diesem Verzeichnis befinden, erkennt und importieren kann.
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Im Entwicklungsmodus wird das Paket nicht kopiert und installiert, sondern als Referenz zur aktuellen Verzeichnisstruktur verlinkt.
# Änderungen am Quellcode sind sofort in der Umgebung verfügbar, ohne dass man das Paket erneut installieren muss.
# Voraussetzung: setup.py
pip install -e .
```

**Konfiguration:**

```bash
# .flake8
[flake8]
# Basis-Konfiguration
max-line-length = 100
max-complexity = 10
statistics = True
docstring-convention = google

# Formatierung
format = %(path)s:%(row)d:%(col)d: %(code)s %(text)s
filename = *.py

# Ignorierte Fehler
ignore = E203, W503, E226

# Ausgeschlossene Pfade
exclude =
    venv/
    .git/
    __pycache__/
    build/
    dist/
    *.egg-info
    .eggs/
    .tox/
    .mypy_cache/


# pyproject.toml (für black und isort)
# Python Code-Formatierung
[tool.black]
line-length = 100
target-version = ['py313']
include = '\.pyx?$'
exclude = '/(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|dist)/'

# Import-Sortierung
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

# Typ-Prüfung
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
ignore_missing_imports = true


# setup.cfg
[flake8]
max-line-length = 100

# Ignorierte Fehler
extend-ignore = D103,D209,D210,D400,D401,F401

# Ausgeschlossene Pfade
exclude =
    .git,
    __pycache__,
    build,
    dist,
    .eggs,
    *.egg,
```


## pre-commit-Tool

1. **pre-commit installieren**
   Installiere `pre-commit` in der virtuellen Umgebung:

   ```bash
   # Pre-commit Setup
   pip install pre-commit            # Tool installieren
   pre-commit --version             # Version prüfen
   # Installation/Update der Hooks
   pre-commit clean                 # Cache leeren
   pre-commit install              # Hooks installieren
   pre-commit install --install-hooks
   pre-commit autoupdate           # Hooks aktualisieren
   pre-commit run --all-files      # Alle Hooks testen
   ```

4. **Pre-Commit-Hooks testen**
   Überprüfe, ob die Hooks korrekt funktionieren:

   ```bash
   ./update_python_packages.sh
   ./check_pythoncode_quality.sh
   ```

`.pre-commit-config.yaml`

```text
repos:
  # Standard Checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace # Entfernt Leerzeichen am Zeilenende
      - id: end-of-file-fixer # Stellt sicher, dass Dateien mit einer neuen Zeile enden
      - id: check-yaml # Validiert die YAML-Syntax
      - id: check-added-large-files
        args: ['--maxkb=800'] # Erhöhe die Grenze (z. B. auf 800 KB)
      - id: check-merge-conflict # Warnt vor verbleibenden Merge-Konflikten
      - id: mixed-line-ending # Konvertiert zu Unix-Zeilenenden (LF)

  # Python Code-Formatierung
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3.13
        files: \.py$ # Nur Python-Dateien prüfen

  # Import-Sortierung
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        files: \.py$ # Nur Python-Dateien prüfen

  # Code-Style & Dokumentation
  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        additional_dependencies:
          - flake8-docstrings # Docstring-Check
        args: [--max-line-length=100, --ignore=D203]
        files: \.py$ # Nur Python-Dateien prüfen

  # Typprüfung
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-PyYAML
          - types-requests
          - types-Pillow
        files: \.py$

  # LaTeX Syntaxprüfung (optional)
  - repo: https://github.com/cmhughes/latexindent.pl
    rev: V3.24.4
    hooks:
      - id: latexindent
        args: ['-l']
        files: '.*\.tex$'

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest --cov --cov-report=term-missing
        language: system
        types: [python]
        pass_filenames: false
        verbose: true
```

`.github/workflow/ci.yml`

```text
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run code quality checks
        run: |
          source venv/bin/activate
          ./check_pythoncode_quality.sh
```

## Projektspezifische requirements.txt

```text
# requirements.in
# Produktionsabhängigkeiten

## PDF-Verarbeitung
PyMuPDF
PyPDF2

## Medienverarbeitung
Pillow
pytube
whisper
youtube-transcript-api

## Dokumentenverarbeitung
markdown-it-py
defusedxml
Jinja2
MarkupSafe

## CLI & Formatierung
click
rich
tqdm

## Konfiguration & Utils
PyYAML
python-dotenv
packaging

## Netzwerk & Encoding
requests


# requirements-dev.in
# Entwicklungsabhängigkeiten

## Basis-Abhängigkeiten
-r requirements.in

## Code-Formatierung & Linting
black
flake8
isort
pycodestyle
pyflakes
mccabe

## Typ-Prüfung
mypy
mypy-extensions
typing_extensions
types-Pillow
types-PyYAML
types-requests
types-tqdm

## Testen
pytest
pytest-cov
coverage
iniconfig
pluggy

## Tools
pipdeptree
pre-commit
identify
nodeenv
virtualenv
platformdirs
pathspec
cfgv
distlib
filelock

## Abhängigkeiten von Entwicklungswerkzeugen
build
pip-tools
pyproject-hooks
setuptools
wheel
```

# Projektstruktur

```plaintext
# Projektstruktur anzeigen
tree -L 2 --dirsfirst
# Projektstruktur erfolgt nach Python-Projektstandards
# Ausgabe kommentieren
```

## Tipps und Best Practices

1. **Virtuelle Umgebung**:
   - Immer in einer virtuellen Umgebung arbeiten
   - Für jedes Projekt eine separate Umgebung erstellen
   - Namen der virtuellen Umgebung (venv) in .gitignore aufnehmen

2. **Requirements**:
   - Requirements.txt regelmäßig aktualisieren
   - Version in Kommentaren dokumentieren
   - Backup der funktionierenden requirements.txt anlegen

3. **Sicherheit**:
   - Regelmäßig nach Sicherheitsupdates suchen
   - Pakete nur aus vertrauenswürdigen Quellen installieren
   - Bei Produktivnutzung fixe Versionen verwenden

## Automatisierungsskript I

```bash
#!/bin/bash
# update_python_packages.sh
# Farben und Formatierung
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
BOLD='\033[1m'

# Logging-Funktionen
log_file="update_log.txt"

setup_logging() {
    echo "=== Python Package Update Log $(date) ===" > "$log_file"
}

log() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$message" >> "$log_file"
}

print_status() {
    local message="[INFO] $1"
    echo -e "${BLUE}${message}${NC}"
    log "$message"
}

print_success() {
    local message="[SUCCESS] $1"
    echo -e "${GREEN}${message}${NC}"
    log "$message"
}

print_error() {
    local message="[ERROR] $1"
    echo -e "${RED}${message}${NC}" >&2
    log "ERROR: $1"
}

print_warning() {
    local message="[WARNING] $1"
    echo -e "${YELLOW}${message}${NC}"
    log "WARNING: $1"
}

print_header() {
    echo -e "\n${BOLD}=== $1 ===${NC}"
    echo -e "${BOLD}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo "----------------------------------------"
    log "=== $1 ==="
}

# Cleanup-Funktion
cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        print_status "Führe Cleanup durch..."
        deactivate 2>/dev/null || true
    fi
    print_status "Skript beendet."
}

trap cleanup EXIT

# Hauptskript
main() {
    setup_logging
    print_header "Python Package Updater Start"

    # Prüfe Python-Installation
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 nicht gefunden!"
        exit 1
    fi

    # Prüfe virtuelle Umgebung
    if [ ! -d "venv" ]; then
        print_error "Virtuelle Umgebung (venv/) nicht gefunden!"
        print_status "Erstellen Sie eine neue virtuelle Umgebung mit: python3 -m venv venv"
        exit 1
    fi

    # Aktiviere virtuelle Umgebung
    print_status "Aktiviere virtuelle Umgebung..."
    source venv/bin/activate || {
        print_error "Fehler beim Aktivieren der virtuellen Umgebung!"
        exit 1
    }

    # Pip Update
    print_header "Aktualisiere pip"
    pip install --upgrade pip || {
        print_error "Pip-Update fehlgeschlagen!"
        exit 1
    }

    # Installiere oder aktualisiere pip-tools
    print_header "Installiere/aktualisiere pip-tools"
    pip install --upgrade pip-tools || {
        print_error "Installation von pip-tools fehlgeschlagen!"
        exit 1
    }

    # Kompiliere requirements.txt
    if [ -f "requirements.in" ]; then
        print_header "Kompiliere requirements.txt"
        if pip-compile requirements.in --strip-extras; then
            print_success "requirements.txt erfolgreich erstellt."
        else
            print_error "Fehler beim Kompilieren von requirements.txt"
            exit 1
        fi
    else
        print_error "requirements.in nicht gefunden!"
        exit 1
    fi

    # Kompiliere requirements-dev.txt
    if [ -f "requirements-dev.in" ]; then
        print_header "Kompiliere requirements-dev.txt"
        if pip-compile requirements-dev.in --strip-extras; then
            print_success "requirements-dev.txt erfolgreich erstellt."
        else
            print_error "Fehler beim Kompilieren von requirements-dev.txt"
            exit 1
        fi
    else
        print_error "requirements-dev.in nicht gefunden!"
        exit 1
    fi

    # Installiere Abhängigkeiten
    print_header "Installiere Produktionsabhängigkeiten"
    if pip install -r requirements.txt; then
        print_success "Produktionsabhängigkeiten installiert."
    else
        print_error "Fehler beim Installieren der Produktionsabhängigkeiten!"
        exit 1
    fi

    print_header "Installiere Entwicklungsabhängigkeiten"
    if pip install -r requirements-dev.txt; then
        print_success "Entwicklungsabhängigkeiten installiert."
    else
        print_error "Fehler beim Installieren der Entwicklungsabhängigkeiten!"
        exit 1
    fi

    print_success "Update-Prozess erfolgreich abgeschlossen!"
}

# Starte Hauptprogramm
main "$@"
```

Nutzung:
```bash
chmod +x update_python_packages.sh
#source venv/bin/activate
./update_python_packages.sh
```

## Automatisierungsskript II

```bash
#!/bin/bash
# check_pythoncode_quality.sh
# Farben und Formatierung
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
BOLD='\033[1m'

# Ausgabefunktionen
print_header() {
    echo -e "\n${BOLD}=== $1 ===${NC}"
    echo "----------------------------------------"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Dynamische Ermittlung der Python-Dateien
find_python_files() {
    local exclude_dirs=("venv" "__pycache__" ".git" "build" "dist" "*.egg-info" ".eggs" ".tox" ".mypy_cache")
    local find_args=(-type f -name '*.py')

    for dir in "${exclude_dirs[@]}"; do
        find_args+=(-not -path "./$dir/*" -not -path "./$dir")
    done

    # shellcheck disable=SC2207
    PYTHON_FILES=($(find . "${find_args[@]}"))
}

# Prüfe Voraussetzungen
check_requirements() {
    local tools=("black" "isort" "flake8" "mypy")
    local missing_tools=()

    print_status "Prüfe Voraussetzungen..."

    # Prüfe Python Version
    python_version=$(python3 -V 2>&1 | cut -d' ' -f2)
    print_status "Gefundene Python-Version: $python_version"
    if ! python3 -c "import sys; exit(1 if sys.version_info < (3,7) else 0)"; then
        print_error "Python 3.7 oder höher wird benötigt!"
        exit 1
    fi

    # Prüfe virtuelle Umgebung
    if [ ! -d "venv" ]; then
        print_error "Virtuelle Umgebung (venv/) nicht gefunden!"
        print_status "Möchten Sie eine neue virtuelle Umgebung erstellen? (j/n)"
        read -r answer
        if [[ "$answer" =~ ^[Jj] ]]; then
            print_status "Erstelle neue virtuelle Umgebung..."
            if python3 -m venv venv; then
                print_success "Virtuelle Umgebung erfolgreich erstellt"
            else
                print_error "Fehler beim Erstellen der virtuellen Umgebung!"
                print_status "Führen Sie manuell aus: python3 -m venv venv"
                exit 1
            fi
        else
            print_status "Abbruch. Erstellen Sie eine neue virtuelle Umgebung mit: python3 -m venv venv"
            exit 1
        fi
    fi

    # Prüfe venv Struktur
    if [ ! -f "venv/bin/activate" ]; then
        print_error "Virtuelle Umgebung scheint beschädigt zu sein!"
        print_status "Versuche Reparatur durch Neuerstellen..."
        rm -rf venv
        if python3 -m venv venv; then
            print_success "Virtuelle Umgebung erfolgreich neu erstellt"
        else
            print_error "Reparatur fehlgeschlagen!"
            exit 1
        fi
    fi

    # Aktiviere virtuelle Umgebung mit erweiterter Fehlerbehandlung
    print_status "Aktiviere virtuelle Umgebung..."
    if ! source venv/bin/activate 2>/dev/null; then
        print_error "Fehler beim Aktivieren der virtuellen Umgebung!"
        print_status "Versuche alternative Aktivierungsmethode..."

        if ! . venv/bin/activate 2>/dev/null; then
            print_error "Aktivierung fehlgeschlagen!"
            print_status "Mögliche Probleme:"
            print_status "- Fehlerhafte Berechtigungen"
            print_status "- Beschädigte virtuelle Umgebung"
            print_status "- Shell-Kompatibilitätsprobleme"
            print_status "Versuchen Sie:"
            print_status "1. chmod -R 755 venv"
            print_status "2. Neu erstellen mit: rm -rf venv && python3 -m venv venv"
            exit 1
        fi
    fi

    # Prüfe erfolgreiche Aktivierung
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Virtuelle Umgebung wurde nicht korrekt aktiviert!"
        exit 1
    fi

    # Zeige venv Status
    print_success "Virtuelle Umgebung aktiv: $VIRTUAL_ENV"
    print_status "Python-Version in venv: $(python -V 2>&1)"

    # Optional: Prüfe pip Installation und Version
    if ! command -v pip >/dev/null 2>&1; then
        print_error "pip nicht gefunden in virtueller Umgebung!"
        print_status "Installiere pip..."
        if curl https://bootstrap.pypa.io/get-pip.py | python; then
            print_success "pip erfolgreich installiert"
        else
            print_error "pip Installation fehlgeschlagen!"
            exit 1
        fi
    fi

    pip_version=$(pip -V | cut -d' ' -f2)
    print_status "pip Version: $pip_version"

    # Prüfe Code-Qualitäts-Tools
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done

    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Folgende Tools fehlen:"
        for tool in "${missing_tools[@]}"; do
            echo "  - $tool"
        done
        print_status "Installation mit: pip install ${missing_tools[*]}"
        exit 1
    fi
}

# Führe Tool aus und prüfe Ergebnis
run_tool() {
    local tool=$1
    shift
    local files=("$@")

    print_header "Führe $tool aus"

    if [ "${#files[@]}" -eq 0 ]; then
        print_warning "Keine Dateien zum Prüfen gefunden."
        return 0
    fi

    if "$tool" "${files[@]}"; then
        print_success "$tool erfolgreich ausgeführt"
        return 0
    else
        print_error "$tool hat Fehler gefunden"
        return 1
    fi
}

# Hauptfunktion
main() {
    print_header "Python Code-Qualitätsprüfung"
    check_requirements

    find_python_files

    # Debug-Ausgabe
    print_status "Gefundene Python-Dateien:"
    for file in "${PYTHON_FILES[@]}"; do
        echo "  $file"
    done

    local has_errors=0

    # Führe Tools aus
    run_tool "black" "${PYTHON_FILES[@]}" || has_errors=1
    run_tool "isort" "${PYTHON_FILES[@]}" || has_errors=1
    run_tool "flake8" "${PYTHON_FILES[@]}" || has_errors=1
    run_tool "mypy" "${PYTHON_FILES[@]}" || has_errors=1

    # Zusammenfassung mit Exit-Code
    print_header "Zusammenfassung"
    if [ $has_errors -eq 0 ]; then
        print_success "Alle Qualitätsprüfungen erfolgreich abgeschlossen"
        exit 0
    else
        print_error "Einige Qualitätsprüfungen haben Fehler gefunden"
        exit 1
    fi
}

# Starte Hauptprogramm
main "$@"
```

Nutzung:
```bash
chmod +x check_pythoncode_quality.sh
#source venv/bin/activate
./check_pythoncode_quality.sh
```
