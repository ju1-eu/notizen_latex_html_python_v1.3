"""Navigation Generator für HTML-Dateien.

Dieses Skript erstellt eine Navigationsseite für HTML-Dateien unter Verwendung von Jinja2-Templates.

Hauptfunktionalitäten:
1. Konfiguration über YAML-Datei
2. Suche nach HTML-Dateien in einem spezifizierten Ordner
3. Generierung einer Navigationsseite mit Links zu allen gefundenen HTML-Dateien
4. Verwendung von Jinja2-Templates für die Erstellung der Navigationsseite

Hauptfunktionen:
- load_config: Lädt die Konfiguration aus einer YAML-Datei
- finde_html_dateien: Sucht nach HTML-Dateien in einem Ordner
- erstelle_navigationsseite: Erstellt die Navigationsseite mit Jinja2
- main: Hauptfunktion zum Ausführen des Skripts

Verwendung:
    python html3_navigation.py [--config PFAD_ZUR_CONFIG]

Args:
    --config: Optionaler Pfad zur Konfigurationsdatei (Standard: config3.yaml im Skriptverzeichnis)

Die Konfigurationsdatei sollte folgende Einstellungen enthalten:
- ORDNERPFAD: Pfad zum Ordner mit HTML-Dateien
- VORLAGENPFAD: Pfad zum Ordner mit Jinja2-Templates
- VORLAGENNAME: Name der zu verwendenden Jinja2-Vorlage
- AUSGABE_DATEINAME: Name der zu erstellenden Navigationsseite

Voraussetzungen:
- Jinja2 muss installiert sein
- PyYAML muss installiert sein

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import logging
import os
from html import escape

import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2 import exceptions as jinja2_exceptions

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_config(config_path: str) -> dict[str, str]:
    """
    Lädt die Konfiguration aus einer YAML-Datei.

    Args:
        config_path: Pfad zur Konfigurationsdatei

    Returns:
        dict[str, str]: Die geladene Konfiguration mit String-Werten

    Raises:
        FileNotFoundError: Wenn die Konfigurationsdatei nicht gefunden wird
        yaml.YAMLError: Wenn die YAML-Datei nicht korrekt formatiert ist
    """
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
        logging.error("Konfigurationsdatei nicht gefunden: %s", config_path)
        raise
    except yaml.YAMLError as e:
        logging.error("Fehler beim Lesen der Konfigurationsdatei: %s", e)
        raise


def finde_html_dateien(ordnerpfad: str) -> list[str]:
    """
    Durchläuft den angegebenen Ordner und findet alle HTML-Dateien.

    Args:
        ordnerpfad: Pfad zum zu durchsuchenden Ordner

    Returns:
        list[str]: Liste der gefundenen HTML-Dateinamen

    Raises:
        FileNotFoundError: Wenn der angegebene Ordner nicht gefunden wird
    """
    try:
        return [dateiname for dateiname in os.listdir(ordnerpfad) if dateiname.endswith(".html")]
    except FileNotFoundError:
        logging.error("Ordner nicht gefunden: %s", ordnerpfad)
        raise


def erstelle_navigationsseite(
    ordnerpfad: str, vorlagenpfad: str, vorlagenname: str, ausgabe_dateiname: str
) -> None:
    """
    Verwendet HTML-Dateien und eine Jinja2-Vorlage, um die Navigationsseite zu erstellen.

    Args:
        ordnerpfad: Pfad zum Ordner mit HTML-Dateien
        vorlagenpfad: Pfad zu den Jinja2-Vorlagen
        vorlagenname: Name der zu verwendenden Vorlage
        ausgabe_dateiname: Name der zu erstellenden Ausgabedatei
    """
    dateinamen = finde_html_dateien(ordnerpfad)

    if not dateinamen:
        logging.warning("Keine HTML-Dateien gefunden.")
        return

    dateinamen = [escape(dateiname) for dateiname in sorted(dateinamen)]

    try:
        env = Environment(loader=FileSystemLoader(vorlagenpfad))
        vorlage = env.get_template(vorlagenname)
    except jinja2_exceptions.TemplateNotFound:
        logging.error("Vorlagendatei nicht gefunden: %s", vorlagenname)
        return

    try:
        with open(ausgabe_dateiname, "w", encoding="utf-8") as nav_file:
            nav_file.write(vorlage.render(dateinamen=dateinamen))
        logging.info(
            "Die Datei '%s' wurde erfolgreich mit %d Links erstellt.",
            ausgabe_dateiname,
            len(dateinamen),
        )
    except IOError as e:
        logging.error("Fehler beim Schreiben der Ausgabedatei: %s", e)


def main() -> None:
    """Hauptfunktion zum Erstellen der Navigationsseite.

    Definiert die Pfade und Namen für Ordner, Vorlage und Ausgabedatei.
    """
    parser = argparse.ArgumentParser(description="Erstellt eine Navigationsseite für HTML-Dateien.")
    parser.add_argument("--config", default="config3.yaml", help="Pfad zur Konfigurationsdatei")
    args = parser.parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, args.config)

    logging.info("Aktuelles Arbeitsverzeichnis: %s", os.getcwd())
    logging.info("Skript-Verzeichnis: %s", script_dir)
    logging.info("Konfigurationspfad: %s", config_path)

    try:
        config = load_config(config_path)
    except Exception as e:
        logging.error("Fehler beim Laden der Konfiguration: %s", e)
        return

    ordnerpfad = os.path.join(script_dir, config["ORDNERPFAD"])
    vorlagenpfad = os.path.join(script_dir, config["VORLAGENPFAD"])
    vorlagenname = config["VORLAGENNAME"]
    ausgabe_dateiname = os.path.join(script_dir, config["AUSGABE_DATEINAME"])

    logging.info("Verwendete Pfade:")
    logging.info("Ordnerpfad: %s", ordnerpfad)
    logging.info("Vorlagenpfad: %s", vorlagenpfad)
    logging.info("Ausgabe-Dateiname: %s", ausgabe_dateiname)

    erstelle_navigationsseite(ordnerpfad, vorlagenpfad, vorlagenname, ausgabe_dateiname)


if __name__ == "__main__":
    main()
