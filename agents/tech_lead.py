"""
Tech Lead Agent - Orchestriert den gesamten Implementierungs-Workflow.
"""

import os
from pathlib import Path
from typing import Dict, Optional
from .prompts import (
    TECH_LEAD_PROMPT,
    BACKEND_PROMPT,
    FRONTEND_PROMPT,
    TESTING_PROMPT,
    REVIEW_PROMPT,
    format_prompt
)
from .repo_scan import RepoScanner, RepoScanResult, format_scan_result
from .contract_validator import ContractValidator, ValidationResult, format_validation_result


class TechLeadAgent:
    """
    Tech Lead Agent orchestriert den kompletten Workflow:
    1. Repo-Scan
    2. Contract-First Design
    3. Plan erstellen
    4. Backend → Frontend → Tests delegieren
    5. Final Review
    """

    def __init__(self, repo_path: str = "/home/user/ReturnGuard-App"):
        self.repo_path = Path(repo_path)
        self.docs_path = self.repo_path / "docs"
        self.contracts_path = self.repo_path / "contracts"

        # Erstelle Verzeichnisse falls nicht vorhanden
        self.docs_path.mkdir(exist_ok=True)
        self.contracts_path.mkdir(exist_ok=True)

    def run(self, feature_request: str) -> Dict[str, str]:
        """
        Führt den kompletten Workflow durch.

        Args:
            feature_request: Die Feature-Beschreibung vom User

        Returns:
            Dict mit Paths zu allen generierten Dateien
        """
        print(f"\n🚀 Tech Lead Agent startet für: '{feature_request}'")
        print("=" * 80)

        # Feature-Slug für Dateinamen
        feature_slug = self._create_slug(feature_request)

        # Phase 0: Repo-Scan (M2)
        print("\n🔍 Phase 0: Scanne Repository...")
        scanner = RepoScanner(str(self.repo_path))
        scan_result = scanner.scan()
        print(f"✅ Repo gescannt: {scan_result.entry_point} ({scan_result.entry_point_lines} Zeilen)")
        print(f"   - Pages: {len(scan_result.pages)}")
        print(f"   - Funktionen: {len(scan_result.functions)}")
        print(f"   - Tests: {'Ja' if scan_result.has_tests else 'Nein'}")
        print(f"   - Dependencies: {len(scan_result.dependencies)}")

        # Phase 1: Plan erstellen (mit echten Repo-Daten - M2)
        print("\n📋 Phase 1: Erstelle Implementierungsplan...")
        plan_path = self._create_plan(feature_request, feature_slug, scan_result)
        print(f"✅ Plan gespeichert: {plan_path}")

        # Phase 2: Contract erstellen (wird vom User/Claude manuell ausgefüllt)
        contract_file = self.contracts_path / f"{feature_slug}.md"
        if contract_file.exists():
            print("\n📝 Phase 2: Contract existiert bereits - verwende bestehenden...")
            print(f"   {contract_file}")
            contract_path = contract_file
        else:
            print("\n📝 Phase 2: Contract-Template erstellt...")
            contract_path = self._create_contract_template(feature_request, feature_slug)
            print(f"✅ Contract-Template gespeichert: {contract_path}")
            print("⚠️  WICHTIG: Contract muss ausgefüllt werden bevor Backend-Phase startet!")

        # Phase 3: Contract-Validierung (M3 - Contract-First Enforcement)
        print("\n🔍 Phase 3: Validiere Contract (M3 - Contract-First Enforcement)...")
        validator = ContractValidator(self.contracts_path)
        validation_result = validator.validate(feature_slug)

        # Zeige Validierungsergebnis
        validation_output = format_validation_result(validation_result, feature_slug)
        print("\n" + validation_output)

        # Entscheide ob weitere Phasen möglich sind
        if validation_result.is_valid:
            print("\n✅ Contract ist gültig - bereit für M4 Phasen (Backend/Frontend/Testing/Review)")
            print("⏭️  M4 Phasen werden nach Abnahme von M3 implementiert")
        else:
            print("\n🚫 BLOCKIERT: Backend/Frontend/Testing können nicht starten!")
            print("   Contract muss erst vollständig ausgefüllt werden.")
            print("   Siehe obige Fehler und behebe sie.")

        return {
            "plan": str(plan_path),
            "contract": str(contract_path),
            "feature_slug": feature_slug,
            "scan_result": scan_result,
            "validation_result": validation_result
        }

    def _create_slug(self, text: str) -> str:
        """Erstellt einen URL-safe Slug aus dem Text."""
        import re
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]  # Max 50 Zeichen

    def _create_plan(self, feature_request: str, feature_slug: str, scan_result: RepoScanResult) -> Path:
        """
        Erstellt den Implementierungsplan mit echten Repo-Daten.

        Args:
            feature_request: Feature-Beschreibung
            feature_slug: URL-safe Slug
            scan_result: Ergebnis des Repo-Scans

        Returns:
            Path zum generierten Plan
        """
        prompt = format_prompt(
            TECH_LEAD_PROMPT,
            feature_request=feature_request,
            feature_slug=feature_slug
        )

        # M2: Plan mit echten Repo-Daten
        plan_content = f"""# Implementierungsplan: {feature_request}

## Status
✅ M2: Plan mit echten Repo-Scan-Daten

## 1. Repo-Überblick
- **Entry Point**: `{scan_result.entry_point or 'Nicht gefunden'}` ({scan_result.entry_point_lines} Zeilen)
- **Streamlit App**: {'Ja' if scan_result.has_streamlit else 'Nein'}
- **Pages/Features** ({len(scan_result.pages)}): {', '.join(scan_result.pages) if scan_result.pages else 'Keine'}
- **Funktionen** ({len(scan_result.functions)}): {', '.join(f['name'] for f in scan_result.functions[:5])}{'...' if len(scan_result.functions) > 5 else ''}
- **Cached Functions**: {', '.join(scan_result.cached_functions) if scan_result.cached_functions else 'Keine'}
- **Tests vorhanden**: {'Ja (' + scan_result.test_framework + ')' if scan_result.has_tests else 'Nein - muss erstellt werden!'}
- **Test-Dateien**: {', '.join(scan_result.test_files) if scan_result.test_files else 'Keine'}
- **Dependencies** ({len(scan_result.dependencies)}): {', '.join(scan_result.dependencies) if scan_result.dependencies else 'Keine'}
- **Dependency-Quelle**: {scan_result.dependency_source or 'Keine'}
- **Python-Dateien**: {len(scan_result.python_files)}
- **Repo-Größe**: {scan_result.repo_size_kb} KB

## 2. Contract
⚠️ Contract muss in `contracts/{feature_slug}.md` erstellt werden.
Siehe Contract-Template für Details.

## 3. Subtasks

### Backend
- [ ] Implementiere Feature-Logik
- [ ] Schreibe Unit Tests
- Akzeptanz: Tests grün, Contract erfüllt

### Frontend
- [ ] Baue UI für Feature
- [ ] Implementiere Error/Loading/Empty States
- Akzeptanz: UI nutzt Contract, keine Business-Logik im UI

### Tests
- [ ] Unit Tests für Backend
- [ ] Edge Cases abdecken
- Akzeptanz: Mindestens 80% Coverage für neue Logik

### Docs
- [ ] Update README falls nötig
- [ ] Inline-Kommentare für komplexe Logik
- Akzeptanz: "How to run" ist klar

## 4. Risiken/Edge Cases
- [Werden in M2+ analysiert]

## 5. How to run / test
```bash
# Python-Version: 3.10+
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 6. Definition of Done
- [ ] Alle Tests grün
- [ ] Contract eingehalten
- [ ] Code-Review bestanden
- [ ] Dokumentation aktualisiert

---
**Tech Lead Prompt (für M2+):**

{prompt}
"""

        plan_path = self.docs_path / f"plan_{feature_slug}.md"
        plan_path.write_text(plan_content, encoding="utf-8")
        return plan_path

    def _create_contract_template(self, feature_request: str, feature_slug: str) -> Path:
        """Erstellt das Contract-Template."""
        contract_content = f"""# Contract: {feature_request}

## Funktionen

### Haupt-Funktion
```python
def feature_function(param: Type) -> ReturnType:
    \"\"\"
    Beschreibung: Was macht diese Funktion?

    Args:
        param: Beschreibung des Parameters
            - Erlaubte Werte: [z.B. Enum('A', 'B', 'C') oder Range 0-100]
            - Format: [z.B. String, nicht leer]

    Returns:
        ReturnType: Beschreibung des Rückgabewerts
            - Struktur: [z.B. dict mit keys 'result', 'status']

    Raises:
        ValueError: Wenn param ungültig
        RuntimeError: Wenn Berechnung fehlschlägt

    Examples:
        >>> feature_function("valid_input")
        {{'result': 'success', 'status': 'ok'}}
    \"\"\"
    pass
```

## Datenmodelle

### Input Model
```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class InputModel:
    field1: str  # Erlaubt: nicht-leerer String
    field2: int  # Erlaubt: 0-100
    field3: Literal['option1', 'option2']  # Nur diese Werte
```

### Output Model
```python
@dataclass
class OutputModel:
    result: str
    status: Literal['success', 'error', 'warning']
    details: dict  # Optional: zusätzliche Infos
```

## Fehlerfälle

### Was passiert bei...
- **Leerem Input**: ValueError mit Message "Input darf nicht leer sein"
- **Ungültigem Wert**: ValueError mit Message "Wert muss zwischen X und Y liegen"
- **None/Null**: TypeError mit Message "None ist nicht erlaubt"
- **Berechnung schlägt fehl**: RuntimeError mit Details zum Fehler

### Welche Exceptions können auftreten?
- `ValueError`: Validierungsfehler
- `TypeError`: Falscher Typ
- `RuntimeError`: Interne Fehler

## UI-States

### Loading State
- Anzeige: Spinner mit Text "Berechne..."
- Wann: Während Funktion läuft
- Action: UI disabled während Loading

### Error State
- Anzeige: Rote Error-Box mit Fehlermeldung
- Wann: Exception aufgetreten
- Action: User kann Input korrigieren

### Empty State
- Anzeige: Info-Box "Noch keine Daten"
- Wann: Kein Input vorhanden
- Action: Hinweis wie User fortfahren kann

### Success State
- Anzeige: Grüne Success-Box mit Ergebnis
- Wann: Funktion erfolgreich abgeschlossen
- Action: Ergebnis anzeigen, weitere Actions erlauben

## Integration

### Wo wird das Feature eingebaut?
- Datei: `app.py`
- Seite: [Name der Seite, z.B. "Calculator"]
- Position: [z.B. "Neue Sektion unter Calculator-Results"]

### Wie wird es aufgerufen?
```python
# Beispiel UI-Code
if st.button("Feature ausführen"):
    with st.spinner("Berechne..."):
        try:
            result = feature_function(user_input)
            st.success(f"Ergebnis: {{result}}")
        except ValueError as e:
            st.error(f"Validierungsfehler: {{e}}")
        except Exception as e:
            st.error(f"Fehler: {{e}}")
```

## Validierung

### Input-Validierung (Backend)
```python
def validate_input(param: str) -> None:
    if not param:
        raise ValueError("Input darf nicht leer sein")
    if len(param) > 100:
        raise ValueError("Input zu lang (max 100 Zeichen)")
    # Weitere Validierungen...
```

### Output-Validierung (Tests)
```python
def test_output_structure():
    result = feature_function("valid_input")
    assert 'result' in result
    assert 'status' in result
    assert result['status'] in ['success', 'error', 'warning']
```

## Performance

### Erwartete Performance
- Ausführungszeit: < 1 Sekunde für normale Inputs
- Memory: < 100 MB
- Caching: Nutze @st.cache_data falls möglich

### Caching-Strategie
```python
@st.cache_data
def cached_feature_function(param: str) -> dict:
    # Schwere Berechnung hier
    return result
```

---

## ⚠️ WICHTIG: Dieses Contract muss ausgefüllt sein, BEVOR Backend-Phase startet!

Alle Platzhalter [in Klammern] müssen konkrete Werte haben.
"""

        contract_path = self.contracts_path / f"{feature_slug}.md"
        contract_path.write_text(contract_content, encoding="utf-8")
        return contract_path


def main():
    """Test-Funktion für M1."""
    agent = TechLeadAgent()
    result = agent.run("Füge Versicherungsvergleich hinzu")
    print("\n" + "=" * 80)
    print("🎉 M1 Complete! Generierte Dateien:")
    for key, path in result.items():
        print(f"  - {key}: {path}")


if __name__ == "__main__":
    main()
