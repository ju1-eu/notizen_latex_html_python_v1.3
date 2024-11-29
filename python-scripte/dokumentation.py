"""Dokumentationsextraktor für Python-Skripte.

Dieses Skript extrahiert Docstrings aus Python-Dateien und generiert daraus Markdown-Dokumentation.

Hauptfunktionalitäten:
1. Extraktion von Docstrings aus Python-Dateien
2. Generierung von Markdown-Dokumentation aus extrahierten Docstrings
3. Verarbeitung mehrerer Python-Dateien in einem Verzeichnis
4. Erstellung von Statistiken über die Verarbeitung

Hauptkomponenten:
- DocExtractorConfig: Dataclass für die Konfiguration des Extraktors
- DocExtractor: Klasse zur Extraktion und Verarbeitung von Docstrings

Verwendung:
    python dokumentation.py

Die Konfiguration enthält:
- quell_verzeichnis: Pfad zum Quellverzeichnis mit Python-Dateien
- markdown_template: Template für die generierte Markdown-Dokumentation

Voraussetzungen:
- Python 3.x mit Unterstützung für Dataclasses

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class DocExtractorConfig:
    """Konfiguration für die Dokumentationsextraktion."""

    quell_verzeichnis: Path
    markdown_template: str = "# Beschreibung\n\n{beschreibung}\n\n"


class DocExtractor:
    """Extraktor für Python-Dokumentation."""

    def __init__(self, config: DocExtractorConfig):
        """Initialisiert den Extraktor."""
        self.config = config

    def extrahiere_beschreibung(self, skript_pfad: Path) -> Optional[str]:
        """Extrahiert die Docstring-Beschreibung aus einer Python-Datei.

        Args:
            skript_pfad: Pfad zur Python-Datei

        Returns:
            Optional[str]: Extrahierte Beschreibung oder None bei Fehler
        """
        try:
            inhalt = skript_pfad.read_text(encoding="utf-8")
            start_index = inhalt.find('"""') + 3
            end_index = inhalt.find('"""', start_index)

            if start_index == 2 or end_index == -1:
                logging.warning("Keine Beschreibung in %s gefunden", skript_pfad)
                return None

            return inhalt[start_index:end_index].strip()

        except Exception as e:
            logging.error("Fehler beim Lesen von %s: %s", skript_pfad, e)
            return None

    def generiere_markdown(self, skript_pfad: Path, beschreibung: str) -> Optional[Path]:
        """Generiert eine Markdown-Datei aus der Skriptbeschreibung.

        Args:
            skript_pfad: Pfad zur Python-Datei
            beschreibung: Extrahierte Beschreibung

        Returns:
            Optional[Path]: Pfad zur generierten Markdown-Datei oder None bei Fehler
        """
        md_pfad = skript_pfad.with_suffix(".md")
        md_inhalt = self.config.markdown_template.format(beschreibung=beschreibung)

        try:
            md_pfad.write_text(md_inhalt, encoding="utf-8")
            logging.info("Markdown-Datei erstellt: %s", md_pfad)
            return md_pfad
        except Exception as e:
            logging.error("Fehler beim Schreiben von %s: %s", md_pfad, e)
            return None

    def verarbeite_verzeichnis(self) -> Dict[Path, Optional[Path]]:
        """Verarbeitet alle Python-Dateien im konfigurierten Verzeichnis.

        Returns:
            Dict[Path, Optional[Path]]: Mapping von Python-Dateien zu generierten
            Markdown-Dateien
        """
        if not self.config.quell_verzeichnis.is_dir():
            logging.error("Verzeichnis nicht gefunden: %s", self.config.quell_verzeichnis)
            return {}

        ergebnisse: Dict[Path, Optional[Path]] = {}
        python_dateien = self.config.quell_verzeichnis.glob("*.py")

        for skript_pfad in python_dateien:
            beschreibung = self.extrahiere_beschreibung(skript_pfad)
            if beschreibung:
                md_pfad = self.generiere_markdown(skript_pfad, beschreibung)
                ergebnisse[skript_pfad] = md_pfad
            else:
                ergebnisse[skript_pfad] = None

        return ergebnisse

    def zeige_statistik(self, ergebnisse: Dict[Path, Optional[Path]]) -> None:
        """Zeigt Statistiken über die Verarbeitung.

        Args:
            ergebnisse: Mapping von Python-Dateien zu generierten Markdown-Dateien
        """
        gesamt = len(ergebnisse)
        erfolgreich = sum(1 for md_pfad in ergebnisse.values() if md_pfad is not None)
        fehlgeschlagen = gesamt - erfolgreich

        logging.info("Verarbeitung abgeschlossen:")
        logging.info("  Gefundene Python-Dateien: %d", gesamt)
        logging.info("  Erfolgreich verarbeitet: %d", erfolgreich)
        logging.info("  Fehlgeschlagen: %d", fehlgeschlagen)


def main() -> None:
    """Hauptfunktion des Skripts."""
    skript_verzeichnis = Path(__file__).parent / "python-scripte"
    config = DocExtractorConfig(quell_verzeichnis=skript_verzeichnis)

    try:
        extraktor = DocExtractor(config)
        ergebnisse = extraktor.verarbeite_verzeichnis()
        extraktor.zeige_statistik(ergebnisse)

    except Exception as e:
        logging.error("Unerwarteter Fehler: %s", e)
        raise


if __name__ == "__main__":
    main()
