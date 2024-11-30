"""HTML Konverter mit Pandoc.

Dieses Skript konvertiert Markdown-Dateien zu HTML unter Verwendung von Pandoc.
Es bietet folgende Hauptfunktionalitäten:

1. Konfiguration über YAML-Datei
2. Multithreading für parallele Verarbeitung
3. Unterstützung für Zitierungen und CSS-Styling
4. Umfangreiche Fehlerbehandlung und Logging

Hauptkomponenten:
- PandocConfig: Verwaltet die Konfigurationseinstellungen
- PandocConverter: Führt die Konvertierung durch

Verwendung:
    python html1_konverter_pandoc.py [--config PFAD_ZUR_CONFIG] [--version]

Args:
    --config: Optionaler Pfad zur Konfigurationsdatei (Standard: config1.yaml im Skriptverzeichnis)
    --version: Zeigt die Versionsnummer des Skripts an

Die Konfigurationsdatei sollte folgende Einstellungen enthalten:
- QUELL_ORDNER: Pfad zum Ordner mit Markdown-Dateien
- ZIEL_ORDNER: Pfad zum Ausgabeordner für HTML-Dateien
- ERWEITERUNG: Dateierweiterung der Markdown-Dateien (z.B. ".md")
- CSL_DATEI: Pfad zur CSL-Datei für Zitierungsstile
- CSS_DATEI: Pfad zur CSS-Datei für Styling
- bib_dateien: Liste der Pfade zu Bibliografie-Dateien

Voraussetzungen:
- Pandoc muss auf dem System installiert sein

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml

# Versionsinformation
__version__ = "1.0"

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class PandocConfig:
    """Konfiguration für die Pandoc-Konvertierung."""

    quell_ordner: Path = field(default_factory=lambda: Path("./md"))
    ziel_ordner: Path = field(default_factory=lambda: Path("./html"))
    erweiterung: str = ".md"
    csl_datei: Path = field(default_factory=lambda: Path("ieee.csl"))
    css_datei: Path = field(default_factory=lambda: Path("style.css"))
    vorlage: Path = field(default_factory=lambda: Path("vorlage-main.html"))  # NEU
    bib_dateien: List[Path] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, config_path: Path) -> "PandocConfig":
        """Lädt die Konfiguration aus einer YAML-Datei.

        Args:
            config_path: Pfad zur YAML-Konfigurationsdatei

        Returns:
            PandocConfig: Konfigurationsobjekt

        Raises:
            FileNotFoundError: Wenn die Konfigurationsdatei nicht existiert
            yaml.YAMLError: Bei Fehlern beim Parsen der YAML-Datei
        """
        try:
            with config_path.open("r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            return cls(
                quell_ordner=Path(config_data["QUELL_ORDNER"]),
                ziel_ordner=Path(config_data["ZIEL_ORDNER"]),
                erweiterung=config_data["ERWEITERUNG"],
                csl_datei=Path(config_data["CSL_DATEI"]),
                css_datei=Path(config_data["CSS_DATEI"]),
                vorlage=Path(config_data["VORLAGE"]),  # VORLAGE fehlte
                bib_dateien=[Path(bib) for bib in config_data["bib_dateien"]],
            )
        except FileNotFoundError:
            logging.error("Konfigurationsdatei nicht gefunden: %s", config_path)
            raise
        except yaml.YAMLError as e:
            logging.error("Fehler beim Lesen der Konfigurationsdatei: %s", e)
            raise

    def validate(self) -> None:
        """Überprüft die Vollständigkeit und Gültigkeit der Konfiguration.

        Raises:
            ValueError: Wenn erforderliche Konfigurationsschlüssel fehlen
        """
        required_files = [self.csl_datei] + self.bib_dateien
        for file_path in required_files:
            if not file_path.is_file():
                logging.warning("Datei nicht gefunden: %s", file_path)


class PandocConverter:
    """Klasse für die Konvertierung von Markdown zu HTML mit Pandoc."""

    def __init__(self, config: PandocConfig):
        """Initialisiert den Konverter mit der Konfiguration."""
        self.config = config

    def pandoc_ist_installiert(self) -> bool:
        """Überprüft, ob Pandoc installiert ist.

        Returns:
            bool: True wenn Pandoc installiert ist, sonst False
        """
        try:
            import subprocess

            subprocess.run(
                ["pandoc", "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _get_pandoc_command(self, quelle: Path, ziel: Path) -> List[str]:
        """Erstellt das Pandoc-Kommando.

        Args:
            quelle: Quelldatei
            ziel: Zieldatei

        Returns:
            List[str]: Pandoc-Kommando als Liste
        """
        cmd = [
            "pandoc",
            str(quelle),
            "-o",
            str(ziel),
            "--template",
            str(self.config.vorlage),
            "-c",
            str(self.config.css_datei),  # CSS hinzufügen
            "--csl",
            str(self.config.csl_datei),
            "--mathjax",
            "--citeproc",
        ]

        for bib in self.config.bib_dateien:
            cmd.extend(["--bibliography", str(bib)])

        return cmd

    def _verarbeite_datei(self, datei: Path) -> None:
        """Konvertiert eine einzelne Datei von Markdown zu HTML.

        Args:
            datei: Zu konvertierende Datei
        """
        if not datei.suffix == self.config.erweiterung:
            return

        ziel_datei = self.config.ziel_ordner / f"{datei.stem}.html"

        try:
            import subprocess

            cmd = self._get_pandoc_command(datei, ziel_datei)
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logging.info("Erfolgreich konvertiert: %s", datei.name)
        except subprocess.CalledProcessError as e:
            logging.error(
                "Fehler beim Konvertieren von '%s':\n%s",
                datei.name,
                e.stderr,
            )

    def konvertiere_alle(self) -> None:
        """Konvertiert alle Markdown-Dateien im Quellverzeichnis."""
        if not self.pandoc_ist_installiert():
            logging.error(
                "Pandoc ist nicht installiert. " "Bitte installieren Sie Pandoc auf Ihrem System."
            )
            return

        self.config.ziel_ordner.mkdir(parents=True, exist_ok=True)

        dateien = list(self.config.quell_ordner.glob(f"*{self.config.erweiterung}"))
        if not dateien:
            logging.warning(
                "Keine %s-Dateien in %s gefunden.",
                self.config.erweiterung,
                self.config.quell_ordner,
            )
            return

        with ThreadPoolExecutor() as executor:
            for i, _ in enumerate(executor.map(self._verarbeite_datei, dateien), 1):
                logging.info("Fortschritt: %d/%d Dateien verarbeitet", i, len(dateien))

        logging.info("Konvertierung abgeschlossen.")


def parse_args() -> argparse.Namespace:
    """Verarbeitet die Kommandozeilenargumente.

    Returns:
        argparse.Namespace: Verarbeitete Argumente
    """
    parser = argparse.ArgumentParser(
        description="Konvertiert Markdown-Dateien zu HTML mit Pandoc.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).parent / "config1.yaml",
        help="Pfad zur Konfigurationsdatei",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()


def main() -> None:
    """Hauptfunktion des Skripts."""
    args = parse_args()
    logging.info("Skript-Verzeichnis: %s", Path(__file__).parent)
    logging.info("Konfigurationsdatei: %s", args.config)

    try:
        config = PandocConfig.from_yaml(args.config)
        config.validate()

        converter = PandocConverter(config)
        converter.konvertiere_alle()

    except Exception as e:
        logging.error("Ein unerwarteter Fehler ist aufgetreten: %s", e)
        raise


if __name__ == "__main__":
    main()
