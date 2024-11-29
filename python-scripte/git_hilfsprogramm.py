"""Git-Hilfsprogramm.

Dieses Skript bietet eine benutzerfreundliche Schnittstelle für gängige Git-Operationen.

Hauptfunktionalitäten:
1. Verwaltung lokaler und Remote-Repositories
2. Ausführung verschiedener Git-Befehle
3. Interaktive Benutzeroberfläche für Git-Operationen

Hauptkomponenten:
- GitConfig: Konfigurationsklasse für Git-Operationen
- GitHelper: Hauptklasse für Git-Operationen
- GitUI: Benutzeroberfläche für Git-Operationen

Verwendung:
    python git_hilfsprogramm.py <ordnername>

Args:
    ordnername: Name des zu bearbeitenden Verzeichnisses

Die Konfiguration enthält:
- github_url: URL des GitHub-Repositories
- readme_file: Name der README-Datei
- github_token: GitHub-Token für API-Zugriff (optional)

Voraussetzungen:
- Git muss auf dem System installiert sein
- GitHub CLI (gh) für bestimmte Operationen

Version: 1.0
Autor: Jan Unger
Datum: 26.11.2024
"""

import logging
import os
import re
import subprocess
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class GitConfig:
    """Konfigurationsklasse für Git-Operationen."""

    github_url: str = "https://github.com/ju1-eu/"
    readme_file: str = "README.md"
    github_token: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """Lädt Umgebungsvariablen nach der Initialisierung."""
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")


