# Konfigurationsdateien für eine bessere Wartbarkeit

# pyproject.toml

```
[tool.black]
line-length = 100
target-version = ['py313']
include = '\.pyx?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
ignore_missing_imports = true
```
# .gitignore

```
# Projektspezifische Dateien
NAVIGATION.html
update_log.txt
*.pdf
html/*.html
images/output/
tex/*.tex

# Eingebettete Git-Repositories
Entwicklung/Git/C-Entwicklung/hello-world/
Entwicklung/Git/fork/MeinProjekt/

# System und Editor
.DS_Store
Thumbs.db
*.un~
*~
.*.un~
.*.swp
.*.swo
*.bak
.gitignore.bak
.idea/
.vscode/

# CRLF/LF Konvertierung
*.ps1 -text

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/
env.bak/
venv.bak/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.env
.env.local
.coverage
.coverage.*
.pytest_cache/
.mypy_cache/
.dmypy.json
dmypy.json
.tox/
htmlcov/
.hypothesis/
pip-log.txt
pip-delete-this-directory.txt

# Jupyter
.ipynb_checkpoints/
profile_default/
ipython_config.py

# Build und Distribution
build/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
develop-eggs/
.pybuilder/
target/
instance/
out/

# LaTeX
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.run.xml
*.synctex.gz
*.toc
# ...
```

# .pre-commit-config.yaml

```
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: mixed-line-ending
        args: [--fix=lf]

  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3.13

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        additional_dependencies:
          - flake8-docstrings
        args: [--max-line-length=100]
```

# setup.cfg

```
[flake8]
max-line-length = 100
extend-ignore = D103,D209,D210,D400,D401,F401
exclude =
    .git,
    __pycache__,
    build,
    dist,
    .eggs,
    *.egg,
    Entwicklung/*
```

# .flake8

```
[flake8]
# Maximale Zeilenlänge
max-line-length = 100

# Dateien und Verzeichnisse, die ignoriert werden sollen
exclude =
    venv,
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info,
    .eggs,
    .tox,
    .mypy_cache

# Ignoriere bestimmte Fehler
ignore =
    # E203: Whitespace before ':' (wird von black anders formatiert)
    E203,
    # W503: Line break before binary operator (wird von black anders formatiert)
    W503,
    # E226: Missing whitespace around arithmetic operator
    E226

# Maximale Komplexität (McCabe complexity)
max-complexity = 10

# Stilüberprüfungen
# Dokumentations-Überprüfungen aktivieren
docstring-convention = google

# Statistik anzeigen
statistics = True

# Dateinamen-Muster
filename = *.py

# Fehler im Format: {Dateipfad}:{Zeile}:{Spalte}: {Fehler-Code} {Nachricht}
format = %(path)s:%(row)d:%(col)d: %(code)s %(text)s
```

# requirements-dev.txt

```
black==24.1.1
flake8==7.0.0
flake8-docstrings==1.7.0
isort==5.13.2
mypy==1.8.0
pre-commit==3.6.0
pytest==8.0.0
pytest-cov==4.1.0
```

# .flake8

```
[flake8]
# Maximale Zeilenlänge
max-line-length = 100

# Dateien und Verzeichnisse, die ignoriert werden sollen
exclude =
    venv,
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info,
    .eggs,
    .tox,
    .mypy_cache

# Ignoriere bestimmte Fehler
ignore =
    # E203: Whitespace before ':' (wird von black anders formatiert)
    E203,
    # W503: Line break before binary operator (wird von black anders formatiert)
    W503,
    # E226: Missing whitespace around arithmetic operator
    E226

# Maximale Komplexität (McCabe complexity)
max-complexity = 10

# Stilüberprüfungen
# Dokumentations-Überprüfungen aktivieren
docstring-convention = google

# Statistik anzeigen
statistics = True

# Dateinamen-Muster
filename = *.py

# Fehler im Format: {Dateipfad}:{Zeile}:{Spalte}: {Fehler-Code} {Nachricht}
format = %(path)s:%(row)d:%(col)d: %(code)s %(text)s
```

# Projektabhängigkeiten

1. Eine `requirements.txt` für die Produktionsabhängigkeiten
2. Eine `requirements-dev.txt` für die Entwicklungswerkzeuge

Requirements nutzen:

1. **Für die Entwicklungsumgebung:**
   ```bash
   pip install -r requirements-dev.txt
   ```
   Dies installiert alle Abhängigkeiten (Produktion + Entwicklung)

2. **Für die Produktionsumgebung:**
   ```bash
   pip install -r requirements.txt
   ```
   Dies installiert nur die für die Produktion notwendigen Pakete

**Empfehlungen**:

