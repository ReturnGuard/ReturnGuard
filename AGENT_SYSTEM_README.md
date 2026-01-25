# ReturnGuard Agent System V1

**Tech Lead Orchestrator für strukturierte Feature-Entwicklung mit 9 Guardrails**

## Was ist das?

Ein Agent-System, das Feature-Entwicklung strukturiert und planbar macht:
- 📋 **Plan erstellen** mit Contract-First Design
- 🔧 **Backend/Frontend/Tests** koordiniert umsetzen
- ✅ **Review** mit PR-ready Output
- 🛡️ **9 Guardrails** für Sicherheit und Vorhersagbarkeit

**Wichtig:** V1 ist ein **Planer + Patch-Generator**, KEIN "autonomes System".
Du bleibst Boss, der Agent gibt dir saubere Vorschläge.

## Quickstart

```bash
# Agent starten
python run_agent.py "Füge Versicherungsvergleich hinzu"

# Guardrails anzeigen
python run_agent.py --guardrails

# Output: docs/plan_*.md + contracts/*.md + patch_*.md
```

## Workflow (V1)

```
1. Feature Request eingeben
   └─> python run_agent.py "Feature-Beschreibung"

2. Tech Lead erstellt:
   ├─> docs/plan_<feature>.md (Implementierungsplan mit echten Repo-Daten)
   └─> contracts/<feature>.md (Contract-Template)

3. DU füllst Contract aus:
   ├─> Funktionen definieren (Inputs/Outputs/Typen)
   ├─> Fehlerfälle festlegen
   └─> UI-States beschreiben

4. Erneut ausführen:
   └─> python run_agent.py "Feature-Beschreibung"

5. Contract-Validierung:
   ├─> Bei ungültig: BLOCKIERT mit klaren Fehlern
   └─> Bei gültig: Erzeugt Patch

6. Patch-Review:
   ├─> docs/patch_<feature>.md (unified diff + Review Notes)
   ├─> Prüfe Änderungen
   └─> Manuell anwenden (wenn OK)
```

## Meilensteine

| Meilenstein | Status | Beschreibung |
|-------------|--------|--------------|
| **M1** | ✅ DONE | Minimaler Orchestrator läuft (Plan + Contract-Template) |
| **M2** | ✅ DONE | Repo-Scan verlässlich (Entry Point, Tests, Dependencies) |
| **M3** | ✅ DONE | Contract-First enforced (kein Code ohne ausgefüllten Contract) |
| **M4** | ✅ DONE | Patch-Erzeugung + Review-Ausgabe (PR-ready mit Guardrails) |

## 🛡️ Guardrails (3 Haupt + 6 Zusatz)

### Haupt-Guardrails (M4)

**1. Output als PR-ready unified diff + Review-Notes**
- Alle Code-Änderungen als unified diff (wie git diff)
- Review-Notes: Was/Warum/Risiko/Test
- Enforced by: diff_generator.py

**2. Default dry-run (nur Diff)**
- Keine Files ändern ohne explizites Kommando
- Apply/Commit nur auf User-Befehl
- Enforced by: tech_lead.py (kein auto-apply)

**3. Strict scope (nur Contract-relevante Files)**
- Nur Contract-genannte oder M2-relevante Files anfassen
- Keine Neben-Refactors, keine "Verbesserungen"
- Enforced by: contract_validator.py + diff_generator.py

### Zusatz-Guardrails (Empfohlen)

**4. No Silent Magic**
- Bei Unklarheit blockieren & nachfragen, nicht interpretieren
- Jede Annahme explizit als ASSUMPTION kennzeichnen
- Action: BLOCK + nachfragen bei Unklarheit
- Enforced by: tech_lead.py (AssumptionTracker)

**5. Negative Tests verpflichtend**
- Pro Feature mind. 1 Test der bei Contract-Verletzung fehlschlägt
- Nicht nur Happy Path, auch test_invalid_input() etc.
- Action: Warnung wenn keine negative Tests vorhanden
- Enforced by: diff_generator.py (ReviewNotes)

