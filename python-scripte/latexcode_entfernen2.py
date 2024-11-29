"""LaTeX-Code-Bearbeitung.

Dieses Skript bearbeitet LaTeX-Dateien, indem es spezifische Muster sucht und ersetzt.

Hauptfunktionalitäten:
1. Suchen und Ersetzen von LaTeX-Befehlen in .tex-Dateien
2. Entfernen bestimmter LaTeX-Befehle
3. Verarbeitung einzelner oder mehrerer Dateien
4. Erstellung von Backup-Dateien vor Änderungen
5. Löschen von Backup-Dateien nach der Verarbeitung

Hauptfunktionen:
- suche_und_ersetze: Ersetzt Muster in einer .tex-Datei
- entferne_befehl: Entfernt einen bestimmten LaTeX-Befehl
- loesche_backup_dateien: Löscht alle .bak-Dateien im Verzeichnis
- bearbeite_dateien: Verarbeitet .tex-Dateien im Verzeichnis
- main: Hauptfunktion zur Steuerung des Ablaufs

Verwendung:
    python latexcode_entfernen2.py [--datei DATEINAME]

Args:
    --datei: Optionaler Name einer spezifischen .tex-Datei zur Bearbeitung

Konfiguration:
- VERZEICHNIS_PFAD: Pfad zum Verzeichnis mit .tex-Dateien
- SUCHMUSTER: Regulärer Ausdruck für zu suchendes Muster
- ERSATZMUSTER: Muster für die Ersetzung

Voraussetzungen:
- Python 3.x

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import argparse
import glob
import os
import re

# Konstanten als Großbuchstaben (Python-Konvention)
VERZEICHNIS_PFAD = "./tex"
LATEX_BEFEHL = "\\passthrough"  # suchen und ersetzen von \passthrough

# Muster für die Suche und Ersetzung
# Such- und Ersatzmuster
SUCHMUSTER = r"\{\[\}@([^:]+:[^:]+:[^\]]+)\{\]\}"
ERSATZMUSTER = r"\\textcite{\1}"


def suche_und_ersetze(tex_pfad: str, suchmuster: str, ersetzen_durch: str) -> None:
    try:
        with open(tex_pfad, "r", encoding="utf-8") as datei:
            inhalt = datei.read()
            inhalt = re.sub(suchmuster, ersetzen_durch, inhalt)

        backup_pfad = tex_pfad + ".bak"
        with open(backup_pfad, "w", encoding="utf-8") as backup_datei:
            backup_datei.write(inhalt)
        with open(tex_pfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)
    except IOError as e:
        print(f"Fehler beim Bearbeiten der Datei {tex_pfad}: {e}")


def entferne_befehl(tex_pfad: str, befehl: str) -> None:
    try:
        with open(tex_pfad, "r", encoding="utf-8") as datei:
            inhalt = datei.read()
            if befehl in inhalt:
                print(f"Befehl {befehl} gefunden in {tex_pfad}")
            else:
                print(f"Befehl {befehl} nicht gefunden in {tex_pfad}")

        backup_pfad = tex_pfad + ".bak"
        with open(backup_pfad, "w", encoding="utf-8") as backup_datei:
            backup_datei.write(inhalt)
        with open(tex_pfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt.replace(befehl, ""))
    except IOError as e:
        print(f"Fehler beim Bearbeiten der Datei {tex_pfad}: {e}")


def loesche_backup_dateien() -> None:
    for backup_datei in glob.iglob(os.path.join(VERZEICHNIS_PFAD, "*.bak")):
        try:
            os.remove(backup_datei)
        except OSError as e:
            print(f"Fehler beim Löschen der Backup-Datei {backup_datei}: {e}")


def bearbeite_dateien(spezifische_datei: str | None = None) -> None:
    dateien = (
        [os.path.join(VERZEICHNIS_PFAD, spezifische_datei + ".tex")]
        if spezifische_datei
        else list(glob.iglob(os.path.join(VERZEICHNIS_PFAD, "*.tex")))
    )
    for tex_datei in dateien:
        if os.path.isfile(tex_datei):
            suche_und_ersetze(tex_datei, SUCHMUSTER, ERSATZMUSTER)
            print(f"Datei {tex_datei} bearbeitet.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bearbeitet LaTeX-Dateien.")
    parser.add_argument("--datei", help="Name der .tex-Datei, die bearbeitet werden soll.")
    args = parser.parse_args()

    if args.datei and (not args.datei.isalnum() or ".." in args.datei or "/" in args.datei):
        print("Ungültiger Dateiname. Bitte geben Sie einen Dateinamen ohne Pfadangaben an.")
        return

    bearbeite_dateien(args.datei)
    loesche_backup_dateien()


if __name__ == "__main__":
    main()
