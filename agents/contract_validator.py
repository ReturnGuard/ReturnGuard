"""
Contract Validator - Erzwingt Contract-First Design.

Blockiert Backend/Frontend/Testing Phasen wenn Contract fehlt oder unvollständig ist.
"""

import re
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from .guardrails import track_performance


@dataclass
class ValidationResult:
    """Ergebnis der Contract-Validierung."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __bool__(self) -> bool:
        """Ermöglicht: if validation_result: ..."""
        return self.is_valid


class ContractValidator:
    """
    Validiert Contracts strikt nach Contract-First Prinzip.

    Prüft:
    - Contract-Datei existiert
    - Keine Platzhalter ([xyz], TODO, ???)
    - Funktionen definiert
    - Datenmodelle vorhanden (wenn nötig)
    - Fehlerfälle beschrieben
    - UI-States definiert
    - Integration-Sektion ausgefüllt
    """

    # Patterns die darauf hindeuten dass Contract unvollständig ist
    INCOMPLETE_PATTERNS = [
        r'\[.*?\]',  # [Platzhalter]
        r'TODO',
        r'\?\?\?',
        r'Beschreibung:.*?\n\s*$',  # Leere Beschreibung
        r'Wird in M\d',  # "Wird in M2..."
        r'Beispiel:.*?\n\s*$',  # Leeres Beispiel
    ]

    def __init__(self, contracts_path: Path):
        self.contracts_path = contracts_path

    @track_performance("Contract-Validierung", threshold_ms=500.0)
    def validate(self, feature_slug: str) -> ValidationResult:
        """
        Validiert Contract für ein Feature.

        Args:
            feature_slug: URL-safe Feature-Slug

        Returns:
            ValidationResult mit is_valid, errors, warnings
        """
        errors = []
        warnings = []

        contract_file = self.contracts_path / f"{feature_slug}.md"

        # 1. Existiert Contract-Datei?
        if not contract_file.exists():
            errors.append(f"Contract-Datei fehlt: {contract_file}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # 2. Lese Contract
        try:
            content = contract_file.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Konnte Contract nicht lesen: {e}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # 3. Prüfe auf Platzhalter/TODOs
        incomplete_issues = self._check_incomplete_patterns(content)
        if incomplete_issues:
            errors.append(
                f"Contract enthält Platzhalter/TODOs:\n  - " + "\n  - ".join(incomplete_issues)
            )

        # 4. Prüfe Funktionen
        if not self._has_functions(content):
            errors.append(
                "Contract muss mindestens eine Funktion definieren.\n"
                "  Wenn wirklich keine Funktion nötig: Schreibe explizit '## Funktionen\\nKeine - nur UI-Änderungen'"
            )

        # 5. Prüfe Fehlerfälle
        if not self._has_error_cases(content):
            errors.append(
                "Contract muss Fehlerfälle beschreiben (Sektion '## Fehlerfälle').\n"
                "  Mindestens: Was passiert bei leerem/ungültigem Input?"
            )

        # 6. Prüfe UI-States
        if not self._has_ui_states(content):
            warnings.append(
                "Contract sollte UI-States definieren (Loading/Error/Empty/Success).\n"
                "  Empfohlen auch für Backend-Features (für späteres UI)"
            )

        # 7. Prüfe Integration
        if not self._has_integration_section(content):
            warnings.append(
                "Contract sollte Integration-Sektion haben:\n"
                "  - Wo wird das Feature eingebaut?\n"
                "  - Wie wird es aufgerufen?"
            )

        # 8. Prüfe Input-Validierung
        if not self._has_validation(content):
            warnings.append(
                "Contract sollte Input-Validierung beschreiben (Sektion '## Validierung').\n"
                "  Was sind erlaubte Werte? Welche Constraints?"
            )

        # Entscheide: Valid wenn keine Errors
        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _check_incomplete_patterns(self, content: str) -> List[str]:
        """
        Prüft auf Platzhalter und unvollständige Stellen.

        Returns:
            Liste von gefundenen Problemen
        """
        issues = []

        # Entferne Code-Blöcke vor der Suche (um False Positives zu vermeiden)
        content_without_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

        for pattern in self.INCOMPLETE_PATTERNS:
            matches = re.findall(pattern, content_without_code, re.MULTILINE | re.IGNORECASE)
            if matches:
                # Zeige nur einzigartige Matches (max 3)
                unique_matches = list(set(matches))[:3]
                for match in unique_matches:
                    issues.append(f"Platzhalter gefunden: '{match.strip()}'")

        return issues

    def _has_functions(self, content: str) -> bool:
        """
        Prüft ob Funktionen definiert sind.

        Akzeptiert:
        - def function_name(...) in Code-Block
        - Explizit "Keine - ..." wenn wirklich keine Funktion nötig
        """
        # Pattern 1: def function_name(...)
        if re.search(r'```python\s*\ndef\s+\w+\s*\(', content, re.MULTILINE):
            return True

        # Pattern 2: Explizit "Keine" mit Begründung
        if re.search(r'##\s*Funktionen.*?Keine\s*-', content, re.DOTALL | re.IGNORECASE):
            return True

        return False

    def _has_error_cases(self, content: str) -> bool:
        """Prüft ob Fehlerfälle beschrieben sind."""
        # Suche nach "## Fehlerfälle" Sektion mit Content
        # Lookahead: Entweder "## " (genau 2 # + Leerzeichen) oder Dateiende
        match = re.search(r'##\s*Fehlerfälle(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE)
        if not match:
            return False

        section_content = match.group(1).strip()

        # Muss mindestens eine Zeile mit "- " oder "* " haben (Bullet Points)
        # oder "Was passiert bei..." Pattern
        if re.search(r'[-*]\s+\w+', section_content):
            return True

        if re.search(r'Was passiert bei', section_content, re.IGNORECASE):
            return True

        return False

    def _has_ui_states(self, content: str) -> bool:
        """Prüft ob UI-States definiert sind."""
        # Suche nach "## UI-States" Sektion
        match = re.search(r'##\s*UI[- ]?States(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE)
        if not match:
            return False

        section_content = match.group(1).strip()

        # Prüfe ob mindestens Loading, Error, Success erwähnt werden
        has_loading = re.search(r'Loading\s*State', section_content, re.IGNORECASE)
        has_error = re.search(r'Error\s*State', section_content, re.IGNORECASE)
        has_success = re.search(r'Success\s*State', section_content, re.IGNORECASE)

        return bool(has_loading and has_error and has_success)

    def _has_integration_section(self, content: str) -> bool:
        """Prüft ob Integration-Sektion vorhanden ist."""
        return bool(re.search(r'##\s*Integration', content, re.IGNORECASE))

    def _has_validation(self, content: str) -> bool:
        """Prüft ob Validierung beschrieben ist."""
        # Suche nach "## Validierung" Sektion oder "validate_" Funktionen
        if re.search(r'##\s*Validierung', content, re.IGNORECASE):
            return True

        if re.search(r'def\s+validate_\w+', content):
            return True

        return False


def validate_contract(
    feature_slug: str,
    contracts_path: Path = Path("/home/user/ReturnGuard-App/contracts")
) -> ValidationResult:
    """
    Convenience-Funktion für Contract-Validierung.

    Args:
        feature_slug: Feature-Slug
        contracts_path: Pfad zum contracts/ Verzeichnis

    Returns:
        ValidationResult
    """
    validator = ContractValidator(contracts_path)
    return validator.validate(feature_slug)


def format_validation_result(result: ValidationResult, feature_slug: str) -> str:
    """
    Formatiert ValidationResult als lesbaren Text.

    Args:
        result: Das Validierungsergebnis
        feature_slug: Feature-Slug (für Pfadanzeige)

    Returns:
        Formatierter Text
    """
    lines = []

    if result.is_valid:
        lines.append("✅ Contract ist gültig!")
        if result.warnings:
            lines.append("\n⚠️  Warnungen (nicht blockierend):")
            for warning in result.warnings:
                lines.append(f"  - {warning}")
    else:
        lines.append("❌ Contract ist UNGÜLTIG - Backend/Frontend/Testing werden blockiert!")
        lines.append("\n🚫 Fehler (müssen behoben werden):")
        for error in result.errors:
            lines.append(f"  - {error}")

        if result.warnings:
            lines.append("\n⚠️  Zusätzliche Warnungen:")
            for warning in result.warnings:
                lines.append(f"  - {warning}")

        lines.append("\n📝 Nächste Schritte:")
        lines.append(f"  1. Öffne contracts/{feature_slug}.md")
        lines.append("  2. Behebe alle obigen Fehler")
        lines.append("  3. Entferne alle Platzhalter ([xyz], TODO, ???)")
        lines.append("  4. Fülle alle Sektionen vollständig aus")
        lines.append("  5. Führe run_agent.py erneut aus")

    return "\n".join(lines)


# CLI Test-Funktion
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python contract_validator.py <feature-slug>")
        print("Example: python contract_validator.py füge-dark-mode-toggle-hinzu")
        sys.exit(1)

    feature_slug = sys.argv[1]

    print(f"🔍 Validiere Contract: {feature_slug}\n")

    result = validate_contract(feature_slug)
    output = format_validation_result(result, feature_slug)

    print(output)

    # Exit code: 0 wenn valid, 1 wenn invalid
    sys.exit(0 if result.is_valid else 1)
