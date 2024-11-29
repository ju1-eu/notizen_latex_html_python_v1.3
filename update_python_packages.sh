#!/bin/bash -e
# ============================================================================
# Script: update_python_packages.sh
# ============================================================================
#
# BESCHREIBUNG
#   Automatisiertes Update-Tool für Python-Pakete in einer virtuellen Umgebung.
#   Das Skript behandelt sowohl Produktions- als auch Entwicklungsabhängigkeiten.
#
# VORAUSSETZUNGEN
#   - Aktive Python-Installation
#   - Virtuelle Umgebung unter ./venv/
#   - Existierende requirements.txt und requirements-dev.txt
#   - Bash oder kompatible Shell (z.B. zsh)
#
# VERWENDUNG
#   chmod +x update_python_packages.sh
#   ./update_python_packages.sh
#
# AUSGABEDATEIEN
#   - requirements.backup.txt - Backup der Produktionsabhängigkeiten
#   - requirements-dev.backup.txt - Backup der Entwicklungsabhängigkeiten
#   - requirements.txt - Aktualisierte Produktionsabhängigkeiten
#   - requirements-dev.txt - Aktualisierte Entwicklungsabhängigkeiten
#   - update_log.txt - Detailliertes Update-Log
#
# VERSION
#   2.0
#
# DATUM
#   2024-11-26
# ============================================================================

# Farben und Formatierung bleiben gleich...
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
BOLD='\033[1m'

# Logging-Funktionen bleiben gleich...
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

# Cleanup-Funktion bleibt gleich...
cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        print_status "Führe Cleanup durch..."
        deactivate 2>/dev/null || true
    fi
    print_status "Skript beendet."
}

trap cleanup EXIT

# Neue Funktion zum Aktualisieren der Paketlisten
update_requirements() {
    local req_type=$1
    local file_name="requirements${req_type}.txt"
    local backup_file="requirements${req_type}.backup_${timestamp}.txt"

    print_header "Bearbeite ${file_name}"

    if [ ! -f "$file_name" ]; then
        print_warning "${file_name} nicht gefunden, überspringe..."
        return
    fi

    # Backup erstellen
    cp "$file_name" "$backup_file"
    print_success "Backup erstellt: $backup_file"

    # Pakete aus der jeweiligen requirements-Datei aktualisieren
    while IFS= read -r line; do
        # Überspringe Kommentare und leere Zeilen
        if [[ $line =~ ^#.*$ ]] || [ -z "$line" ] || [[ $line =~ ^-r.* ]]; then
            continue
        fi

        # Extrahiere Paketnamen (ohne Version)
        package=$(echo "$line" | cut -d'=' -f1)
        print_status "Aktualisiere: $package"

        if pip install -U "$package"; then
            print_success "$package erfolgreich aktualisiert"
        else
            print_warning "Problem beim Update von $package"
        fi
    done < "$file_name"

    # Neue requirements-Datei erstellen
    if [ "$req_type" = "" ]; then
        # Für requirements.txt: Nur Produktionsabhängigkeiten
        pip freeze > temp_requirements.txt
        # Entferne Entwicklungspakete
        grep -v -f requirements-dev.txt temp_requirements.txt > "$file_name" || true
        rm temp_requirements.txt
    else
        # Für requirements-dev.txt: Entwicklungsabhängigkeiten
        pip freeze > "$file_name"
    fi

    print_success "Neue ${file_name} erstellt"

    # Änderungsübersicht
    print_header "Änderungsübersicht für ${file_name}"
    if ! diff "$backup_file" "$file_name"; then
        print_status "Siehe oben für die Änderungen"
    else
        print_status "Keine Änderungen in den Paketversionen"
    fi
}

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

    # Prüfe requirements Dateien
    if [ ! -f "requirements.txt" ] && [ ! -f "requirements-dev.txt" ]; then
        print_error "Keine requirements.txt oder requirements-dev.txt gefunden!"
        exit 1
    fi

    # Aktiviere virtuelle Umgebung
    print_status "Aktiviere virtuelle Umgebung..."
    source venv/bin/activate || {
        print_error "Fehler beim Aktivieren der virtuellen Umgebung!"
        exit 1
    }

    # Timestamp für Backups
    timestamp=$(date '+%Y%m%d_%H%M%S')

    # Pip Update
    print_header "Aktualisiere pip"
    pip install --upgrade pip || {
        print_error "Pip-Update fehlgeschlagen!"
        exit 1
    }

    # Update Produktionsabhängigkeiten
    update_requirements ""

    # Update Entwicklungsabhängigkeiten
    update_requirements "-dev"

    print_success "Update-Prozess erfolgreich abgeschlossen!"
}

# Starte Hauptprogramm
main "$@"
