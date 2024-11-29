"""Navigation Generator für HTML-Dateien.

Dieses Skript erstellt eine Navigationsseite für HTML-Dateien unter Verwendung von Jinja2-Templates.

Hauptfunktionalitäten:
1. Konfiguration über YAML-Datei
2. Suche nach HTML-Dateien in einem spezifizierten Ordner
3. Generierung einer Navigationsseite mit Links zu allen gefundenen HTML-Dateien
4. Verwendung von Jinja2-Templates für die Erstellung der Navigationsseite

Hauptkomponenten:
- NavigationConfig: Verwaltet die Konfigurationseinstellungen
- NavigationGenerator: Führt die Erstellung der Navigationsseite durch

Verwendung:
    python html2_dateien_verarbeiten.py [--config PFAD_ZUR_CONFIG]

Args:
    --config: Optionaler Pfad zur Konfigurationsdatei (Standard: config3.yaml im Skriptverzeichnis)

Die Konfigurationsdatei sollte folgende Einstellungen enthalten:
- ORDNERPFAD: Pfad zum Ordner mit HTML-Dateien
- VORLAGENPFAD: Pfad zum Ordner mit Jinja2-Templates
- VORLAGENNAME: Name der zu verwendenden Jinja2-Vorlage
- AUSGABE_DATEINAME: Name der zu erstellenden Navigationsseite

Voraussetzungen:
- Jinja2 muss installiert sein

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import logging
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader, Template
from jinja2 import exceptions as jinja2_exceptions

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class NavigationConfig:
    """Konfiguration für den Navigations-Generator."""

    ordnerpfad: Path
    vorlagenpfad: Path
    vorlagenname: str
    ausgabe_datei: Path

    @classmethod
    def from_yaml(cls, config_path: Path) -> "NavigationConfig":
        """Erstellt eine Konfiguration aus einer YAML-Datei.

        Args:
            config_path: Pfad zur YAML-Konfigurationsdatei

        Returns:
            NavigationConfig: Konfigurationsobjekt

        Raises:
            FileNotFoundError: Wenn die Konfigurationsdatei nicht existiert
            yaml.YAMLError: Bei Fehlern beim Parsen der YAML-Datei
            KeyError: Wenn erforderliche Konfigurationsschlüssel fehlen
        """
        try:
            config_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            script_dir = Path(__file__).parent

            return cls(
                ordnerpfad=script_dir / config_data["ORDNERPFAD"],
                vorlagenpfad=script_dir / config_data["VORLAGENPFAD"],
                vorlagenname=config_data["VORLAGENNAME"],
                ausgabe_datei=script_dir / config_data["AUSGABE_DATEINAME"],
            )
        except FileNotFoundError:
            logging.error("Konfigurationsdatei nicht gefunden: %s", config_path)
            raise
        except yaml.YAMLError as e:
            logging.error("Fehler beim Lesen der Konfigurationsdatei: %s", e)
            raise
        except KeyError as e:
            logging.error("Fehlender Konfigurationsschlüssel: %s", e)
            raise


class NavigationGenerator:
    """Generator für HTML-Navigationsseiten."""

    def __init__(self, config: NavigationConfig):
        """Initialisiert den Generator mit der Konfiguration."""
        self.config = config

    def finde_html_dateien(self) -> List[str]:
        """Findet alle HTML-Dateien im konfigurierten Ordner.

        Returns:
            List[str]: Liste der gefundenen HTML-Dateinamen

        Raises:
            FileNotFoundError: Wenn der konfigurierte Ordner nicht existiert
        """
        try:
            return sorted(f.name for f in self.config.ordnerpfad.glob("*.html"))
        except FileNotFoundError:
            logging.error("Ordner nicht gefunden: %s", self.config.ordnerpfad)
            raise

    def lade_template(self) -> Optional[Template]:
        """Lädt das Jinja2-Template.

        Returns:
            Optional[Template]: Das geladene Template oder None bei Fehler
        """
        try:
            env = Environment(loader=FileSystemLoader(self.config.vorlagenpfad))
            return env.get_template(self.config.vorlagenname)
        except jinja2_exceptions.TemplateNotFound:
            logging.error(
                "Vorlagendatei nicht gefunden: %s",
                self.config.vorlagenname,
            )
            return None

    def erstelle_navigationsseite(self) -> bool:
        """Erstellt die Navigationsseite.

        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        dateinamen = self.finde_html_dateien()
        if not dateinamen:
            logging.warning("Keine HTML-Dateien gefunden.")
            return False

        # HTML-Escape für alle Dateinamen
        dateinamen = [escape(name) for name in dateinamen]

        template = self.lade_template()
        if not template:
            return False

        try:
            inhalt = template.render(dateinamen=dateinamen)
            self.config.ausgabe_datei.write_text(inhalt, encoding="utf-8")

            logging.info(
                "Navigationsseite erfolgreich erstellt: %s (%d Links)",
                self.config.ausgabe_datei,
                len(dateinamen),
            )
            return True

        except OSError as e:
            logging.error("Fehler beim Schreiben der Ausgabedatei: %s", e)
            return False


def parse_args() -> argparse.Namespace:
    """Verarbeitet die Kommandozeilenargumente.

    Returns:
        argparse.Namespace: Verarbeitete Argumente
    """
    parser = argparse.ArgumentParser(
        description="Erstellt eine Navigationsseite für HTML-Dateien.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).parent / "config3.yaml",
        help="Pfad zur Konfigurationsdatei",
    )
    return parser.parse_args()


def main() -> None:
    """Hauptfunktion zum Erstellen der Navigationsseite."""
    args = parse_args()
    script_dir = Path(__file__).parent

    logging.info("Skript-Verzeichnis: %s", script_dir)
    logging.info("Konfigurationsdatei: %s", args.config)

    try:
        config = NavigationConfig.from_yaml(args.config)
        generator = NavigationGenerator(config)

        if not generator.erstelle_navigationsseite():
            logging.error("Navigation konnte nicht erstellt werden.")
            return

    except Exception as e:
        logging.error("Fehler bei der Verarbeitung: %s", e)
        raise


if __name__ == "__main__":
    main()
