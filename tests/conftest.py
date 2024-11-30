"""Konfigurationsdatei für Pytest Fixtures und Plugins."""

from pathlib import Path
from typing import Dict, List

import pytest


@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def python_files(project_root: Path) -> List[Path]:
    return list(project_root.glob("python-scripte/*.py"))


@pytest.fixture(scope="session")
def config_files(project_root: Path) -> List[Path]:
    return list(project_root.glob("*.yaml"))


@pytest.fixture(scope="session")
def doc_files(project_root: Path) -> Dict[str, List[Path]]:
    return {"md": list(project_root.glob("**/*.md")), "tex": list(project_root.glob("**/*.tex"))}
