"""Synchronisierung von LaTeX-Dateien.

Dieses Skript ermöglicht die Synchronisierung von .tex-Dateien zwischen Verzeichnissen.

Hauptfunktionalitäten:
1. Synchronisierung aller .tex-Dateien oder einer spezifischen Datei
2. Benutzerinteraktion zur Auswahl der Synchronisierungsmethode
3. Sichere Ausführung von rsync-Befehlen

Hauptkomponenten:
- sicherer_aufruf: Führt einen Befehl sicher aus und behandelt Fehler
- synchronisiere_tex_dateien: Synchronisiert .tex-Dateien basierend auf der Benutzerauswahl
- auswahl_und_synchronisierung: Ermöglicht die Benutzerauswahl und führt die Synchronisation durch

Verwendung:
    python sync_tex.py

Das Skript führt den Benutzer interaktiv durch den Prozess der Dateiauswahl und Synchronisierung.

Voraussetzungen:
- rsync muss auf dem System installiert sein

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import subprocess


def sicherer_aufruf(befehl: list[str]) -> None:
    """Führt einen Befehl sicher aus."""
    try:
        subprocess.run(befehl, check=True)
    except subprocess.CalledProcessError:
        print("Es gab einen Fehler beim Ausführen des Befehls.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def synchronisiere_tex_dateien(spezifische_datei: str | None = None) -> None:
    """Synchronisiert .tex-Dateien basierend auf der Benutzerauswahl."""
    befehl = ["rsync", "-avh", "--progress"]
    if spezifische_datei:
        vollstaendiger_pfad = "tex/" + spezifische_datei
        befehl.append(vollstaendiger_pfad)
    else:
        befehl.append("tex/")
    befehl.append(".")
    sicherer_aufruf(befehl)


def auswahl_und_synchronisierung() -> None:
    """Ermöglicht die Benutzerauswahl und führt die Synchronisation durch."""
    auswahl = (
        input("Möchten Sie alle Dateien kopieren (A) oder nur eine bestimmte (B)? [A/B]: ")
        .strip()
        .upper()
    )
    if auswahl == "A":
        synchronisiere_tex_dateien()
    elif auswahl == "B":
        dateiname = input("Geben Sie den Namen der Datei ein (z.B. beispiel.tex): ")
        synchronisiere_tex_dateien(dateiname)
    else:
        print("Ungültige Auswahl.")


def main() -> None:
    auswahl_und_synchronisierung()


if __name__ == "__main__":
    main()
