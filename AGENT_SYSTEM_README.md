# ReturnGuard Agent System V1

**Tech Lead Orchestrator für strukturierte Feature-Entwicklung**

## Was ist das?

Ein Agent-System, das Feature-Entwicklung strukturiert und planbar macht:
- 📋 **Plan erstellen** mit Contract-First Design
- 🔧 **Backend/Frontend/Tests** koordiniert umsetzen
- ✅ **Review** mit PR-ready Output

**Wichtig:** V1 ist ein **Planer + Patch-Generator**, KEIN "autonomes System".
Du bleibst Boss, der Agent gibt dir saubere Vorschläge.

## Quickstart

```bash
# Agent starten
python run_agent.py "Füge Versicherungsvergleich hinzu"

# Output: docs/plan_*.md + contracts/*.md werden erstellt
```

## Workflow (V1)

```
1. Feature Request eingeben
   └─> python run_agent.py "Feature-Beschreibung"

2. Tech Lead erstellt:
   ├─> docs/plan_<feature>.md (Implementierungsplan)
   └─> contracts/<feature>.md (Contract-Template)

3. DU füllst Contract aus:
   ├─> Funktionen definieren (Inputs/Outputs/Typen)
   ├─> Fehlerfälle festlegen
   └─> UI-States beschreiben

4. M2-M4: Backend → Frontend → Tests → Review
   └─> (Wird in nächsten Meilensteinen implementiert)
```

## Meilensteine

| Meilenstein | Status | Beschreibung |
|-------------|--------|--------------|
| **M1** | ✅ DONE | Minimaler Orchestrator läuft (Plan + Contract-Template) |
| **M2** | ⏳ TODO | Repo-Scan verlässlich (Entry Point, Tests, Dependencies) |
| **M3** | ⏳ TODO | Contract-First enforced (kein Code ohne ausgefüllten Contract) |
| **M4** | ⏳ TODO | Patch-Erzeugung + Review-Ausgabe (PR-ready) |

## Dateistruktur

```
ReturnGuard-App/
├── agents/
│   ├── tech_lead.py         # Orchestrator
│   ├── prompts.py            # Zentrale Prompts + Regeln
│   ├── roles/                # M2+: Backend, Frontend, Testing, Docs
│   └── repo_scan.py          # M2: Repo-Scanner
├── contracts/
│   └── <feature>.md          # Contract pro Feature
├── docs/
│   ├── plan_<feature>.md     # Implementierungsplan
│   ├── backend_changes.md    # M3: Backend Patches
│   ├── frontend_changes.md   # M3: Frontend Patches
│   ├── testing_results.md    # M3: Test-Ergebnisse
│   └── review.md             # M4: Final Review (PR-ready)
└── run_agent.py              # CLI Entry Point
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

# Datenmodelle
@dataclass
class Damage:
    part: str
    severity: Literal[0, 1, 2, 3, 4]
    cost: float

# UI-States
- Loading: Spinner "Vergleiche Versicherungen..."
- Error: st.error(f"Fehler: {e}")
- Empty: st.info("Bitte wähle mindestens einen Schaden")
- Success: st.success + Tabelle mit Ergebnissen
```

## M1 Status: Was funktioniert jetzt?

✅ **Funktioniert:**
- `python run_agent.py "Feature"` erzeugt Plan + Contract-Template
- Plan-Struktur mit Subtasks (Backend/Frontend/Tests/Docs)
- Contract-Template mit allen nötigen Sektionen
- Ausgabe in docs/ und contracts/

⏳ **Noch nicht:**
- Echter Repo-Scan (kommt in M2)
- Backend/Frontend/Testing Agents (kommen in M3)
- Review + Patch-Erzeugung (kommt in M4)

## Beispiel-Session

