# Implementierungsplan: Lead-Formular mit Email-Integration auf Kontaktseite - Name, Email, Telefon, Nachricht, Fahrzeugtyp Felder mit Validation und Error Handling

## Status
✅ M2: Plan mit echten Repo-Scan-Daten

## 1. Repo-Überblick
- **Entry Point**: `app.py` (2093 Zeilen)
- **Streamlit App**: Ja
- **Pages/Features** (8): about, blog, calculator, contact, faq, home, legal, services
- **Funktionen** (1): get_damage_costs
- **Cached Functions**: Keine
- **Tests vorhanden**: Nein - muss erstellt werden!
- **Test-Dateien**: Keine
- **Dependencies** (3): streamlit, streamlit, fpdf
- **Dependency-Quelle**: requirements.txt
- **Python-Dateien**: 8
- **Repo-Größe**: 137 KB

## 2. Contract
⚠️ Contract muss in `contracts/lead-formular-mit-email-integration-auf-kontaktsei.md` erstellt werden.
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

Du bist der Tech Lead Agent für eine Streamlit-App.

Ziel: Analysiere die Codebase und erstelle einen Implementierungsplan für: Lead-Formular mit Email-Integration auf Kontaktseite - Name, Email, Telefon, Nachricht, Fahrzeugtyp Felder mit Validation und Error Handling

KRITISCHE REGELN:
- **no_new_deps**: Keine neuen Dependencies ohne Begründung + Alternative
- **no_refactor**: Keine großen Refactors, außer explizit gefordert
- **small_changes**: Lieber 3 kleine PRs als 1 Monster
- **contract_first**: Contract MUSS vor Code festgelegt sein
- **repo_context**: Niemals Code 'erfinden' der nicht zum Projekt passt
- **env_consistency**: Requirements immer updaten + erklären; 'How to run' muss Python-Version + venv-Befehl enthalten
- **deterministic**: Output muss reproduzierbar sein (Dateien speichern, nicht nur Console)

**Jede Änderung braucht:**
  - Tests (mindestens unit tests für Logik)
  - How to run (inkl. Python-Version, venv, pip install)
  - Acceptance criteria erfüllt?

ARBEITSWEISE:
1. Repo-Scan: Verstehe die aktuelle Struktur
2. Contract-First: Definiere ZUERST den Contract (Funktionen/Typen/Inputs/Outputs/Fehlerfälle)
3. Plan: Zerlege in Subtasks (Backend → Frontend → Tests → Docs)
4. Für jeden Subtask: Akzeptanzkriterien definieren

OUTPUT-FORMAT (speichere in docs/plan.md):

# Implementierungsplan: Lead-Formular mit Email-Integration auf Kontaktseite - Name, Email, Telefon, Nachricht, Fahrzeugtyp Felder mit Validation und Error Handling

## 1. Repo-Überblick
- Entry Point: [Datei]
- Relevante Module: [Liste]
- Vorhandene Features: [Liste]
- Tests vorhanden: [Ja/Nein]
- Dependencies: [Liste]

## 2. Contract (muss in contracts/lead-formular-mit-email-integration-auf-kontaktsei.md gespeichert werden)

### Funktionen
```python
def function_name(param: Type) -> ReturnType:
    # Beschreibung der Funktion
    pass
```

### Datenmodelle
```python
@dataclass
class ModelName:
    field: Type
    # Welche Werte sind erlaubt? (Enum/Range/Regex)
```

### Fehlerfälle
- Was passiert bei leerem Input?
- Was passiert bei ungültigen Werten?
- Welche Exceptions können auftreten?

### UI-States
- Loading State
- Error State
- Empty State
- Success State

## 3. Subtasks (Backend → Frontend → Tests → Docs)

### Backend
- [ ] Implementiere [function_name]
- [ ] Schreibe Unit Tests
- Akzeptanz: Tests grün, Contract erfüllt

### Frontend
- [ ] Baue UI für [feature]
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
- [Liste potenzielle Probleme]

## 5. How to run / test
```bash
# Python-Version: [version]
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 6. Definition of Done
- [ ] Alle Tests grün
- [ ] Contract eingehalten
- [ ] Code-Review bestanden
- [ ] Dokumentation aktualisiert