1. **Virtuelle Umgebung erstellen:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Linux/Mac
   # oder
   .\venv\Scripts\activate  # Unter Windows
   ```

2. **Abhängigkeiten aktualisieren:**
   ```bash
   pip install --upgrade -r requirements-dev.txt
   ```

3. **Abhängigkeitsbaum anzeigen:**
   ```bash
   pipdeptree
   ```
   Dies zeigt Ihnen die Hierarchie der installierten Pakete

4. **Neue Abhängigkeiten hinzufügen:**
   - Produktionsabhängigkeiten in `requirements.txt`
   - Entwicklungswerkzeuge in `requirements-dev.txt`

5. **Requirements einfrieren:**
   ```bash
   pip freeze > requirements-freeze.txt
   ```
   Dies erstellt eine vollständige Liste aller installierten Pakete mit exakten Versionen


6. **Pre-commit Hooks einrichten:**
   ```bash
   pre-commit install
   ```

7. **Manuelle Ausführung der Werkzeuge:**
   ```bash
   # Formatierung
   black .
   isort .

   # Überprüfung
   flake8
   mypy .
   ```

Die Konfiguration bietet folgende Vorteile:

1. **Einheitliche Formatierung:**
   - Black und isort sind aufeinander abgestimmt
   - 100 Zeichen Zeilenlänge
   - Konsistente Import-Sortierung

2. **Strikte Typisierung:**
   - Mypy ist auf strenge Typenprüfung eingestellt
   - Ignoriert fehlende Importe von Drittanbieter-Bibliotheken

3. **Automatische Prüfungen:**
   - Pre-commit Hooks verhindern Commits mit Formatierungsfehlern
   - Zusätzliche Prüfungen für YAML und große Dateien

4. **Entwicklungsabhängigkeiten:**
   - Alle notwendigen Werkzeuge sind in requirements-dev.txt definiert
   - Festgelegte Versionen für Reproduzierbarkeit


# zwei eingebettete Git-Repositories

1. **Entfernen der eingebetteten Repositories aus dem Index:**
```bash
# Repository 1 entfernen
git rm --cached Entwicklung/Git/C-Entwicklung/hello-world

# Repository 2 entfernen
git rm --cached Entwicklung/Git/fork/MeinProjekt
```

2. **Gitignore erweitern** um diese Verzeichnisse:

3. **Git-Attribute für PowerShell-Skripte** festlegen durch Erstellung einer `.gitattributes` Datei:

```
# Auto detect text files and perform LF normalization
* text=auto

# PowerShell-Skripte
*.ps1 text eol=crlf

# Bash-Skripte
*.sh text eol=lf

# Python
*.py text diff=python

# Documentation
*.md text diff=markdown
*.tex text diff=tex

# Binary files
*.pdf binary
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.svg binary
```

4. **Schritte zur Bereinigung:**
```bash
# 1. Aktuelle Änderungen sichern
git stash

# 2. Cache leeren
git rm -r --cached .

# 3. Neue .gitignore und .gitattributes anwenden
git add .gitignore .gitattributes

# 4. Alle Dateien neu hinzufügen
git add .

# 5. Änderungen committen
git commit -m "Bereinige Repository-Struktur und füge .gitattributes hinzu"

# 6. Gesicherte Änderungen zurückholen
git stash pop
```

5. **Optionale Konfiguration** um die Warnung zu deaktivieren:
```bash
git config advice.addEmbeddedRepo false
```

Wenn Sie die eingebetteten Repositories als Submodule verwenden möchten, können Sie stattdessen:
```bash
# Für Repository 1
git submodule add <url> Entwicklung/Git/C-Entwicklung/hello-world

# Für Repository 2
git submodule add <url> Entwicklung/Git/fork/MeinProjekt
```

# pre-commit-Tool

1. **`pre-commit` installieren**
   Installiere `pre-commit` in der virtuellen Umgebung:

   ```bash
   pip install pre-commit
   ```

2. **Prüfen, ob die Installation erfolgreich war**
   Verifiziere die Installation mit:

   ```bash
   pre-commit --version
   ```

3. **Pre-Commit-Hooks erneut installieren**
   Nachdem das Tool verfügbar ist, führe den Installationsbefehl erneut aus:

   ```bash
   pre-commit clean
   pre-commit install
   pre-commit autoupdate
   ```

4. **Pre-Commit-Hooks testen**
   Überprüfe, ob die Hooks korrekt funktionieren:

   ```bash
   pre-commit run --all-files
   ```

.pre-commit-config.yaml

# Whitespace- und End-of-file-Checks überspringen

Lassen Sie uns alle pre-commit Hooks für diesen initialen Commit überspringen:

```bash
SKIP=flake8,black,isort,trailing-whitespace,end-of-file-fixer git commit -m "Update Konfigurationsdateien