**6. Dependency-Transparenz**
- Jede Dependency im Review kurz nennen: wofür & warum
- Keine "magischen" Imports
- Action: Review Notes müssen Dependencies erklären
- Enforced by: diff_generator.py (ReviewNotes)

**7. Performance-Hinweis**
- Repo-Scan / Validation > 500 ms → Warnung im Output (kein Abbruch)
- User awareness für lange Operationen
- Action: ⚠️ Warnung bei > 500ms
- Enforced by: repo_scan.py + contract_validator.py (@track_performance)

**8. Regel-Kollision = Stop**
- Bei Konflikten zwischen Contract, Repo-Scan oder Guardrails abbrechen
- Rückfrage stellen, keine Eigenentscheidung
- Action: STOP + Rückfrage an User
- Enforced by: tech_lead.py (detect_conflicts)

**9. Ownership bleibt beim Menschen**
- Output nur als Vorschlag (Diff + Notes)
- Apply/Merge bleibt immer beim Menschen
- Kein "auto-commit", kein "auto-push"
- Enforced by: Gesamtes System (kein apply-Modus)

## Dateistruktur

```
ReturnGuard-App/
├── agents/
│   ├── tech_lead.py               # Orchestrator (M1-M4)
│   ├── prompts.py                 # Zentrale Prompts + Regeln
│   ├── repo_scan.py               # M2: Scannt Codebase
│   ├── contract_validator.py      # M3: Validiert Contracts
│   ├── diff_generator.py          # M4: Erzeugt unified diffs
│   ├── guardrails.py              # 9 Guardrails + Utilities
│   └── roles/                     # (Platzhalter für Backend/Frontend/Testing)
├── contracts/
│   └── <feature>.md               # Contract pro Feature
├── docs/
│   ├── plan_<feature>.md          # Implementierungsplan (M2 Daten)
│   └── patch_<feature>.md         # Unified diff + Review (M4)
├── run_agent.py                   # CLI Entry Point
└── AGENT_SYSTEM_README.md         # Diese Datei
```

## Harte Regeln (in agents/prompts.py definiert)

Diese Regeln gelten für ALLE Agenten:

1. **no_new_deps**: Keine neuen Dependencies ohne Begründung + Alternative
2. **no_refactor**: Keine großen Refactors, außer explizit gefordert
3. **small_changes**: Lieber 3 kleine PRs als 1 Monster
4. **contract_first**: Contract MUSS vor Code festgelegt sein
5. **repo_context**: Niemals Code 'erfinden' der nicht zum Projekt passt
6. **env_consistency**: Requirements immer updaten; "How to run" muss Python-Version + venv enthalten
7. **deterministic**: Output muss reproduzierbar sein (Dateien speichern, nicht nur Console)

**Jede Änderung braucht:**
- Tests (mindestens unit tests für Logik)
- How to run (inkl. Python-Version, venv, pip install)
- Acceptance criteria erfüllt

## Contract-First Design (Kern des Systems)

**Ohne ausgefüllten Contract startet keine Backend-Phase!**

Contract definiert:
- ✅ **Funktionen**: Signaturen, Inputs, Outputs, Typen
- ✅ **Datenmodelle**: Dataclasses mit erlaubten Werten (Enums/Ranges)
- ✅ **Fehlerfälle**: Was passiert bei leerem/ungültigem Input?
- ✅ **UI-States**: Loading/Error/Empty/Success
- ✅ **Validierung**: Input/Output-Checks

**Warum?** Verhindert, dass Backend und Frontend aneinander vorbei bauen.

### Beispiel Contract:

