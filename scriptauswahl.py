"""Interaktives Skript zur Ausführung verschiedener Befehle.

Skript bietet ein Menü zur Auswahl und Ausführung von Befehlen für LaTeX und HTML.

Hauptfunktionalitäten:
1. Konfiguration über YAML-Datei
2. Interaktives Menü zur Befehlsauswahl
3. Ausführung von LaTeX-bezogenen Befehlen
4. Ausführung von HTML-bezogenen Befehlen
5. Kombinierte Verarbeitungssequenzen für LaTeX und HTML

Hauptkomponenten:
- load_config: Lädt die Konfiguration aus einer YAML-Datei
- sicherer_aufruf: Führt Befehle sicher aus und behandelt Fehler
- zeige_menue_und_waehle: Zeigt das Menü und verarbeitet die Benutzerauswahl
- kombinierte_latex_verarbeitung: Führt eine Sequenz von LaTeX-Befehlen aus
- kombinierte_html_verarbeitung: Führt eine Sequenz von HTML-Befehlen aus

Verwendung:
    python scriptauswahl.py [--config PFAD_ZUR_CONFIG]

Args:
    --config: Optionaler Pfad zur Konfigurationsdatei (Standard: config.yaml)

Die Konfigurationsdatei sollte Befehle für LaTeX- und HTML-Verarbeitung enthalten.

Voraussetzungen:
- Python 3.x
- PyYAML muss installiert sein
- Verschiedene Kommandozeilenwerkzeuge (abhängig von den konfigurierten Befehlen)

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import logging
import subprocess
from typing import Callable, Dict, List, Optional, Union

import yaml

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Definition des CommandType und BefehlsEintrag
CommandType = Union[Callable[[], None], List[str]]
BefehlsEintrag = Dict[str, Union[str, CommandType]]


# Lade Konfiguration aus YAML-Datei
def load_config(config_path: str) -> dict[str, list[str]]:
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        # Typisiertes Dictionary erstellen
        result: dict[str, list[str]] = {}
        for key, value in config.items():
            if isinstance(value, list) and all(isinstance(x, str) for x in value):
                result[key] = value
        return result


CONFIG = load_config("config.yaml")

# Gruppierte Konstanten für Befehle
LATEX_COMMANDS = {
    "KONVERTIEREN": CONFIG["LATEX_KONVERTIEREN"],
    "ENTFERNEN": CONFIG["LATEX_ENTFERNEN"],
    "SUCHEN_ERSETZEN": CONFIG["LATEX_SUCHEN_ERSETZEN"],
    "SYNC_TEX_FILES": CONFIG["SYNC_TEX_FILES"],
}

MAKE_COMMANDS = {
    "DEFAULT": CONFIG["MAKE"],
    "XELATEX": CONFIG["MAKE_XELATEX"],
    "LUALATEX": CONFIG["MAKE_LUALATEX"],
    "CLEAN": CONFIG["MAKE_CLEAN"],
    "CLEAN_PDF": CONFIG["MAKE_CLEAN_PDF"],
}

HTML_COMMANDS = {
    "PANDOC": CONFIG["HTML_PANDOC"],
    "NAVIGATION": CONFIG["HTML_NAVIGATION"],
    "ENTFERNEN": CONFIG["HTML_ENTFERNEN"],
}


def kombinierte_html_verarbeitung() -> None:
    for befehl in [
        HTML_COMMANDS["PANDOC"],  # MD -> HTML mit Template
        HTML_COMMANDS["NAVIGATION"],  # Erstellt Navigation
        HTML_COMMANDS["ENTFERNEN"],  # Bildpfade korrigieren
    ]:
        if isinstance(befehl, list):
            sicherer_aufruf(befehl)


def sicherer_aufruf(befehl: List[str]) -> bool:
    """
    Führt einen Befehl sicher aus und fängt bekannte sowie unerwartete Fehler.

    Args:
        befehl (List[str]): Der auszuführende Befehl als Liste von Strings.

    Returns:
        bool: True, wenn der Befehl erfolgreich ausgeführt wurde, sonst False.
    """
    logging.info(f"Ausführender Befehl: {' '.join(befehl)}")
    try:
        subprocess.run(befehl, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Fehler beim Ausführen des Befehls: {e}")
    except FileNotFoundError as e:
        logging.error(f"Befehl nicht gefunden: {e}")
    except PermissionError as e:
        logging.error(f"Keine Berechtigung zur Ausführung des Befehls: {e}")
    except Exception as e:
        logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    return False


def zeige_menue_und_waehle() -> Optional[str]:
    """
    Zeigt das Menü und gibt die Auswahl des Benutzers zurück.

    Returns:
        Optional[str]: Die Auswahl des Benutzers oder None, wenn 'q' gewählt wurde.
    """
    print("\nBitte wählen Sie einen Befehl aus:\n")
    for key, value in BEFEHLE.items():
        print(f"{key}. {value['name']}")
    auswahl = input("\nGeben Sie die Nummer des gewünschten Befehls ein oder 'q' zum Beenden: ")
    return None if auswahl == "q" else auswahl


def pause() -> None:
    """Pausiert das Skript, bis der Benutzer fortfährt."""
    input("\nDrücken Sie Enter, um fortzufahren...")


def verarbeite_alle_tex_dateien() -> None:
    """Automatisierte Version zum Synchronisieren aller .tex-Dateien."""
    befehl = ["rsync", "-avh", "--progress", "tex/", "."]
    if sicherer_aufruf(befehl):
        logging.info("Alle .tex-Dateien wurden synchronisiert.")
    else:
        logging.error("Fehler beim Synchronisieren der .tex-Dateien.")


def kombinierte_latex_verarbeitung() -> None:
    """Führt die Schritte 1 bis 4 und 7 in einer Sequenz aus."""
    logging.info("Starte kombinierte LaTeX Verarbeitung...")
    schritte = [
        (LATEX_COMMANDS["KONVERTIEREN"], "LaTeX konvertieren"),
        (LATEX_COMMANDS["ENTFERNEN"], "LaTeX Code entfernen"),
        (LATEX_COMMANDS["SUCHEN_ERSETZEN"], "LaTeX Code suchen und ersetzen"),
        (verarbeite_alle_tex_dateien, "Synchronisiere .tex-Dateien"),
        (MAKE_COMMANDS["XELATEX"], "make xelatex"),
    ]

    for befehl, beschreibung in schritte:
        logging.info(f"Führe aus: {beschreibung}")
        if isinstance(befehl, list):
            if not sicherer_aufruf(befehl):
                logging.error(f"Fehler bei: {beschreibung}")
                return
        elif callable(befehl):
            befehl()
        else:
            logging.error(f"Ungültiger Befehlstyp für: {beschreibung}")
            return

    logging.info("Kombinierte LaTeX Verarbeitung abgeschlossen.")


def fuehre_befehl_aus(befehl: Union[List[str], Callable[[], None]]) -> None:
    """
    Führt einen Befehl basierend auf seinem Typ aus.

    Args:
        befehl: Der auszuführende Befehl (Funktion oder Liste von Strings)
    """
    if callable(befehl):
        befehl()
    elif isinstance(befehl, list):
        sicherer_aufruf(befehl)
    else:
        logging.error(f"Ungültiger Befehlstyp: {type(befehl)}")


BEFEHLE: Dict[str, BefehlsEintrag] = {
    "1": {"name": "LaTeX konvertieren", "command": LATEX_COMMANDS["KONVERTIEREN"]},
    "2": {
        "name": "LaTeX Code entfernen (Alle Dateien)",
        "command": LATEX_COMMANDS["ENTFERNEN"],
    },
    "3": {
        "name": "LaTeX Code Suchen und Ersetzen",
        "command": LATEX_COMMANDS["SUCHEN_ERSETZEN"],
    },
    "4": {
        "name": "Synchronisiere .tex-Dateien mit Auswahl einer Datei oder allen",
        "command": LATEX_COMMANDS["SYNC_TEX_FILES"],
    },
    "5": {
        "name": "Kombi Latex (Schritte 1-4+7)",
        "command": kombinierte_latex_verarbeitung,
    },
    "6": {"name": "make (# pdflatex)", "command": MAKE_COMMANDS["DEFAULT"]},
    "7": {"name": "make xelatex", "command": MAKE_COMMANDS["XELATEX"]},
    "8": {"name": "make lualatex", "command": MAKE_COMMANDS["LUALATEX"]},
    "9": {"name": "make clean - aufräumen ohne PDFs", "command": MAKE_COMMANDS["CLEAN"]},
    "10": {
        "name": "make clean-pdf - aufräumen mit PDFs",
        "command": MAKE_COMMANDS["CLEAN_PDF"],
    },
    "11": {
        "name": "Markdown in HTML Konvertierung mit Pandoc",
        "command": HTML_COMMANDS["PANDOC"],
    },
    "12": {
        "name": "Navigation über HTML Seiten erstellen",
        "command": HTML_COMMANDS["NAVIGATION"],
    },
    "13": {"name": "HTML Code entfernen", "command": HTML_COMMANDS["ENTFERNEN"]},
    "14": {
        "name": "Kombi HTML (Schritte 11-13)",
        "command": kombinierte_html_verarbeitung,
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interaktives Skript zur Ausführung verschiedener Befehle."
    )
    parser.add_argument("--config", default="config.yaml", help="Pfad zur Konfigurationsdatei")
    args = parser.parse_args()

    global CONFIG
    CONFIG = load_config(args.config)

    while True:
        auswahl = zeige_menue_und_waehle()
        if auswahl is None:
            break
        if auswahl in BEFEHLE:
            logging.info("\n" + "=" * 50)
            befehl = BEFEHLE[auswahl]["command"]
            if isinstance(befehl, list):
                sicherer_aufruf(befehl)
            elif callable(befehl):
                befehl()
            else:
                logging.error(f"Ungültiger Befehlstyp für Auswahl {auswahl}")
            logging.info("=" * 50)
            pause()
        else:
            logging.warning("Ungültige Auswahl. Bitte erneut versuchen.")


if __name__ == "__main__":
    main()
