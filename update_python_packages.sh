#!/bin/bash -e
# ============================================================================
# Script: update_python_packages.sh
# ============================================================================
#
# BESCHREIBUNG
#   Automatisiertes Update-Tool für Python-Pakete in einer virtuellen Umgebung.
#   Das Skript verwendet pip-tools zur Verwaltung der Abhängigkeiten.
#
# VORAUSSETZUNGEN
#   - Aktive Python-Installation
#   - Virtuelle Umgebung unter ./venv/
#   - Existierende requirements.in und requirements-dev.in
#   - Bash oder kompatible Shell (z.B. zsh)
#
# VERWENDUNG
#   chmod +x update_python_packages.sh
#   ./update_python_packages.sh
#
# AUSGABEDATEIEN
#   - requirements.txt - Aktualisierte Produktionsabhängigkeiten mit festen Versionen
#   - requirements-dev.txt - Aktualisierte Entwicklungsabhängigkeiten mit festen Versionen
#   - update_log.txt - Detailliertes Update-Log
#
# VERSION
#   3.0
#
# DATUM
#   2024-11-30
# ============================================================================

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