```python
# Funktionen
def compare_insurance(damages: list[Damage]) -> ComparisonResult:
    """
    Args:
        damages: Liste von Damage(part, severity, cost)
            - erlaubte severity: Literal[0, 1, 2, 3, 4]
            - erlaubte parts: siehe DAMAGE_PARTS enum

    Returns:
        ComparisonResult(provider, monthly_rate, coverage)
            - provider: Literal['Allianz', 'HUK24', 'Ergo']
            - monthly_rate: float (0.0 - 1000.0)

    Raises:
        ValueError: wenn damages leer oder severity ungültig
    """

# Fehlerfälle
### Was passiert bei leerem Input?
- ValueError("Keine Schäden ausgewählt")

# UI-States
### Loading State
Spinner "Vergleiche Versicherungen..."

### Error State
st.error(f"Fehler: {e}")

### Empty State
st.info("Bitte wähle mindestens einen Schaden")

### Success State
st.success + Tabelle mit Ergebnissen
```

## Output-Format (M4)

```markdown
# Backend Changes

## Modified Files
- `app.py`

## app.py
```diff
--- a/app.py
+++ b/app.py
@@ -1,6 +1,32 @@
+def new_function():
+    pass
```

## Review Notes

- **Was**: PDF-Export Funktion `export_to_pdf()` hinzugefügt
- **Warum**: Contract fordert PDF-Export für Calculator-Ergebnisse
- **Risiko**: fpdf Dependency, Encoding latin1 bei Umlauten
- **Test**: pytest mit Mock, prüfe PDF-Header (%PDF)
- **Dependencies**: fpdf: PDF-Generierung (bereits in requirements.txt). Wird genutzt um Calculator-Ergebnisse als downloadbare PDF zu exportieren.
- **Negative Tests**: test_export_empty_damages() - ValueError bei leerem dict, test_export_invalid_vehicle_class() - ValueError bei ungültiger Klasse
```

## Beispiel-Session

```bash
$ python run_agent.py "Füge PDF-Export hinzu"

╔════════════════════════════════════════════════════════════════════════╗
║                     ReturnGuard Agent System V1                        ║
║                    Tech Lead Orchestrator                              ║
╚════════════════════════════════════════════════════════════════════════╝

🔍 Phase 0: Scanne Repository...
✅ Repo gescannt: app.py (1292 Zeilen)
   - Pages: 8
   - Funktionen: 1
   - Tests: Nein
   - Dependencies: 3

📋 Phase 1: Erstelle Implementierungsplan...
✅ Plan gespeichert: docs/plan_füge-pdf-export-hinzu.md

📝 Phase 2: Contract-Template erstellt...
✅ Contract-Template gespeichert: contracts/füge-pdf-export-hinzu.md
⚠️  WICHTIG: Contract muss ausgefüllt werden bevor Backend-Phase startet!

🔍 Phase 3: Validiere Contract (M3 - Contract-First Enforcement)...

❌ Contract ist UNGÜLTIG - Backend/Frontend/Testing werden blockiert!

🚫 Fehler (müssen behoben werden):
  - Contract enthält Platzhalter/TODOs: [in Klammern], [Name der Seite]

📝 Nächste Schritte:
  1. Öffne contracts/füge-pdf-export-hinzu.md
  2. Behebe alle obigen Fehler
  3. Entferne alle Platzhalter
  4. Fülle alle Sektionen vollständig aus
  5. Führe run_agent.py erneut aus

# --- Contract ausfüllen ---

$ python run_agent.py "Füge PDF-Export hinzu"

🔍 Phase 3: Validiere Contract...

✅ Contract ist gültig!

🔧 Phase 4: Erzeuge Patch-Vorschläge (M4 - Dry-Run)...
✅ Patch-Vorschlag gespeichert: docs/patch_füge-pdf-export-hinzu.md

📋 Patch-Zusammenfassung:
   - Modified Files: app.py
   - New Files: Keine
   - Review Notes: Was/Warum/Risiko/Test dokumentiert

💡 Nächste Schritte:
   1. Öffne docs/patch_*.md und prüfe Änderungen
   2. Unified diff zeigt genau was geändert würde
   3. Review Notes erklären Kontext
   4. Wenn OK: Manuell anwenden
   5. Tests laufen lassen

🛡️ M4 Guardrails aktiv:
   ✓ Output als PR-ready unified diff
   ✓ Default dry-run (keine Files geändert)
   ✓ Strict scope (nur Contract-relevante Files)
```

