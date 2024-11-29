"""HTML-Datei-Bearbeiter.

Dieses Skript bearbeitet HTML-Dateien, indem es Bildpfade für .eps- und .pdf-Dateien ersetzt.

Hauptfunktionalitäten:
1. Konfiguration über YAML-Datei
2. Multithreading für parallele Verarbeitung mehrerer Dateien
3. Ersetzen von Bildpfaden in HTML-Dateien
4. Umfangreiche Fehlerbehandlung und Logging

Hauptfunktionen:
- load_config: Lädt die Konfiguration aus einer YAML-Datei
- ersetze_in_datei: Ersetzt Bildpfade in einer einzelnen HTML-Datei
- bearbeite_dateien: Verarbeitet mehrere HTML-Dateien parallel
- main: Hauptfunktion zum Ausführen des Skripts

Verwendung:
    python html4_entfernen.py [--datei DATEINAME]

Args:
    --datei: Optionaler Name einer spezifischen HTML-Datei zur Bearbeitung (ohne .html-Endung)

Die Konfigurationsdatei sollte folgende Einstellungen enthalten:
- VERZEICHNIS: Pfad zum Verzeichnis mit den zu bearbeitenden HTML-Dateien

Voraussetzungen:
- PyYAML muss installiert sein
- tqdm muss installiert sein für den Fortschrittsbalken

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import glob
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

import yaml
from tqdm import tqdm

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_config(config_path: str) -> dict[str, str]:
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            # Typisiertes Dictionary erstellen
            result: dict[str, str] = {}
            for key, value in config.items():
                if isinstance(value, str):
                    result[key] = value
            return result
    except FileNotFoundError:
        logging.error(f"Konfigurationsdatei nicht gefunden: {config_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Fehler beim Lesen der Konfigurationsdatei: {e}")
        raise


# Debug-Ausgaben
print("Aktuelles Arbeitsverzeichnis:", os.getcwd())
print("Skript-Verzeichnis:", os.path.dirname(__file__))

# Lade Konfiguration aus YAML-Datei
config_path = os.path.join(os.path.dirname(__file__), "config4.yaml")
config = load_config(config_path)

VERZEICHNIS_PFAD = config["VERZEICHNIS"]
SUCH_MUSTER_EPS = r'src="images/(.*?)\.eps"'
SUCH_MUSTER_PDF = r'src="images/(.*?)\.pdf"'
ERSETZ_MUSTER_EPS = r'src="./images/\1.svg"'
ERSETZ_MUSTER_PDF = r'src="./images/\1.webp"'


def ersetze_in_datei(html_pfad: str) -> bool:
    """
    Ersetzt alle Vorkommen des Suchmusters durch das Ersetzungsmuster in einer .html-Datei.

    :param html_pfad: Pfad zur HTML-Datei
    :return: True wenn erfolgreich, False sonst
    """
    try:
        with open(html_pfad, "r", encoding="utf-8") as datei:
            inhalt = datei.read()

        # Ersetzen von .eps und .pdf Referenzen
        inhalt = re.sub(SUCH_MUSTER_EPS, ERSETZ_MUSTER_EPS, inhalt)
        inhalt = re.sub(SUCH_MUSTER_PDF, ERSETZ_MUSTER_PDF, inhalt)

        with open(html_pfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)

        logging.info(f"Datei {html_pfad} erfolgreich bearbeitet.")
        return True
    except IOError as e:
        logging.error(f"Fehler beim Bearbeiten der Datei {html_pfad}: {e}")
        return False


def bearbeite_dateien(spezifische_datei: Optional[str] = None) -> List[str]:
    """
    Bearbeitet .html-Dateien im angegebenen Verzeichnis oder eine spezifische Datei.

    :param spezifische_datei: Name der spezifischen Datei (ohne .html-Endung), falls vorhanden
    :return: Liste der erfolgreich bearbeiteten Dateien
    """
    dateien = (
        [os.path.join(VERZEICHNIS_PFAD, spezifische_datei + ".html")]
        if spezifische_datei
        else list(glob.iglob(os.path.join(VERZEICHNIS_PFAD, "*.html")))
    )

    erfolgreich_bearbeitet = []
    with ThreadPoolExecutor() as executor:
        ergebnisse = list(
            tqdm(
                executor.map(ersetze_in_datei, dateien),
                total=len(dateien),
                desc="Dateien bearbeitet",
            )
        )

    erfolgreich_bearbeitet = [datei for datei, erfolg in zip(dateien, ergebnisse) if erfolg]
    return erfolgreich_bearbeitet


def main() -> None:
    """Hauptfunktion, die andere Funktionen in der richtigen Reihenfolge aufruft."""
    parser = argparse.ArgumentParser(description="Bearbeitet HTML-Dateien.")
    parser.add_argument(
        "--datei",
        help="Name der spezifischen .html-Datei, die bearbeitet werden soll. Ohne .html-Endung.",
    )
    args = parser.parse_args()

    if args.datei and (not args.datei.isalnum() or ".." in args.datei or "/" in args.datei):
        logging.error(
            "Ungültiger Dateiname. Bitte geben Sie einen sicheren Dateinamen ohne Pfadangaben an."
        )
        return

    erfolgreich = bearbeite_dateien(args.datei)
    logging.info(f"Verarbeitung abgeschlossen. {len(erfolgreich)} Dateien erfolgreich bearbeitet.")


if __name__ == "__main__":
    main()
