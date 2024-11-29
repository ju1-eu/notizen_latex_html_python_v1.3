"""LaTeX Konvertierung.

Dieses Modul konvertiert Markdown-Dateien zu LaTeX unter Verwendung von Pandoc.

Hauptfunktionalitäten:
1. Konfiguration über eine Config-Klasse
2. Konvertierung von Markdown zu LaTeX mit Pandoc
3. Unterstützung für benutzerdefinierte Vorlagen und Filter
4. Multithreading für parallele Verarbeitung mehrerer Dateien

Hauptkomponenten:
- Config: Dataclass für die Konfiguration der Konvertierung
- MarkdownConverter: Klasse zur Konvertierung von Markdown zu LaTeX

Verwendung:
    python latex_convert1.py

Die Konfiguration enthält:
- quellpfad: Pfad zum Ordner mit Markdown-Dateien
- zielpfad: Pfad zum Ausgabeordner für LaTeX-Dateien
- vorlagepfad: Pfad zur LaTeX-Vorlagendatei
- filterpfad: Pfad zur Lua-Filterdatei

Voraussetzungen:
- Pandoc muss auf dem System installiert sein

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class Config:
    """Konfigurationsklasse für die Konvertierung."""

    quellpfad: Path = Path("./md")
    zielpfad: Path = Path("./tex")
    vorlagepfad: Path = Path("content/vorlage-main.tex")
    filterpfad: Path = Path("content/combined-filter.lua")


class MarkdownConverter:
    """Klasse zur Konvertierung von Markdown zu LaTeX."""

    def __init__(self, config: Config):
        """Initialisiert den MarkdownConverter."""
        self.config = config

    def ist_pandoc_installiert(self) -> bool:
        """Prüft, ob Pandoc auf dem System installiert ist."""
        try:
            subprocess.run(
                ["pandoc", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            logging.error("Pandoc konnte nicht ausgeführt werden")
            return False
        except FileNotFoundError:
            logging.error("Pandoc ist nicht installiert")
            return False

    def extrahiere_thema(self, dateiname: str) -> str:
        """Extrahiert das Thema aus dem Dateinamen.

        Args:
            dateiname: Name der Datei

        Returns:
            str: Extrahiertes Thema (Dateiname ohne Erweiterung)
        """
        return Path(dateiname).stem

    def konvertiere_datei(self, md_pfad: Path, tex_pfad: Path) -> None:
        """Konvertiert eine einzelne .md-Datei in .tex.

        Args:
            md_pfad: Pfad zur Markdown-Datei
            tex_pfad: Pfad zur Ziel-LaTeX-Datei
        """
        thema = self.extrahiere_thema(str(md_pfad))

        try:
            cmd = [
                "pandoc",
                str(md_pfad),
                "--to",
                "latex",
                "--output",
                str(tex_pfad),
                "--template",
                str(self.config.vorlagepfad),
                "--lua-filter",
                str(self.config.filterpfad),
                "--variable",
                f"title:{thema}",
                "--listings",
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            logging.info("Erfolgreich konvertiert: %s", md_pfad)
        except subprocess.CalledProcessError as e:
            logging.error(
                "Fehler bei der Konvertierung von %s:\n%s",
                md_pfad,
                e.stderr.decode(),
            )

    def finde_markdown_dateien(self, dateiname: Optional[str] = None) -> List[Path]:
        """Findet alle zu konvertierenden Markdown-Dateien.

        Args:
            dateiname: Optional, spezifische Datei die konvertiert werden soll

        Returns:
            List[Path]: Liste der gefundenen Markdown-Dateien
        """
        if dateiname:
            if not dateiname.endswith(".md"):
                logging.error("Ungültige Dateiendung: %s", dateiname)
                return []
            return [self.config.quellpfad / dateiname]

        return list(self.config.quellpfad.glob("*.md"))

    def konvertiere_dateien(self, dateiname: Optional[str] = None) -> None:
        """Konvertiert ausgewählte oder alle Markdown-Dateien zu LaTeX.

        Args:
            dateiname: Optional, spezifische Datei die konvertiert werden soll
        """
        if not self._prüfe_pfade():
            return

        md_dateien = self.finde_markdown_dateien(dateiname)
        if not md_dateien:
            logging.warning("Keine Markdown-Dateien gefunden")
            return

        for md_datei in md_dateien:
            if not md_datei.exists():
                logging.warning("Datei existiert nicht: %s", md_datei)
                continue

            tex_datei = self.config.zielpfad / f"{md_datei.stem}.tex"
            self.konvertiere_datei(md_datei, tex_datei)

        logging.info("Konvertierung abgeschlossen")

    def _prüfe_pfade(self) -> bool:
        """Prüft, ob alle notwendigen Pfade existieren.

        Returns:
            bool: True wenn alle Pfade valide sind, sonst False
        """
        if not self.config.quellpfad.exists():
            logging.error("Quellordner existiert nicht: %s", self.config.quellpfad)
            return False

        if not self.config.vorlagepfad.exists():
            logging.error("Vorlage existiert nicht: %s", self.config.vorlagepfad)
            return False

        if not self.config.zielpfad.exists():
            self.config.zielpfad.mkdir(parents=True)
            logging.info("Zielordner erstellt: %s", self.config.zielpfad)

        return True


def main() -> None:
    """Hauptfunktion des Skripts."""
    config = Config()
    converter = MarkdownConverter(config)

    if not converter.ist_pandoc_installiert():
        logging.error(
            "Pandoc ist nicht installiert. " "Bitte installieren Sie Pandoc, um fortzufahren."
        )
        return

    converter.konvertiere_dateien()


if __name__ == "__main__":
    main()