## Guardrails in Action

### Performance-Warnung (Guardrail #7)
```
⚠️ Performance-Hinweis: Repo-Scan dauerte 520ms (> 500ms Threshold)
```

### Dependency-Transparenz (Guardrail #6)
```
- **Dependencies**: fpdf: PDF-Generierung (bereits in requirements.txt).
  Wird genutzt um Calculator-Ergebnisse als downloadbare PDF zu exportieren.
```

### Negative Tests (Guardrail #5)
```
- **Negative Tests**:
  test_export_empty_damages() - ValueError bei leerem dict
  test_export_invalid_vehicle_class() - ValueError bei ungültiger Klasse
  test_export_negative_total() - ValueError bei negativen Kosten
```

### Assumptions (Guardrail #4)
```
⚠️ GETROFFENE ANNAHMEN:

1. ⚠️ ASSUMPTION:
   Was: Contract sagt 'app.py', nehme an das ist der Entry Point
   Warum: Repo-Scan hat app.py als wahrscheinlichsten Entry Point identifiziert
   Risiko: Falls app.py nicht der Entry Point ist, wird die Änderung am falschen Ort sein
```

### Regel-Kollision (Guardrail #8)
```
🚨 REGEL-KOLLISION ERKANNT:

Konflikt zwischen Contract und Repo-Scan:
  Contract: "main.py"
  Repo-Scan: "app.py"

❌ BLOCKIERT: Kann nicht automatisch lösen.
   Bitte entscheide welcher Wert korrekt ist.
```

## CLI Commands

```bash
# Haupt-Befehl
python run_agent.py "Feature-Beschreibung"

# Guardrails anzeigen
python run_agent.py --guardrails

# Contract validieren (standalone)
cd agents && python contract_validator.py <feature-slug>

# Repo-Scan (standalone)
cd agents && python repo_scan.py

# Diff-Generator (Demo)
cd agents && python diff_generator.py

# Guardrails (Demo)
cd agents && python guardrails.py
```

## FAQ

**Q: Kann der Agent die App eigenständig erweitern?**
A: Nein. Er erstellt Plan + Patches, aber DU bleibst Boss über mergen/testen/shippen.

**Q: Warum Contract-First?**
A: Verhindert dass Backend und Frontend aneinander vorbei bauen. Contract = Single Source of Truth.

**Q: Warum 9 Guardrails?**
A: Sicherheit und Vorhersagbarkeit. Verhindert "autonom neue Bugs erzeugen", erzwingt Transparenz und Performance-Awareness.

**Q: Was wenn der Agent Quatsch baut?**
A: Darum Review-Phase + "Du bleibst Boss". Agents sind Vorschläge, keine autonomen Entscheidungen. Alle Änderungen nur als Diff, nie direkt.

**Q: Wann blockiert das System?**
A:
- Contract ungültig (Platzhalter/TODOs)
- Contract fehlt
- Regel-Kollision (Contract vs Repo-Scan)
- Unklarheit (No Silent Magic)

**Q: Was ist mit echter Code-Generierung?**
A: Aktuell zeigt M4 Beispiel-Output im richtigen Format. Echte Code-Generierung erfordert Claude API Integration und wird in späterer Iteration hinzugefügt. Die Infrastruktur ist bereit.

## Credits

Design-Prinzipien basierend auf Feedback:
- Contract-First (verhindert Integration-Hölle)
- Nacheinander statt parallel (V1 Simplicity)
- Output in Dateien (reproduzierbar)
- Harte Regeln (keine Dependencies, keine Refactors, Tests Pflicht)
- Guardrails (3 Haupt + 6 Zusatz für Sicherheit)

---

**Version:** V1 (M1-M4 Complete mit 9 Guardrails)
**Last Updated:** 2026-01-22
**Branch:** claude/agent-system-v1-lgBfK
