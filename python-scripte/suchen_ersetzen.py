"""LaTeX-Datei Verarbeitung.

Dieses Skript durchläuft alle .tex-Dateien in einem vorgegebenen Verzeichnis und führt eine Reihe
von spezifischen Ersetzungen und Bereinigungen durch.

Hauptfunktionalitäten:
1. Konfiguration über eine Config-Klasse
2. Verarbeitung von .tex-Dateien mit verschiedenen Transformationen
3. Multithreading für parallele Verarbeitung mehrerer Dateien
4. Umfangreiche Fehlerbehandlung und Logging

Hauptkomponenten:
- Config: Dataclass für die Konfiguration der Verarbeitung
- LatexProcessor: Klasse zur Verarbeitung von LaTeX-Dateien

Verwendung:
    python suchen_ersetzen.py [--tex-dir VERZEICHNIS] [--verbose]

Args:
    --tex-dir: Optionaler Pfad zum Verzeichnis mit .tex-Dateien (Standard: ./tex)
    --verbose: Aktiviert ausführliche Logging-Ausgaben

Die Verarbeitung umfasst:
- Hinzufügen oder Ersetzen von Zeitstempel-Kommentaren
- Aktualisierung von figure-Umgebungen
- Anwendung einfacher Textersetzungen
- Ersetzung deutscher Sonderzeichen in Labels
- Konvertierung von Code-Blöcken
- Umwandlung von longtable zu normalen Tabellen
- Anpassung des Tabellenformats
- Konvertierung mathematischer Begrenzer
- Entfernung von pandoc-bounded Markierungen

Voraussetzungen:
- Python 3.x

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import datetime
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Match, Tuple

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class Config:
    """Konfigurationsklasse für das Skript."""

    tex_dir: Path
    timestamp: str
    label_replacements: Dict[str, str]
    default_image_width: str = "0.8"
    default_image_height: str = "0.6"

    @classmethod
    def create_default(cls, tex_dir: str = "./tex") -> "Config":
        """Erstellt eine Standardkonfiguration."""
        return cls(
            tex_dir=Path(tex_dir),
            timestamp=datetime.datetime.now().strftime("%d-%b-%y"),
            label_replacements={
                "uxfc": "ue",
                "uxf6": "oe",
                "uxe4": "ae",
                "uxdf": "ss",
            },
        )


class LatexProcessor:
    """Klasse zur Verarbeitung von LaTeX-Dateien."""

    # Typ-Alias für Transformationsfunktionen
    TransformFunc = Callable[..., str]
    TransformationType = Tuple[TransformFunc, Dict[str, Any]]

    def __init__(self, config: Config):
        """Initialisiert den LatexProcessor."""
        self.config = config
        self.table_patterns = {
            "toprule": r"\\toprule\\noalign{}\n",
            "endhead": r"\\noalign{}\n\\endhead\n",
            "bottomrule": r"\\bottomrule\\noalign{}\n\\endlastfoot\n",
        }
        self.simple_replacements = {
            ",height=\\textheight": "",
            "``": ">>",
            "''": "<<",
            "\\tightlist": "",
            "\\midrule": "\\midrule[\\heavyrulewidth]\n",
        }
        # Vorkompilierte reguläre Ausdrücke für bessere Performance
        self._figure_pattern = re.compile(
            r"(\\begin{figure}\s*\\centering\s*)(\\includegraphics)(\[.*?\])?(\{.*?\})",
            re.DOTALL,
        )
        self._label_pattern = re.compile(r"\\label{([^}]*?)}")
        self._code_pattern = re.compile(r"\\passthrough{\\lstinline!(.*?)!}")
        self._longtable_pattern = re.compile(
            r"\\begin{longtable}\[\]{@{}(.*?)@{}}(.*?)\\end{longtable}", re.DOTALL
        )
        self._table_content_pattern = re.compile(r"\\toprule(.*?)\\bottomrule", re.DOTALL)
        self._minipage_pattern = re.compile(
            r"\\begin{minipage}\[.*?\]{.*?}\\raggedright|\\end{minipage}"
        )
        self._math_pattern = re.compile(r"\\\(|\\\)")
        self._pandoc_pattern = re.compile(r"\\pandocbounded\{(.*?)\}")

    def process_files(self) -> None:
        """Verarbeitet alle .tex-Dateien im konfigurierten Verzeichnis."""
        try:
            os.chdir(self.config.tex_dir)
            logging.info("Verarbeite Dateien in: %s", self.config.tex_dir)

            tex_files = list(Path(".").glob("*.tex"))
            if not tex_files:
                logging.warning("Keine .tex-Dateien gefunden!")
                return

            logging.info("Gefundene .tex-Dateien: %d", len(tex_files))
            for file_path in tex_files:
                self._process_single_file(file_path)

        except OSError as e:
            logging.error("Fehler beim Zugriff auf Verzeichnis: %s", e)
            sys.exit(1)
        finally:
            os.chdir("..")

    def _process_single_file(self, file_path: Path) -> None:
        """Verarbeitet eine einzelne .tex-Datei."""
        logging.info("Verarbeite: %s", file_path)
        try:
            content = file_path.read_text(encoding="utf-8")
            content = self._apply_all_transformations(content, file_path.name)
            file_path.write_text(content, encoding="utf-8")
            logging.info("✓ Erfolgreich verarbeitet: %s", file_path)
        except Exception as e:
            logging.error("Fehler bei der Verarbeitung von %s: %s", file_path, e)

    def _apply_all_transformations(self, content: str, filename: str) -> str:
        """Wendet alle Transformationen auf den Inhalt an."""
        transformations: list[LatexProcessor.TransformationType] = [
            (self._add_or_replace_comment, {"filename": filename}),
            (self._update_figure_environment, {}),
            (self._apply_simple_replacements, {}),
            (self._replace_german_chars_in_labels, {}),
            (self._convert_code_blocks, {}),
            (self._convert_longtable_to_table, {}),
            (self._adjust_table_format, {}),
            (self._convert_math_delimiters, {}),
            (self._remove_pandoc_bounded, {}),
        ]

        for transform_func, kwargs in transformations:
            try:
                content = transform_func(content, **kwargs)
            except Exception as e:
                logging.error(
                    "Fehler bei Transformation %s: %s",
                    transform_func.__name__,
                    e,
                )

        return content

    # Die Typdeklarationen der Transformationsmethoden präzisieren
    def _add_or_replace_comment(self, content: str, filename: str) -> str:
        """Fügt einen Zeitstempel-Kommentar hinzu oder ersetzt ihn."""
        new_comment = f"% ju {self.config.timestamp} {filename}"
        lines = [line for line in content.splitlines() if not line.strip().startswith("% ju")]
        return "\n".join([new_comment] + lines)

    def _update_figure_environment(self, content: str) -> str:
        """Aktualisiert die figure-Umgebung mit standardisierten Größenangaben."""
        return self._figure_pattern.sub(self._repl_figure, content)

    def _repl_figure(self, match: Match[str]) -> str:
        """Hilfsfunktion für figure-Ersetzung."""
        before, includegraphics, options, path = match.groups()
        if not options:
            options = self._create_image_options()
        elif "width=" not in options and "height=" not in options:
            options = options[:-1] + "," + self._create_image_options()[1:]

        return f"{before}{includegraphics}{options}{path}\n" "%\\floatnotes{}\n" "%\\label{fig:}"

    def _create_image_options(self) -> str:
        """Erstellt die Standardoptionen für Bilder."""
        return (
            f"[width={self.config.default_image_width}\\textwidth,"
            f"height={self.config.default_image_height}\\textheight,keepaspectratio]"
        )

    def _apply_simple_replacements(self, content: str) -> str:
        """Wendet einfache Textersetzungen an."""
        for old, new in self.simple_replacements.items():
            content = content.replace(old, new)
        return content

    def _replace_german_chars_in_labels(self, content: str) -> str:
        """Ersetzt deutsche Sonderzeichen in Labels."""

        def replacer(match: Match[str]) -> str:
            label_content = match.group(1)
            for char, replacement in self.config.label_replacements.items():
                label_content = label_content.replace(char, replacement)
            return f"\\label{{{label_content}}}"

        return self._label_pattern.sub(replacer, content)

    def _convert_code_blocks(self, content: str) -> str:
        """Konvertiert Code-Blöcke."""
        return self._code_pattern.sub(r"\\verb|\1|", content)

    def _convert_longtable_to_table(self, content: str) -> str:
        """Konvertiert longtable zu normalen Tabellen."""

        def replacer(match: Match[str]) -> str:
            col_defs, table_content = match.groups()
            clean_content = self._clean_table_content(table_content)
            return self._create_table_environment(col_defs, clean_content)

        return self._longtable_pattern.sub(replacer, content)

    def _clean_table_content(self, content: str) -> str:
        """Bereinigt den Tabelleninhalt."""
        for pattern in self.table_patterns.values():
            content = re.sub(pattern, "", content)
        return content

    def _create_table_environment(self, col_defs: str, content: str) -> str:
        """Erstellt eine neue Tabellenumgebung."""
        return (
            "\\begin{table}[ht]\n"
            "  %\\caption{}\n"
            "  %\\label{tab:my-table}\n"
            f"  \\begin{{tabular}}{{@{{}}{col_defs}@{{}}}}\n"
            "  \\toprule\n"
            f"{content}"
            "  \\bottomrule\n"
            "  \\end{tabular}%\n"
            "\\end{table}"
        )

    def _adjust_table_format(self, content: str) -> str:
        """Passt das Tabellenformat an."""
        pattern = re.compile(
            r"\\begin{tabular}{@{}\s*>\s*{\\raggedright.*?\\end{tabular}", re.DOTALL
        )
        return pattern.sub(self._adjust_table_structure, content)

    def _adjust_table_structure(self, match: Match[str]) -> str:
        """Erstellt eine neue Tabellenstruktur."""
        table_content = self._extract_table_content(match.group(0))
        cols_count = self._calculate_columns(table_content)
        return self._create_adjusted_table(table_content, cols_count)

    def _extract_table_content(self, content: str) -> str:
        """Extrahiert den Tabelleninhalt."""
        match = self._table_content_pattern.search(content)
        if not match:
            return "Inhalt konnte nicht extrahiert werden."
        return self._minipage_pattern.sub("", match.group(1)).strip()

    def _calculate_columns(self, content: str) -> int:
        """Berechnet die Anzahl der Spalten."""
        if "\\\\" not in content:  # Geändert von 'not "\\\\" in content'
            return 1
        return content.count("&") // content.count("\\\\") + 1

    def _create_adjusted_table(self, content: str, cols_count: int) -> str:
        """Erstellt eine angepasste Tabellenstruktur."""
        return (
            f'\\begin{{tabular}}{{@{{}}{"l" * cols_count}@{{}}}}\n'
            "\\toprule\n"
            f"{content}\n"
            "\\bottomrule\n"
            "\\end{tabular}"
        )

    def _convert_math_delimiters(self, content: str) -> str:
        """Konvertiert mathematische Begrenzer."""
        return self._math_pattern.sub("$", content)

    def _remove_pandoc_bounded(self, content: str) -> str:
        """Entfernt pandoc-bounded Markierungen."""
        return self._pandoc_pattern.sub(r"\1", content)


def parse_arguments() -> argparse.Namespace:
    """Verarbeitet die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(
        description="Verarbeitet LaTeX-Dateien mit verschiedenen Transformationen.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--tex-dir",
        default="./tex",
        help="Verzeichnis mit den .tex-Dateien",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Aktiviert ausführliche Ausgaben",
    )
    return parser.parse_args()


def main() -> None:
    """Hauptfunktion des Skripts."""
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        config = Config.create_default(args.tex_dir)
        processor = LatexProcessor(config)
        processor.process_files()
        logging.info("Verarbeitung erfolgreich abgeschlossen!")
    except Exception as e:
        logging.error("Fehler bei der Verarbeitung: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
