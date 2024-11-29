"""Verzeichnis-Inhaltsverzeichnis-Generator.

Skript erstellt ein HTML-basiertes Inhaltsverzeichnis für verschiedene Dateitypen.

Hauptfunktionalitäten:
1. Konvertierung von Markdown und Code-Dateien in HTML
2. Kopieren von PDF-Dateien
3. Erstellung eines HTML-Inhaltsverzeichnisses für alle verarbeiteten Dateien

Hauptkomponenten:
- Config: Dataclass für die Konfiguration des Generators
- VerzeichnisKonverter: Klasse zur Konvertierung und Verarbeitung von Verzeichnissen

Verwendung:
    python dateien_inhaltsverzeichnis.py

Die Konfiguration enthält:
- quellverzeichnis: Pfad zum Quellverzeichnis (Standard: ./md)
- zielverzeichnis: Pfad zum Zielverzeichnis (Standard: ./INHALTSVERZEICHNIS)
- pygments_css: Name der Pygments CSS-Datei für Code-Hervorhebung
- custom_css: Name der benutzerdefinierten CSS-Datei
- sprachoptionen: Dictionary mit Dateiendungen und zugehörigen Programmiersprachen

Unterstützte Dateitypen:
- Markdown (.md)
- Python (.py)
- PHP (.php)
- JavaScript (.js)
- C (.c)
- C++ (.cc)
- PDF (.pdf)

Voraussetzungen:
- Pandoc muss installiert sein für Markdown-Konvertierung
- Pygments muss installiert sein für Code-Hervorhebung

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import logging
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class Config:
    """Konfigurationsklasse für den Verzeichniskonverter."""

    quellverzeichnis: Path = Path("./md")
    zielverzeichnis: Path = Path("./INHALTSVERZEICHNIS")
    pygments_css: str = "pygments_style.css"
    custom_css: str = "custom_style.css"
    sprachoptionen: Dict[str, str] = field(
        default_factory=lambda: {
            ".py": "python",
            ".php": "php",
            ".js": "javascript",
            ".c": "c",
            ".cc": "cpp",
        }
    )


class VerzeichnisKonverter:
    """Klasse zur Konvertierung und Verarbeitung von Verzeichnissen."""

    def __init__(self, config: Config):
        """Initialisiert den VerzeichnisKonverter."""
        self.config = config
        self.unterstuetzte_endungen = [".md", ".cc", ".py", ".php", ".pdf", ".js", ".c"]

    def run_command(self, command: List[str]) -> bool:
        """Führt einen Befehl aus und protokolliert das Ergebnis.

        Args:
            command: Liste der Befehlskomponenten

        Returns:
            bool: True bei erfolgreichem Befehl, sonst False
        """
        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
            logging.info("Befehl erfolgreich: %s", " ".join(command))
            return True
        except subprocess.CalledProcessError as e:
            logging.error(
                "Befehlsfehler: %s\nStdout: %s\nStderr: %s",
                " ".join(command),
                e.stdout,
                e.stderr,
            )
            return False

    def konvertiere_datei(self, dateipfad: Path, zielverzeichnis: Path) -> None:
        """Konvertiert eine Datei in das entsprechende Format oder kopiert sie.

        Args:
            dateipfad: Pfad zur Quelldatei
            zielverzeichnis: Pfad zum Zielverzeichnis
        """
        dateiname = dateipfad.stem
        endung = dateipfad.suffix.lower()
        zieldatei = zielverzeichnis / f"{dateiname}.html"

        if endung == ".md":
            self._konvertiere_markdown(dateipfad, zieldatei)
        elif endung == ".pdf":
            self._kopiere_pdf(dateipfad, zielverzeichnis)
        elif endung in self.config.sprachoptionen:
            self._konvertiere_code(dateipfad, zieldatei, endung)
        else:
            logging.warning("Keine Aktion definiert für Endung: %s", endung)

    def _konvertiere_markdown(self, quelle: Path, ziel: Path) -> None:
        """Konvertiert Markdown zu HTML."""
        css_pfad = self.config.zielverzeichnis / self.config.custom_css
        command = [
            "pandoc",
            str(quelle),
            "-o",
            str(ziel),
            "-s",
            "--mathjax",
            "-c",
            str(css_pfad),
        ]
        if self.run_command(command):
            logging.info("Markdown konvertiert: %s", ziel)

    def _kopiere_pdf(self, quelle: Path, ziel: Path) -> None:
        """Kopiert eine PDF-Datei."""
        shutil.copy2(quelle, ziel)
        logging.info("PDF kopiert: %s", quelle)

    def _konvertiere_code(self, quelle: Path, ziel: Path, endung: str) -> None:
        """Konvertiert Code-Dateien zu HTML mit Syntaxhervorhebung."""
        sprache = self.config.sprachoptionen[endung]
        command = [
            "pygmentize",
            "-l",
            sprache,
            "-f",
            "html",
            "-O",
            f"full,cssfile={self.config.pygments_css}",
            "-o",
            str(ziel),
            str(quelle),
        ]
        if self.run_command(command):
            logging.info("Code konvertiert: %s", quelle)

    def erstelle_verzeichnisstruktur(
        self,
        ordnerpfad: Path,
        tiefe: int = 0,
        root: Optional[Path] = None,
    ) -> str:
        """Erstellt die HTML-Verzeichnisstruktur rekursiv."""
        if root is None:
            root = ordnerpfad

        struktur = []
        einzug = "    " * tiefe

        for element in sorted(ordnerpfad.iterdir()):
            if element.is_dir():
                unterstruktur = self.erstelle_verzeichnisstruktur(element, tiefe + 1, root)
                struktur.append(
                    f"{einzug}<li class='dir'>{element.name}<ul>\n"
                    f"{unterstruktur}{einzug}</ul></li>\n"
                )
            else:
                dateilink = self._erstelle_dateilink(element, root)
                if dateilink:
                    struktur.append(f"{einzug}<li class='file'>{dateilink}</li>\n")

        return "".join(struktur)

    def _erstelle_dateilink(self, dateipfad: Path, root: Path) -> Optional[str]:
        """Erstellt einen HTML-Link für eine Datei."""
        endung = dateipfad.suffix.lower()
        if endung not in self.unterstuetzte_endungen:
            return None

        rel_pfad = dateipfad.relative_to(root)
        if endung == ".pdf":
            return f"<a href='./{rel_pfad}'>{dateipfad.name}</a>"
        return f"<a href='./{dateipfad.stem}.html'>{dateipfad.name}</a>"

    def erstelle_inhaltsverzeichnis(self) -> None:
        """Erstellt das HTML-Inhaltsverzeichnis."""
        struktur = self.erstelle_verzeichnisstruktur(self.config.quellverzeichnis)
        zieldatei = self.config.zielverzeichnis / "INHALTSVERZEICHNIS.html"

        inhalt = [
            "<!DOCTYPE html>",
            "<html lang='de'>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<title>Inhaltsverzeichnis</title>",
            f"<link rel='stylesheet' href='./{self.config.custom_css}'>",
            "</head>",
            "<body>",
            "<div class='container'>",
            "<h1>Inhaltsverzeichnis</h1>",
            "<ul class='root'>",
            struktur,
            "</ul>",
            "</div>",
            "</body>",
            "</html>",
        ]

        zieldatei.write_text("\n".join(inhalt), encoding="utf-8")
        logging.info("Inhaltsverzeichnis erstellt: %s", zieldatei)

    def verarbeite_verzeichnis(self) -> None:
        """Hauptmethode zur Verarbeitung des Verzeichnisses."""
        self.config.zielverzeichnis.mkdir(exist_ok=True)

        # CSS-Dateien kopieren
        for css in [self.config.custom_css, self.config.pygments_css]:
            if (Path(".") / css).exists():
                shutil.copy2(css, self.config.zielverzeichnis / css)
                logging.info("CSS kopiert: %s", css)

        # Dateien konvertieren
        for datei in self.config.quellverzeichnis.rglob("*"):
            if datei.is_file() and datei.suffix.lower() in self.unterstuetzte_endungen:
                self.konvertiere_datei(datei, self.config.zielverzeichnis)

        # Inhaltsverzeichnis erstellen
        self.erstelle_inhaltsverzeichnis()
        logging.info("Verarbeitung abgeschlossen: %s", self.config.zielverzeichnis)


def main() -> None:
    """Hauptfunktion des Skripts."""
    config = Config()
    konverter = VerzeichnisKonverter(config)
    konverter.verarbeite_verzeichnis()


if __name__ == "__main__":
    main()