```bash
$ python run_agent.py "Füge Versicherungsvergleich hinzu"

╔════════════════════════════════════════════════════════════════════════╗
║                     ReturnGuard Agent System V1                        ║
║                    Tech Lead Orchestrator                              ║
╚════════════════════════════════════════════════════════════════════════╝

🚀 Tech Lead Agent startet für: 'Füge Versicherungsvergleich hinzu'
================================================================================

📋 Phase 1: Erstelle Implementierungsplan...
✅ Plan gespeichert: /home/user/ReturnGuard-App/docs/plan_fuge-versicherungsvergleich-hinzu.md

📝 Phase 2: Contract-Template erstellt...
✅ Contract-Template gespeichert: /home/user/ReturnGuard-App/contracts/fuge-versicherungsvergleich-hinzu.md
⚠️  WICHTIG: Contract muss ausgefüllt werden bevor Backend-Phase startet!

⏭️  Weitere Phasen (Backend/Frontend/Testing/Review) folgen in M2-M4

================================================================================
🎉 Agent-System abgeschlossen!
================================================================================

📁 Generierte Dateien:
  ✓ plan: /home/user/ReturnGuard-App/docs/plan_fuge-versicherungsvergleich-hinzu.md
  ✓ contract: /home/user/ReturnGuard-App/contracts/fuge-versicherungsvergleich-hinzu.md

📋 Nächste Schritte:
  1. Öffne contracts/fuge-versicherungsvergleich-hinzu.md
  2. Fülle das Contract-Template aus (siehe Platzhalter)
  3. Contract muss komplett sein bevor Backend-Phase startet!

  ⚠️  M2-M4 folgen: Repo-Scan, Contract-Enforcement, Patch-Erzeugung

💡 Tipp:
  - Contract definiert ALLE Funktionen, Typen, Fehlerfälle, UI-States
  - Je detaillierter der Contract, desto besser der generierte Code
  - Nutze die Beispiele im Template als Orientierung
```

## Nächste Schritte (M2-M4)

### M2: Repo-Scan
- `agents/repo_scan.py` implementieren
- Findet Entry Point (app.py)
- Listet relevante Module, Features
- Erkennt vorhandene Tests
- Scannt Dependencies aus requirements.txt

### M3: Contract-First Enforcement
- Prüft ob Contract ausgefüllt ist
- Blockiert Backend-Phase wenn Contract fehlt
- Implementiert Backend/Frontend/Testing Agents
- Erzeugt konkrete Code-Patches

### M4: Review + Patch-Erzeugung
- Tech Lead Review implementieren
- PR-ready Output: modified files, how to run, acceptance checklist
- Test-Ausführung integrieren
- Security-Checks (XSS, SQL-Injection, etc.)

## Warum so aufgebaut?

### ✅ Verhindert typische Agenten-Fallen:
1. **"UI hübsch, Logik kaputt"** → Contract-First zwingt Backend zuerst
2. **"Läuft bei mir"** → "How to run" mit Python-Version + venv ist Pflicht
3. **"Autonom neue Bugs"** → Review-Phase mit Security-Checks
4. **"Agents bauen gegeneinander"** → Contract definiert Interface

### ✅ V1 bleibt minimal:
- Keine Parallelität (Backend → Frontend → Tests sequenziell)
- Keine "Subagent-Spawns" (nur strukturierte Prompts)
- Keine fancy CLI (einfaches python run_agent.py)
- Output in Dateien (reproduzierbar, nicht nur Console)

### ✅ Du bleibst Boss:
- Agent gibt Vorschläge (Plan, Patches)
- DU entscheidest was gemerged wird
- DU füllst Contract aus (Agent kennt Business-Logic nicht)
- DU testest und shippst

## FAQ

**Q: Kann der Agent die App eigenständig erweitern?**
A: Nein. Er erstellt Plan + Patches, aber DU bleibst Boss über mergen/testen/shippen.

**Q: Warum Contract-First?**
A: Verhindert dass Backend und Frontend aneinander vorbei bauen. Contract = Single Source of Truth.

**Q: Warum sequenziell statt parallel?**
A: V1 Simplicity. Parallel kommt in V1.1 wenn V1 stabil läuft.

**Q: Brauche ich Claude API?**
A: Für V1: Nein (nur Templates). Für M2+: Ja (für echte Code-Generierung).

**Q: Was wenn der Agent Quatsch baut?**
A: Darum Review-Phase + "Du bleibst Boss". Agents sind Vorschläge, keine autonomen Entscheidungen.

## Credits

Basierend auf ChatGPT's Feedback:
> "Ja, das kannst du so bauen – aber nicht als 'eigenständig erweitert die App',
> sondern als Orchestrator der Plan + Patches erzeugt und du bleibst Boss."

Design-Prinzipien:
- Contract-First (verhindert Integration-Hölle)
- Nacheinander statt parallel (V1 Simplicity)
- Output in Dateien (reproduzierbar)
- Harte Regeln (keine Dependencies, keine Refactors, Tests Pflicht)

---

**Version:** V1 (M1 Complete, M2-M4 Pending)
**Last Updated:** 2026-01-22
**Branch:** claude/agent-system-v1-lgBfK
