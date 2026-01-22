"""
Repo-Scanner für die Analyse der ReturnGuard Codebase.

Liefert strukturierte Daten über:
- Entry Point
- Module/Pages
- Tests
- Dependencies
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .guardrails import track_performance


@dataclass
class RepoScanResult:
    """Ergebnis des Repo-Scans."""

    # Entry Point
    entry_point: Optional[str] = None
    entry_point_lines: int = 0

    # Pages/Features
    pages: List[str] = field(default_factory=list)

    # Funktionen
    functions: List[Dict[str, any]] = field(default_factory=list)
    cached_functions: List[str] = field(default_factory=list)

    # Tests
    has_tests: bool = False
    test_files: List[str] = field(default_factory=list)
    test_framework: Optional[str] = None

    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    dependency_source: Optional[str] = None  # requirements.txt oder pyproject.toml

    # Struktur
    python_files: List[str] = field(default_factory=list)
    directories: List[str] = field(default_factory=list)

    # Zusätzliche Infos
    has_streamlit: bool = False
    has_gitignore: bool = False
    repo_size_kb: int = 0


class RepoScanner:
    """
    Scannt ein Repository und liefert strukturierte Daten.

    Analysiert:
    - Entry Point (app.py, streamlit_app.py, main.py)
    - Pages (bei Streamlit: st.session_state.page == '...')
    - Funktionen (def, @cache_data, etc.)
    - Tests (tests/, test_*.py, *_test.py)
    - Dependencies (requirements.txt, pyproject.toml)
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

        if not self.repo_path.exists():
            raise ValueError(f"Repo-Pfad existiert nicht: {repo_path}")

    @track_performance("Repo-Scan", threshold_ms=500.0)
    def scan(self) -> RepoScanResult:
        """
        Führt vollständigen Repo-Scan durch.

        Returns:
            RepoScanResult mit allen gesammelten Daten
        """
        result = RepoScanResult()

        # 1. Entry Point finden
        result.entry_point = self._find_entry_point()
        if result.entry_point:
            result.entry_point_lines = self._count_lines(result.entry_point)

        # 2. Struktur scannen
        result.python_files = self._find_python_files()
        result.directories = self._find_directories()

        # 3. Entry Point analysieren (wenn vorhanden)
        if result.entry_point:
            result.pages = self._extract_pages(result.entry_point)
            result.functions = self._extract_functions(result.entry_point)
            result.cached_functions = self._extract_cached_functions(result.entry_point)
            result.has_streamlit = self._check_streamlit_usage(result.entry_point)

        # 4. Tests scannen
        result.has_tests, result.test_files, result.test_framework = self._scan_tests()

        # 5. Dependencies scannen
        result.dependencies, result.dependency_source = self._scan_dependencies()

        # 6. Zusätzliche Infos
        result.has_gitignore = (self.repo_path / ".gitignore").exists()
        result.repo_size_kb = self._calculate_repo_size()

        return result

    def _find_entry_point(self) -> Optional[str]:
        """
        Findet den Entry Point der App.

        Sucht in dieser Reihenfolge:
        1. app.py
        2. streamlit_app.py
        3. main.py
        4. Erstes .py File im Root

        Returns:
            Relativer Pfad zum Entry Point oder None
        """
        candidates = ["app.py", "streamlit_app.py", "main.py"]

        for candidate in candidates:
            path = self.repo_path / candidate
            if path.exists():
                return candidate

        # Fallback: Erstes .py File im Root
        for file in self.repo_path.glob("*.py"):
            if file.name not in ["setup.py", "conftest.py"]:
                return file.name

        return None

    def _find_python_files(self) -> List[str]:
        """Findet alle Python-Dateien (außer in __pycache__, .git, venv)."""
        python_files = []

        exclude_dirs = {"__pycache__", ".git", "venv", ".venv", "env", ".env", "node_modules"}

        for py_file in self.repo_path.rglob("*.py"):
            # Prüfe ob File in excluded dir liegt
            if any(excl in py_file.parts for excl in exclude_dirs):
                continue

            rel_path = py_file.relative_to(self.repo_path)
            python_files.append(str(rel_path))

        return sorted(python_files)

    def _find_directories(self) -> List[str]:
        """Findet alle Verzeichnisse (außer versteckte und venv)."""
        directories = []

        exclude_dirs = {"__pycache__", ".git", "venv", ".venv", "env", ".env", "node_modules"}

        for dir_path in self.repo_path.rglob("*"):
            if not dir_path.is_dir():
                continue

            # Skip excluded
            if dir_path.name in exclude_dirs or dir_path.name.startswith("."):
                continue

            rel_path = dir_path.relative_to(self.repo_path)
            directories.append(str(rel_path))

        return sorted(directories)

    def _extract_pages(self, entry_point: str) -> List[str]:
        """
        Extrahiert Pages aus Streamlit App.

        Sucht nach Patterns wie:
        - st.session_state.page == 'home'
        - st.session_state.page = 'about'

        Returns:
            Liste von Page-Namen
        """
        file_path = self.repo_path / entry_point
        content = file_path.read_text(encoding="utf-8", errors="ignore")

        # Pattern: st.session_state.page = 'xyz' oder == 'xyz'
        pattern = r"st\.session_state\.page\s*[=!]=\s*['\"]([^'\"]+)['\"]"
        matches = re.findall(pattern, content)

        # Unique + sortiert
        pages = sorted(set(matches))
        return pages

    def _extract_functions(self, entry_point: str) -> List[Dict[str, any]]:
        """
        Extrahiert alle Funktionen aus Entry Point.

        Returns:
            Liste von Dicts mit {name, line, has_docstring}
        """
        file_path = self.repo_path / entry_point
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")

        functions = []
        for i, line in enumerate(lines, 1):
            # Pattern: def function_name(...)
            match = re.match(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", line)
            if match:
                func_name = match.group(1)

                # Prüfe ob nächste Zeile Docstring ist
                has_docstring = False
                if i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('"""') or next_line.startswith("'''"):
                        has_docstring = True

                functions.append({
                    "name": func_name,
                    "line": i,
                    "has_docstring": has_docstring
                })

        return functions

    def _extract_cached_functions(self, entry_point: str) -> List[str]:
        """
        Findet Funktionen mit @st.cache_data oder @st.cache_resource.

        Returns:
            Liste von Funktionsnamen
        """
        file_path = self.repo_path / entry_point
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")

        cached_funcs = []
        for i, line in enumerate(lines):
            # Prüfe ob Zeile @st.cache_* decorator ist
            if re.match(r"^\s*@st\.cache_(data|resource)", line):
                # Nächste Zeile sollte die Funktion sein
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    match = re.match(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", next_line)
                    if match:
                        cached_funcs.append(match.group(1))

        return cached_funcs

    def _check_streamlit_usage(self, entry_point: str) -> bool:
        """Prüft ob Streamlit importiert wird."""
        file_path = self.repo_path / entry_point
        content = file_path.read_text(encoding="utf-8", errors="ignore")

        # Pattern: import streamlit oder import streamlit as st
        return bool(re.search(r"^import\s+streamlit", content, re.MULTILINE))

    def _scan_tests(self) -> tuple[bool, List[str], Optional[str]]:
        """
        Scannt nach Tests.

        Sucht:
        - tests/ Verzeichnis
        - test_*.py Dateien
        - *_test.py Dateien

        Returns:
            (has_tests, test_files, test_framework)
        """
        test_files = []

        # Suche tests/ Verzeichnis
        tests_dir = self.repo_path / "tests"
        if tests_dir.exists():
            for test_file in tests_dir.rglob("*.py"):
                rel_path = test_file.relative_to(self.repo_path)
                test_files.append(str(rel_path))

        # Suche test_*.py im Root und Subdirs
        for test_file in self.repo_path.rglob("test_*.py"):
            rel_path = test_file.relative_to(self.repo_path)
            if str(rel_path) not in test_files:
                test_files.append(str(rel_path))

        # Suche *_test.py im Root und Subdirs
        for test_file in self.repo_path.rglob("*_test.py"):
            rel_path = test_file.relative_to(self.repo_path)
            if str(rel_path) not in test_files:
                test_files.append(str(rel_path))

        test_files = sorted(test_files)
        has_tests = len(test_files) > 0

        # Erkenne Test-Framework
        test_framework = None
        if has_tests:
            # Lese erste Test-Datei und schaue nach Imports
            first_test = self.repo_path / test_files[0]
            content = first_test.read_text(encoding="utf-8", errors="ignore")

            if re.search(r"^import\s+pytest", content, re.MULTILINE):
                test_framework = "pytest"
            elif re.search(r"^import\s+unittest", content, re.MULTILINE):
                test_framework = "unittest"

        return has_tests, test_files, test_framework

    def _scan_dependencies(self) -> tuple[List[str], Optional[str]]:
        """
        Scannt Dependencies.

        Sucht:
        1. requirements.txt
        2. pyproject.toml

        Returns:
            (dependencies, source)
        """
        # 1. requirements.txt
        req_file = self.repo_path / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text(encoding="utf-8", errors="ignore")
            deps = [
                line.strip()
                for line in content.split("\n")
                if line.strip() and not line.strip().startswith("#")
            ]
            return deps, "requirements.txt"

        # 2. pyproject.toml
        pyproject_file = self.repo_path / "pyproject.toml"
        if pyproject_file.exists():
            content = pyproject_file.read_text(encoding="utf-8", errors="ignore")

            # Extrahiere Dependencies aus [project.dependencies] oder [tool.poetry.dependencies]
            deps = []

            # Pattern für [project.dependencies]
            match = re.search(r'\[project\.dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
            if match:
                dep_section = match.group(1)
                # Pattern: "package>=version" oder 'package>=version'
                deps = re.findall(r'["\']([a-zA-Z0-9_-]+)[>=<]*[^"\']*["\']', dep_section)

            # Fallback: Poetry
            if not deps:
                match = re.search(r'\[tool\.poetry\.dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
                if match:
                    dep_section = match.group(1)
                    deps = re.findall(r'([a-zA-Z0-9_-]+)\s*=', dep_section)

            return deps, "pyproject.toml"

        return [], None

    def _count_lines(self, file_path: str) -> int:
        """Zählt Zeilen in einer Datei."""
        try:
            full_path = self.repo_path / file_path
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            return len(content.split("\n"))
        except:
            return 0

    def _calculate_repo_size(self) -> int:
        """Berechnet Repo-Größe in KB (nur .py Dateien)."""
        total_size = 0

        for py_file in self.repo_path.rglob("*.py"):
            # Skip __pycache__, .git, venv
            if any(excl in py_file.parts for excl in {"__pycache__", ".git", "venv", ".venv"}):
                continue

            try:
                total_size += py_file.stat().st_size
            except:
                pass

        return total_size // 1024  # Bytes -> KB


def scan_repo(repo_path: str = "/home/user/ReturnGuard-App") -> RepoScanResult:
    """
    Convenience-Funktion für schnellen Repo-Scan.

    Args:
        repo_path: Pfad zum Repository

    Returns:
        RepoScanResult mit allen Daten
    """
    scanner = RepoScanner(repo_path)
    return scanner.scan()


def format_scan_result(result: RepoScanResult) -> str:
    """
    Formatiert RepoScanResult als lesbaren Text.

    Args:
        result: Das Scan-Ergebnis

    Returns:
        Formatierter Text
    """
    lines = []

    lines.append("# Repo-Scan Ergebnis\n")

    # Entry Point
    lines.append("## Entry Point")
    if result.entry_point:
        lines.append(f"- Datei: `{result.entry_point}` ({result.entry_point_lines} Zeilen)")
        lines.append(f"- Streamlit App: {'Ja' if result.has_streamlit else 'Nein'}")
    else:
        lines.append("- ⚠️ Kein Entry Point gefunden")
    lines.append("")

    # Pages
    if result.pages:
        lines.append("## Pages/Features")
        for page in result.pages:
            lines.append(f"- {page}")
        lines.append("")

    # Funktionen
    if result.functions:
        lines.append("## Funktionen")
        lines.append(f"- Gesamt: {len(result.functions)}")
        if result.cached_functions:
            lines.append(f"- Cached (@st.cache_data): {', '.join(result.cached_functions)}")
        lines.append("")

    # Tests
    lines.append("## Tests")
    if result.has_tests:
        lines.append(f"- Framework: {result.test_framework or 'unbekannt'}")
        lines.append(f"- Test-Dateien ({len(result.test_files)}):")
        for test_file in result.test_files:
            lines.append(f"  - {test_file}")
    else:
        lines.append("- ⚠️ Keine Tests gefunden")
    lines.append("")

    # Dependencies
    lines.append("## Dependencies")
    if result.dependencies:
        lines.append(f"- Quelle: `{result.dependency_source}`")
        lines.append(f"- Anzahl: {len(result.dependencies)}")
        lines.append("- Liste:")
        for dep in result.dependencies:
            lines.append(f"  - {dep}")
    else:
        lines.append("- ⚠️ Keine Dependencies-Datei gefunden")
    lines.append("")

    # Struktur
    lines.append("## Struktur")
    lines.append(f"- Python-Dateien: {len(result.python_files)}")
    lines.append(f"- Verzeichnisse: {len(result.directories)}")
    lines.append(f"- Repo-Größe: {result.repo_size_kb} KB")
    lines.append(f"- .gitignore: {'Ja' if result.has_gitignore else 'Nein'}")

    return "\n".join(lines)


# CLI Test-Funktion
if __name__ == "__main__":
    print("🔍 Scanne ReturnGuard Repository...\n")

    result = scan_repo()
    output = format_scan_result(result)

    print(output)
    print("\n✅ Scan abgeschlossen!")
