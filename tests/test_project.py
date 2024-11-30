"""Enthält Unit-Tests für das Projekt."""

import importlib.util
import re
from pathlib import Path
from typing import Dict, List, Set

import pytest


def test_python_files_exist(python_files: List[Path]) -> None:
    assert python_files, "Keine Python-Dateien gefunden"


def test_file_encoding(python_files: List[Path]) -> None:
    valid_encodings: List[str] = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        "# coding: utf-8",
        '"""',
    ]
    for py_file in python_files:
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
            has_encoding = any(enc in content for enc in valid_encodings)
            assert has_encoding, f"{py_file} fehlt Header"


def test_config_files(config_files: List[Path]) -> None:
    assert config_files, "Keine Config-Dateien gefunden"
    for config in config_files:
        with open(config, "r", encoding="utf-8") as f:
            content = f.read()
            assert content.strip(), f"{config} ist leer"


def test_requirements(project_root: Path) -> None:
    req_files = ["requirements.txt", "requirements-dev.txt"]
    for req in req_files:
        req_path = project_root / req
        assert req_path.exists(), f"{req} fehlt"
        with open(req_path, "r") as f:
            content = f.read()
            assert content.strip(), f"{req} ist leer"


def test_documentation(doc_files: Dict[str, List[Path]]) -> None:
    assert doc_files["md"], "Keine Markdown-Dateien gefunden"
    readme = next((f for f in doc_files["md"] if f.name == "README.md"), None)
    assert readme, "README.md fehlt"


def test_python_syntax(python_files: List[Path]) -> None:
    for py_file in python_files:
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
            try:
                compile(content, str(py_file), "exec")
            except SyntaxError as e:
                assert False, f"Syntax-Fehler in {py_file}: {str(e)}"


def test_type_hints(python_files: List[Path]) -> None:
    ignored_files: Set[str] = {"__init__.py", "setup.py", "conftest.py"}
    for py_file in python_files:
        if py_file.name not in ignored_files:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                has_types = re.search(r"def \w+\([^)]*\)\s*->", content) or re.search(
                    r":\s*(?:str|int|float|bool|list|dict|tuple|set|None)\s*[,)]", content
                )
                assert has_types, f"{py_file} fehlen Type Hints"


def test_main_block(python_files: List[Path]) -> None:
    ignored_files: Set[str] = {"__init__.py", "conftest.py"}
    for py_file in python_files:
        if py_file.name not in ignored_files:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                has_main = re.search(r'if\s+__name__\s*==\s*["\']__main__["\']:', content)
                assert has_main, f"{py_file} fehlt if __name__ == '__main__'"


def test_docstring_quality(python_files: List[Path]) -> None:
    for py_file in python_files:
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
            has_docstring = re.search(r'"""[^"]+"""', content)
            assert has_docstring, f"{py_file} fehlt Docstring"


def test_function_length(python_files: List[Path]) -> None:
    max_lines = 50
    for py_file in python_files:
        with open(py_file, "r", encoding="utf-8") as f:
            functions = re.finditer(r"def\s+\w+\([^)]*\):[^(]*?(?=(?:def|\Z))", f.read(), re.DOTALL)
            for func in functions:
                lines = func.group().count("\n")
                assert lines <= max_lines, f"Funktion in {py_file} ist zu lang ({lines} Zeilen)"