class GitHelper:
    """Hauptklasse für Git-Operationen."""

    def __init__(self, config: GitConfig):
        """Initialisiert den GitHelper mit der Konfiguration."""
        self.config = config

    def ausfuehren_befehl(self, befehl: Union[List[str], str], ordner: Union[str, Path]) -> bool:
        """Führt einen Shell-Befehl sicher aus.

        Args:
            befehl: Auszuführender Befehl
            ordner: Arbeitsverzeichnis

        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            if isinstance(befehl, str):
                befehl_str = befehl
                shell = True
            else:
                befehl_str = " ".join(befehl)
                shell = False

            result = subprocess.run(
                befehl,
                check=True,
                cwd=ordner,
                text=True,
                shell=shell,
                capture_output=True,
            )

            if result.stdout:
                logging.info("Ausgabe: %s", result.stdout)

            if result.stderr:
                if any(msg in result.stderr for msg in ["Zu Branch", "Bereits aktuell"]):
                    logging.info("Info: %s", result.stderr)
                else:
                    logging.warning("Fehlerausgabe (Ignorierbar): %s", result.stderr)

            return True

        except subprocess.CalledProcessError as e:
            logging.error(
                "Fehler bei Ausführung des Befehls: %s\nFehlerausgabe:\n%s",
                befehl_str,
                e.stderr,
            )
            return False

    def _hat_aenderungen(self, ordner: Path) -> bool:
        """Prüft, ob es Änderungen im Repository gibt."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=ordner,
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False

    def lokales_repo_erstellen(self, ordner: Path) -> None:
        """Erstellt und initialisiert ein lokales Git-Repository."""
        try:
            ordner.mkdir(parents=True, exist_ok=True)
            gitignore_path = ordner / ".gitignore"
            readme_path = ordner / self.config.readme_file

            if not gitignore_path.exists():
                gitignore_path.write_text(
                    "# Dateien und Verzeichnisse für Git-Ignorierung\n",
                    encoding="utf-8",
                )

            readme_content = (
                f"# {ordner.name} Repository\n"
                f"This is the README for the {ordner.name} repository.\n"
            )
            readme_path.write_text(readme_content, encoding="utf-8")

            self.ausfuehren_befehl(["git", "init"], ordner)
            self.ausfuehren_befehl(["git", "add", self.config.readme_file], ordner)

            if self._hat_aenderungen(ordner):
                self.ausfuehren_befehl(["git", "commit", "-m", "Initial commit"], ordner)

        except Exception as e:
            logging.error("Fehler beim Erstellen des Repositories: %s", e)
            raise

    def github_repo_verbinden(self, ordner: Path) -> None:
        """Verbindet ein lokales Repository mit GitHub."""
        entscheidung = self._abfrage_repo_art()

        if entscheidung == "vorhanden":
            self._verbinde_mit_bestehendem_repo(ordner)
        elif entscheidung == "neu":
            self._erstelle_und_verbinde_neues_repo(ordner)

    def _abfrage_repo_art(self) -> str:
        """Fragt den Benutzer nach der Art des GitHub-Repositories."""
        while True:
            auswahl = input(
                "Möchten Sie ein bestehendes Repository verwenden oder ein "
                "neues erstellen? (vorhanden/neu): "
            ).lower()
            if auswahl in ["vorhanden", "neu"]:
                return auswahl
            logging.warning("Ungültige Auswahl. Bitte 'vorhanden' oder 'neu' eingeben.")

    def _verbinde_mit_bestehendem_repo(self, ordner: Path) -> None:
        """Verbindet mit einem bestehenden GitHub-Repository."""
        repo_url = input("GitHub-Repository URL: ")
        self.ausfuehren_befehl(["git", "remote", "add", "origin", repo_url], ordner)
        self.ausfuehren_befehl(["git", "branch", "-M", "main"], ordner)
        self.ausfuehren_befehl(["git", "push", "-u", "origin", "main"], ordner)

    def _erstelle_und_verbinde_neues_repo(self, ordner: Path) -> None:
        """Erstellt ein neues GitHub-Repository und verbindet es."""
        repo_name = input("Name für das neue Repository: ")
        self.ausfuehren_befehl(["gh", "repo", "create", repo_name, "--public"], ordner)
        repo_url = f"{self.config.github_url}{repo_name}.git"
        self.ausfuehren_befehl(["git", "remote", "add", "origin", repo_url], ordner)
        self.ausfuehren_befehl(["git", "branch", "-M", "main"], ordner)
        self.ausfuehren_befehl(["git", "push", "-u", "origin", "main"], ordner)

    def aenderungen_hinzufuegen(self, ordner: Path) -> None:
        """Fügt Änderungen zum Staging-Bereich hinzu."""
        datei = input("Welche Datei hinzufügen? (. für alle): ")
        self.ausfuehren_befehl(["git", "add", datei], ordner)

    def aenderungen_commiten(self, ordner: Path) -> None:
        """Committet Änderungen im Repository."""
        if not self._hat_aenderungen(ordner):
            logging.info("Keine Änderungen zum Committen vorhanden.")
            return

        nachricht = input("Commit-Nachricht: ")
        self.ausfuehren_befehl(["git", "commit", "-m", nachricht], ordner)

    def aenderungen_pushen(self, ordner: Path) -> None:
        """Pusht Änderungen zum Remote-Repository."""
        self.ausfuehren_befehl(["git", "push", "origin", "main"], ordner)

    def aenderungen_pullen(self, ordner: Path) -> None:
        """Pullt Änderungen vom Remote-Repository."""
        if self._hat_aenderungen(ordner):
            logging.warning("Bitte erst lokale Änderungen committen oder stashen.")
            return

        self.ausfuehren_befehl(["git", "pull", "origin", "main"], ordner)

    def repo_klonen(self, ordner: Path) -> None:
        """Klont ein GitHub-Repository."""
        repos = self._get_user_repositories()
        if not repos:
            logging.warning("Keine Repositories gefunden.")
            return

        self._zeige_verfuegbare_repos(repos)
        auswahl = self._waehle_repository(repos)
        if auswahl is None:
            return

        repo = repos[auswahl]
        ziel = ordner / repo["name"]
        if ziel.exists() and any(ziel.iterdir()):
            logging.error("Zielordner existiert bereits und ist nicht leer.")
            return

        self.ausfuehren_befehl(
            ["git", "clone", f"{self.config.github_url}{repo['name']}.git"], ordner
        )

    def _get_user_repositories(self) -> List[Dict[str, Any]]:
        """Holt die Liste der Repository des Benutzers von GitHub."""
        username = self._get_username_from_url()
        if not username:
            logging.error("Konnte Benutzernamen nicht aus GitHub-URL extrahieren.")
            return []

        headers = (
            {"Authorization": f"token {self.config.github_token}"}
            if self.config.github_token
            else {}
        )

        try:
            response = requests.get(
                f"https://api.github.com/users/{username}/repos",
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            # Explizite Typ-Konvertierung
            result: List[Dict[str, Any]] = []
            for repo in response.json():
                if isinstance(repo, dict):
                    result.append(repo)
            return result
        except requests.RequestException as e:
            logging.error("Fehler beim Abrufen der Repositories: %s", e)
            return []

    def _get_username_from_url(self) -> Optional[str]:
        """Extrahiert den Benutzernamen aus der GitHub-URL."""
        match = re.match(r"https://github\.com/([^/]+)/?", self.config.github_url)
        return match.group(1) if match else None

    def _zeige_verfuegbare_repos(self, repos: List[Dict[str, Any]]) -> None:
        """Zeigt die verfügbaren Repositories an."""
        for idx, repo in enumerate(repos, 1):
            logging.info(
                "%d. %s\n   URL: %s\n",
                idx,
                repo["name"],
                repo["html_url"],
            )

    def _waehle_repository(self, repos: List[Dict[str, Any]]) -> Optional[int]:
        """Lässt den Benutzer ein Repository auswählen."""
        try:
            auswahl = int(input("Nummer des zu klonenden Repositories (0 zum Abbrechen): "))
            if 0 < auswahl <= len(repos):
                return auswahl - 1
            if auswahl == 0:
                return None
            logging.warning("Ungültige Auswahl.")
            return None
        except ValueError:
            logging.error("Bitte eine Zahl eingeben.")
            return None

    def branch_erstellen(self, ordner: Path) -> None:
        """Erstellt einen neuen Branch."""
        name = input("Name des neuen Branches: ")
        self.ausfuehren_befehl(["git", "checkout", "-b", name], ordner)

    def branch_wechseln(self, ordner: Path) -> None:
        """Wechselt zu einem anderen Branch."""
        name = input("Zu welchem Branch wechseln? ")
        self.ausfuehren_befehl(["git", "checkout", name], ordner)

    def alle_branches_anzeigen(self, ordner: Path) -> None:
        """Zeigt alle Branches an."""
        self.ausfuehren_befehl(["git", "fetch", "--all"], ordner)
        self.ausfuehren_befehl(["git", "branch", "-a"], ordner)

    def branch_mergen(self, ordner: Path) -> None:
        """Merged einen Branch in den aktuellen Branch."""
        branch = input("Welchen Branch mergen? ")
        self.ausfuehren_befehl(["git", "merge", branch], ordner)

    def aenderungen_stashen(self, ordner: Path) -> None:
        """Stasht die aktuellen Änderungen."""
        self.ausfuehren_befehl(["git", "stash"], ordner)
        logging.info("Änderungen wurden gestasht.")

    def konflikte_anzeigen(self, ordner: Path) -> None:
        """Zeigt Dateien mit Merge-Konflikten an."""
        self.ausfuehren_befehl(["git", "diff", "--name-only", "--diff-filter=U"], ordner)

    def pull_requests_anzeigen(self, ordner: Path) -> None:
        """Zeigt Pull Requests an."""
        self.ausfuehren_befehl(["gh", "pr", "list"], ordner)

    def gitignore_verwalten(self, ordner: Path) -> None:
        """Verwaltet die .gitignore-Datei."""
        auswahl = input("1. .gitignore anzeigen\n" "2. Regel hinzufügen\n" "Auswahl: ")

        gitignore_path = ordner / ".gitignore"

        if auswahl == "1":
            if gitignore_path.exists():
                logging.info("\n%s", gitignore_path.read_text(encoding="utf-8"))
            else:
                logging.warning(".gitignore existiert nicht.")
        elif auswahl == "2":
            regel = input("Neue Regel: ")
            with gitignore_path.open("a", encoding="utf-8") as f:
                f.write(f"\n{regel}")
            logging.info("Regel hinzugefügt: %s", regel)

    def log_anzeigen(self, ordner: Path) -> None:
        """Zeigt Git-Logs an."""
        self.ausfuehren_befehl(["git", "log", "--oneline"], ordner)

    def status_anzeigen(self, ordner: Path) -> None:
        """Zeigt Git-Status an."""
        self._zeige_status_legende()
        self.ausfuehren_befehl(["git", "status"], ordner)

    def _zeige_status_legende(self) -> None:
        """Zeigt Legende für Git-Status-Symbole."""
        legende = [
            "Status-Symbole:",
            "M  - Geänderte Datei",
            "A  - Hinzugefügte Datei",
            "D  - Gelöschte Datei",
            "?? - Ungetrackte Datei",
            "UU - Merge-Konflikt",
        ]
        for zeile in legende:
            logging.info(zeile)
        logging.info("-" * 50)

    def github_repos_anzeigen(self) -> None:
        """Zeigt alle GitHub-Repositories des Benutzers an."""
        repos = self._get_user_repositories()
        if repos:
            logging.info("Verfügbare Repositories:")
            for idx, repo in enumerate(repos, 1):
                logging.info(
                    "%d. %s\n   URL: %s\n   Beschreibung: %s\n",
                    idx,
                    repo["name"],
                    repo["html_url"],
                    repo.get("description", "Keine Beschreibung"),
                )
        else:
            logging.warning("Keine Repositories gefunden.")

    def github_repo_loeschen(self, ordner: Path) -> None:
        """Löscht ein GitHub-Repository."""
        name = input("Name des zu löschenden Repositories: ")
        if input(f"Repository '{name}' wirklich löschen? (j/n): ").lower() != "j":
            logging.info("Löschung abgebrochen.")
            return

        self.ausfuehren_befehl(["gh", "repo", "delete", name, "--yes"], ordner)
        logging.info("Repository '%s' wurde gelöscht.", name)


class GitUI:
    """Benutzeroberfläche für Git-Operationen."""

    def __init__(self, git_helper: GitHelper):
        """Initialisiert die Benutzeroberfläche."""
        self.git_helper = git_helper
        self.befehle: Dict[int, Dict[str, Any]] = {
            1: {
                "name": "Neues lokales Repository erstellen",
                "func": self.git_helper.lokales_repo_erstellen,
            },
            2: {
                "name": "Mit GitHub verbinden",
                "func": self.git_helper.github_repo_verbinden,
            },
            3: {
                "name": "Änderungen hinzufügen (git add)",
                "func": self.git_helper.aenderungen_hinzufuegen,
            },
            4: {
                "name": "Änderungen committen (git commit)",
                "func": self.git_helper.aenderungen_commiten,
            },
            5: {
                "name": "Änderungen pushen (git push)",
                "func": self.git_helper.aenderungen_pushen,
            },
            6: {
                "name": "Änderungen pullen (git pull)",
                "func": self.git_helper.aenderungen_pullen,
            },
            7: {
                "name": "Repository klonen",
                "func": self.git_helper.repo_klonen,
            },
            8: {
                "name": "Branch erstellen",
                "func": self.git_helper.branch_erstellen,
            },
            9: {
                "name": "Branch wechseln",
                "func": self.git_helper.branch_wechseln,
            },
            10: {
                "name": "Alle Branches anzeigen",
                "func": self.git_helper.alle_branches_anzeigen,
            },
            11: {
                "name": "Branch mergen",
                "func": self.git_helper.branch_mergen,
            },
            12: {
                "name": "Änderungen stashen",
                "func": self.git_helper.aenderungen_stashen,
            },
            13: {
                "name": "Merge-Konflikte anzeigen",
                "func": self.git_helper.konflikte_anzeigen,
            },
            14: {
                "name": "Pull Requests anzeigen",
                "func": self.git_helper.pull_requests_anzeigen,
            },
            15: {
                "name": ".gitignore verwalten",
                "func": self.git_helper.gitignore_verwalten,
            },
            16: {
                "name": "Git-Logs anzeigen",
                "func": self.git_helper.log_anzeigen,
            },
            17: {
                "name": "Git-Status anzeigen",
                "func": self.git_helper.status_anzeigen,
            },
            18: {
                "name": "GitHub-Repositories anzeigen",
                "func": self.git_helper.github_repos_anzeigen,
            },
            19: {
                "name": "GitHub-Repository löschen",
                "func": self.git_helper.github_repo_loeschen,
            },
        }

    def zeige_menue(self) -> str:
        """Zeigt das Hauptmenü an und gibt die Benutzerauswahl zurück.

        Returns:
            str: Die Benutzerauswahl oder 'q' zum Beenden
        """
        logging.info("\nGit-Operationen:")
        for nr, befehl in sorted(self.befehle.items()):
            logging.info("%d. %s", nr, befehl["name"])
        logging.info("q. Beenden")

        while True:
            auswahl = input("\nWählen Sie eine Option (oder 'q' zum Beenden): ").strip()
            if auswahl == "q" or auswahl.isdigit():
                return auswahl
            logging.warning("Ungültige Eingabe. Bitte eine Zahl oder 'q' eingeben.")

    def verarbeite_auswahl(self, auswahl: str, ordner: Path) -> bool:
        """Verarbeitet die Benutzerauswahl.

        Args:
            auswahl: Gewählte Option
            ordner: Zu bearbeitendes Verzeichnis

        Returns:
            bool: False wenn Beenden gewählt wurde, sonst True
        """
        if auswahl == "q":
            return False

        try:
            nr = int(auswahl)
            if nr in self.befehle:
                logging.info("=" * 50)
                self.befehle[nr]["func"](ordner)
                logging.info("=" * 50)
                input("\nDrücken Sie Enter zum Fortfahren...")
            else:
                logging.warning("Ungültige Auswahl.")
        except ValueError:
            logging.error("Bitte geben Sie eine gültige Zahl ein.")
        except Exception as e:
            logging.error("Fehler bei der Ausführung: %s", e)
            traceback.print_exc()

        return True


def main() -> None:
    """Hauptfunktion des Programms."""
    if len(sys.argv) != 2:
        logging.error("Bitte geben Sie den Ordnernamen als Argument an.")
        sys.exit(1)

    try:
        config = GitConfig()
        git_helper = GitHelper(config)
        ui = GitUI(git_helper)
        ordner = Path(sys.argv[1])

        while True:
            auswahl = ui.zeige_menue()  # Gibt jetzt garantiert einen String zurück
            if not ui.verarbeite_auswahl(auswahl, ordner):
                logging.info("Programm wird beendet.")
                break

    except KeyboardInterrupt:
        logging.info("\nProgramm wurde durch Benutzer beendet.")
        sys.exit(0)
    except Exception as e:
        logging.error("Unerwarteter Fehler: %s", e)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
