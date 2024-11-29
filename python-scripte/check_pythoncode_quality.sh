#!/bin/bash -e
# ============================================================================
# Script: check_pythoncode_quality.sh
# ============================================================================
#
# BESCHREIBUNG
#   Automatisierte Code-Qualitätsprüfung für Python-Skripte.
#   Führt folgende Tools aus:
#   - black (Code-Formatierung)
#   - isort (Import-Sortierung)
#   - flake8 (Style Guide)
#   - mypy (Statische Typ-Prüfung)
#
# VORAUSSETZUNGEN
#   - Python-Installation
#   - Installierte Tools: black, isort, flake8, mypy
#   - Python-Skripte im Verzeichnis ./python-scripte/
#
# VERWENDUNG
#   chmod +x check_pythoncode_quality.sh
#   ./check_pythoncode_quality.sh
#
# AUTOR
#   Jan
#
# VERSION
#   1.0
#
# DATUM
#   2024-11-26
# ============================================================================

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

# Definiere Verzeichnis und Dateien
SCRIPT_DIR="python-scripte"
PYTHON_FILES=(
    "$SCRIPT_DIR/dateien_inhaltsverzeichnis.py"
    "$SCRIPT_DIR/dokumentation.py"
    "$SCRIPT_DIR/git_hilfsprogramm.py"
    "$SCRIPT_DIR/html1_konverter_pandoc.py"
    "$SCRIPT_DIR/html2_dateien_verarbeiten.py"
    "$SCRIPT_DIR/html3_navigation.py"
    "$SCRIPT_DIR/html4_entfernen.py"
    "$SCRIPT_DIR/latex_convert1.py"
    "$SCRIPT_DIR/latexcode_entfernen2.py"
    "$SCRIPT_DIR/suchen_ersetzen.py"
    "$SCRIPT_DIR/sync_tex.py"
    "$SCRIPT_DIR/extract_pdf_images.py"
    "$SCRIPT_DIR/pdf_extractor.py"
    "$SCRIPT_DIR/create_gallery.py"
    "$SCRIPT_DIR/youtube_text_extraktor.py"
    "image_resizer.py"
    "scriptauswahl.py"
)

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

    # Prüfe venv Verzeichnis und Status
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

    # Prüfe Verzeichnis
    if [ ! -d "$SCRIPT_DIR" ]; then
        print_error "Verzeichnis $SCRIPT_DIR nicht gefunden!"
        exit 1
    fi

    # Prüfe ob Dateien existieren
    local missing_files=false
    for file in "${PYTHON_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            print_warning "Datei nicht gefunden: $file"
            missing_files=true
        fi
    done

    if [ "$missing_files" = true ]; then
        print_warning "Einige Dateien wurden nicht gefunden. Fortfahren mit vorhandenen Dateien."
    fi
}

# Führe Tool aus und prüfe Ergebnis
run_tool() {
    local tool=$1
    local files=("${@:2}")

    print_header "Führe $tool aus"
    if "$tool" "${files[@]}"; then
        print_success "$tool erfolgreich ausgeführt"
        return 0
    else
        print_warning "$tool hat Probleme gefunden"
        return 1
    fi
}

# Hauptfunktion
main() {
    print_header "Python Code-Qualitätsprüfung"
    check_requirements

    local has_errors=0

    # Führe Tools aus
    run_tool "black" "${PYTHON_FILES[@]}" || has_errors=1
    run_tool "isort" "${PYTHON_FILES[@]}" || has_errors=1
    run_tool "flake8" "${PYTHON_FILES[@]}" || has_errors=1
    run_tool "mypy" "${PYTHON_FILES[@]}" || has_errors=1

    print_header "Zusammenfassung"
    if [ $has_errors -eq 0 ]; then
        print_success "Alle Qualitätsprüfungen erfolgreich abgeschlossen"
    else
        print_warning "Einige Qualitätsprüfungen haben Probleme gefunden"
    fi
}

# Starte Hauptprogramm
main "$@"