- Aktualisiere .gitignore für besseres Datei-Management
- Füge .flake8 für Python Code-Qualitätsprüfung hinzu
- Aktualisiere .pre-commit-config.yaml für automatische Prüfungen
- Bereinige Projektstruktur"
```

Dies wird:
1. Alle Code-Format-Checks überspringen (flake8, black, isort)
2. Die Whitespace-Checks überspringen
3. Die End-of-file-Checks überspringen
4. Nur die grundlegendsten Checks durchführen

Danach können wir in separaten Commits die Formatierung der Dateien vornehmen.


Ah, ich sehe das Problem. GitHub akzeptiert keine Passwort-Authentifizierung mehr. Stattdessen müssen Sie einen Personal Access Token (PAT) verwenden. Hier ist die Schritt-für-Schritt-Anleitung:

1. **Erstellen Sie einen GitHub Personal Access Token:**
   - Gehen Sie zu GitHub.com und loggen Sie sich ein
   - Klicken Sie auf Ihr Profilbild → Settings
   - Scrollen Sie nach unten zu "Developer settings" (ganz unten links)
   - Klicken Sie auf "Personal access tokens" → "Tokens (classic)"
   - Wählen Sie "Generate new token" → "Generate new token (classic)"
   - Geben Sie dem Token einen Namen, z.B. "Git Push Token"
   - Wählen Sie die Berechtigungen:
     - mindestens `repo` muss ausgewählt sein
   - Klicken Sie auf "Generate token"
   - **Wichtig**: Kopieren Sie den Token sofort - er wird nur einmal angezeigt!

2. **Git konfigurieren:**
```bash
# Speichern Sie den Token für zukünftige Verwendung
git config --global credential.helper store

# Versuchen Sie dann erneut zu pushen
git push

# Wenn nach Anmeldedaten gefragt wird:
# Username: Ihr GitHub Benutzername
# Password: Fügen Sie den kopierten Token ein (NICHT Ihr GitHub Passwort)
```

3. **Alternative (wenn Sie den Token nicht speichern möchten):**
```bash
# Fügen Sie den Token direkt in die URL ein
```

Für das Pushen zu Ihrem Repository benötigen Sie nur die grundlegenden Berechtigungen.

Mindestanforderungen:
- [x] `repo` (Full control of private repositories)
  - Dies deckt alles ab, was Sie für normale Git-Operationen brauchen

Optional, aber nützlich:
- [x] `read:user` (Read ALL user profile data)
- [x] `user:email` (Access user email addresses)

Alle anderen Berechtigungen sind für Ihr aktuelles Vorhaben nicht notwendig.

Der wichtigste Scope ist `repo`, der reicht für:
- Push
- Pull
- Commit
- Branch-Operationen
- Issue-Management

Die Auswahl ist einfach:
1. Wählen Sie `repo` aus
2. Geben Sie dem Token einen aussagekräftigen Namen (z.B. "Git Push Access")
3. Setzen Sie ein angemessenes Ablaufdatum (z.B. 90 Tage)
4. Klicken Sie auf "Generate token"

# Git-Historie aufräumen

Die letzten Commits, die sich mit der Konfiguration und Token-Entfernung beschäftigen.

```bash
# Interaktives Rebase starten, um die letzten 5 Commits zu kombinieren
git rebase -i HEAD~5
```

Im Editor würden wir dann:
```
pick 7817741 Update .gitignore und .gitattributes
squash 92be1f6 Update Konfigurationsdateien
squash 4599b09 Cleanup: Entferne nicht benötigte Bilddateien
squash f4526f7 python konfig update
squash 37ccb0d Remove exposed token for security
```

Dies würde alle diese Commits in einen einzigen, sauberen Commit zusammenfassen mit einer aussagekräftigen Commit-Nachricht wie:

```
Update Projektkonfiguration und Bereinigung

- Aktualisiere .gitignore und .gitattributes
- Füge Python Code-Qualitätsprüfung hinzu
- Bereinige nicht benötigte Dateien
- Aktualisiere Python-Konfiguration
```

Nach dem Rebase müssten wir force-pushen:
```bash
git push --force-with-lease
```

#  Git-Historie bereinigen

Der Token ist immer noch in der Git-Historie vorhanden.

1. **Commit aus der Historie entfernen:**
```bash
# Interaktives Rebase starten, um den problematischen Commit zu bearbeiten
git rebase -i HEAD~5
```

2. **Im Editor:**
- Suchen Sie den Commit mit der Token-Exposition
- Ändern Sie `pick` zu `edit` bei diesem Commit
- Speichern und schließen Sie den Editor

```
pick 92be1f6 Update Konfigurationsdateien
pick 4599b09 Cleanup: Entferne nicht benötigte Bilddateien
edit b04f322 python konfig update
drop 70f0509 Remove exposed token for security
drop 122f29e Remove exposed token for security
```

1. **Token aus der Datei entfernen:**
```bash
# Datei bearbeiten
vim python-scripte/python-config.md
# Token entfernen

# Änderungen zum Commit hinzufügen
git add python-scripte/python-config.md
git commit --amend

# Rebase fortsetzen
git rebase --continue
```

4. **Force Push (da wir die Historie geändert haben):**
```bash
git push --force-with-lease
```
