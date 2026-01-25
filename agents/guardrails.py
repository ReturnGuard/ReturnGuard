"""
Guardrails Configuration - Harte Regeln für das Agent-System.

Definiert Haupt- und Zusatz-Guardrails die das System sicher und vorhersagbar machen.
"""

from typing import List, Optional
from dataclasses import dataclass
import time


# ============================================================================
# HAUPT-GUARDRAILS (M4)
# ============================================================================

MAIN_GUARDRAILS = {
    "1_pr_ready_output": {
        "title": "Output als PR-ready unified diff + Review-Notes",
        "description": "Alle Code-Änderungen als unified diff (wie git diff), "
                      "begleitet von Review-Notes (Was/Warum/Risiko/Test)",
        "enforced_by": "diff_generator.py",
        "violation": "Direkte File-Änderungen ohne diff"
    },
    "2_default_dry_run": {
        "title": "Default dry-run (nur Diff)",
        "description": "Keine Files ändern ohne explizites Kommando. "
                      "Apply/Commit nur auf User-Befehl.",
        "enforced_by": "tech_lead.py (kein auto-apply)",
        "violation": "Automatisches Anwenden von Patches"
    },
    "3_strict_scope": {
        "title": "Strict scope (nur Contract-relevante Files)",
        "description": "Nur Contract-genannte oder M2-relevante Files anfassen. "
                      "Keine Neben-Refactors, keine 'Verbesserungen'.",
        "enforced_by": "contract_validator.py + diff_generator.py",
        "violation": "Änderungen außerhalb Contract-Scope"
    }
}


# ============================================================================
# ZUSATZ-GUARDRAILS (Optional aber empfohlen)
# ============================================================================

ADDITIONAL_GUARDRAILS = {
    "4_no_silent_magic": {
        "title": "No Silent Magic",
        "description": "Bei Unklarheit, Mehrdeutigkeit oder impliziten Annahmen "
                      "blockieren und nachfragen, nicht interpretieren. "
                      "Jede Annahme im Output explizit als ASSUMPTION kennzeichnen.",
        "enforced_by": "Alle Agents (Backend/Frontend/Testing)",
        "violation": "Implizite Annahmen ohne Kennzeichnung",
        "action": "BLOCK + nachfragen bei Unklarheit"
    },
    "5_negative_tests_mandatory": {
        "title": "Negative Tests verpflichtend",
        "description": "Pro Feature mindestens ein Test der bei Contract-Verletzung "
                      "fehlschlägt (nicht nur Happy Path). "
                      "Z.B. test_invalid_input(), test_missing_param(), etc.",
        "enforced_by": "testing_agent.py",
        "violation": "Nur Happy-Path Tests ohne negative Cases",
        "action": "Warnung wenn keine negative Tests vorhanden"
    },
    "6_dependency_transparency": {
        "title": "Dependency-Transparenz",
        "description": "Jede genutzte Dependency (auch bestehende) im Review kurz nennen: "
                      "wofür & warum. Keine 'magischen' Imports.",
        "enforced_by": "Review Notes (diff_generator.py)",
        "violation": "Neue Dependencies ohne Erklärung",
        "action": "Review Notes müssen Dependencies erklären"
    },
    "7_performance_warning": {
        "title": "Performance-Hinweis",
        "description": "Repo-Scan / Validation > 500 ms → Warnung im Output (kein Abbruch). "
                      "User awareness für lange Operationen.",
        "enforced_by": "repo_scan.py + contract_validator.py",
        "violation": "Langsame Operationen ohne Warnung",
        "action": "⚠️ Warnung bei > 500ms"
    },
    "8_rule_collision_stop": {
        "title": "Regel-Kollision = Stop",
        "description": "Bei Konflikten zwischen Contract, Repo-Scan oder Guardrails "
                      "abbrechen und Rückfrage stellen, keine Eigenentscheidung.",
        "enforced_by": "tech_lead.py (Orchestrator)",
        "violation": "Automatische Konfliktlösung",
        "action": "STOP + Rückfrage an User",
        "examples": [
            "Contract sagt 'Datei A', Repo-Scan findet nur 'Datei B'",
            "Contract fordert Dependency X, aber requirements.txt hat Y",
            "Contract definiert Funktion foo(), Code hat bereits bar()"
        ]
    },
    "9_ownership": {
        "title": "Ownership bleibt beim Menschen",
        "description": "Output nur als Vorschlag (Diff + Notes). "
                      "Apply/Merge bleibt immer beim Menschen. "
                      "Kein 'auto-commit', kein 'auto-push'.",
        "enforced_by": "Gesamtes System (kein apply-Modus)",
        "violation": "Automatisches Committen/Pushen",
        "action": "Alle Änderungen nur als Diff, nie direkt"
    }
}


# ============================================================================
# PERFORMANCE TRACKING
# ============================================================================

@dataclass
class PerformanceMetrics:
    """Tracking für Performance-Guardrail #7."""
    operation: str
    duration_ms: float
    threshold_ms: float = 500.0

    @property
    def is_slow(self) -> bool:
        """Ist die Operation langsam (> threshold)?"""
        return self.duration_ms > self.threshold_ms

    def format_warning(self) -> str:
        """Formatiert Performance-Warnung."""
        if not self.is_slow:
            return ""

        return (f"⚠️ Performance-Hinweis: {self.operation} dauerte {self.duration_ms:.0f}ms "
                f"(> {self.threshold_ms:.0f}ms Threshold)")


def track_performance(operation: str, threshold_ms: float = 500.0):
    """
    Decorator für Performance-Tracking (Guardrail #7).

    Usage:
        @track_performance("Repo-Scan")
        def scan_repo():
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000

            metrics = PerformanceMetrics(operation, duration_ms, threshold_ms)
            if metrics.is_slow:
                print(f"\n{metrics.format_warning()}")

            return result
        return wrapper
    return decorator


# ============================================================================
# ASSUMPTIONS TRACKING (Guardrail #4)
# ============================================================================

@dataclass
class Assumption:
    """Eine Annahme die getroffen wurde."""
    what: str  # Was wurde angenommen?
    why: str  # Warum?
    risk: str  # Risiko wenn Annahme falsch?

    def format(self) -> str:
        """Formatiert als ASSUMPTION Block."""
        return f"""
⚠️ ASSUMPTION:
   Was: {self.what}
   Warum: {self.why}
   Risiko: {self.risk}
"""


class AssumptionTracker:
    """
    Trackt Annahmen für Guardrail #4 (No Silent Magic).

    Jede Annahme muss explizit gemacht werden.
    """

    def __init__(self):
        self.assumptions: List[Assumption] = []

    def add(self, what: str, why: str, risk: str):
        """Fügt eine Annahme hinzu."""
        self.assumptions.append(Assumption(what, why, risk))

    def has_assumptions(self) -> bool:
        """Gibt es Annahmen?"""
        return len(self.assumptions) > 0

    def format_all(self) -> str:
        """Formatiert alle Annahmen."""
        if not self.assumptions:
            return "✅ Keine Annahmen getroffen"

        lines = ["⚠️ GETROFFENE ANNAHMEN:"]
        for i, assumption in enumerate(self.assumptions, 1):
            lines.append(f"\n{i}. {assumption.format()}")

        return "\n".join(lines)


# ============================================================================
# CONFLICT DETECTION (Guardrail #8)
# ============================================================================

@dataclass
class RuleConflict:
    """Ein Konflikt zwischen Regeln/Daten."""
    source1: str  # Erste Quelle (z.B. "Contract")
    value1: str  # Wert aus Quelle 1
    source2: str  # Zweite Quelle (z.B. "Repo-Scan")
    value2: str  # Wert aus Quelle 2
    resolution: Optional[str] = None  # Wie lösen? (oder None = User fragen)

    def format(self) -> str:
        """Formatiert als Konflikt-Meldung."""
        msg = f"""
🚨 REGEL-KOLLISION ERKANNT:

Konflikt zwischen {self.source1} und {self.source2}:
  {self.source1}: "{self.value1}"
  {self.source2}: "{self.value2}"
"""
        if self.resolution:
            msg += f"\nVorgeschlagene Lösung:\n  {self.resolution}\n"
        else:
            msg += "\n❌ BLOCKIERT: Kann nicht automatisch lösen.\n"
            msg += "   Bitte entscheide welcher Wert korrekt ist.\n"

        return msg


def detect_conflicts(
    contract_value: str,
    repo_value: str,
    field_name: str
) -> Optional[RuleConflict]:
    """
    Erkennt Konflikte zwischen Contract und Repo-Scan (Guardrail #8).

    Returns:
        RuleConflict wenn Konflikt, sonst None
    """
    if contract_value != repo_value:
        return RuleConflict(
            source1="Contract",
            value1=contract_value,
            source2="Repo-Scan",
            value2=repo_value,
            resolution=None  # User muss entscheiden
        )

    return None


# ============================================================================
# GUARDRAILS SUMMARY
# ============================================================================

def print_guardrails_summary():
    """Druckt Übersicht aller Guardrails."""
    print("\n" + "=" * 80)
    print("🛡️ AGENT-SYSTEM GUARDRAILS")
    print("=" * 80)

    print("\n## Haupt-Guardrails (M4)")
    for key, guard in MAIN_GUARDRAILS.items():
        print(f"\n{key}. {guard['title']}")
        print(f"   {guard['description']}")
        print(f"   Enforced by: {guard['enforced_by']}")

    print("\n## Zusatz-Guardrails (Empfohlen)")
    for key, guard in ADDITIONAL_GUARDRAILS.items():
        print(f"\n{key}. {guard['title']}")
        print(f"   {guard['description']}")
        print(f"   Enforced by: {guard['enforced_by']}")
        print(f"   Action: {guard['action']}")

    print("\n" + "=" * 80)
    print("✅ Alle 9 Guardrails definiert und dokumentiert")
    print("=" * 80 + "\n")


# CLI Test
if __name__ == "__main__":
    print_guardrails_summary()

    # Test Performance Tracking
    print("\n📊 Test: Performance Tracking (Guardrail #7)")
    print("-" * 80)

    @track_performance("Test Operation", threshold_ms=100.0)
    def slow_operation():
        time.sleep(0.15)  # 150ms - sollte Warnung geben
        return "Done"

    result = slow_operation()
    print(f"Result: {result}")

    # Test Assumptions
    print("\n📊 Test: Assumption Tracking (Guardrail #4)")
    print("-" * 80)

    tracker = AssumptionTracker()
    tracker.add(
        what="Contract sagt 'app.py', nehme an das ist der Entry Point",
        why="Repo-Scan hat app.py als wahrscheinlichsten Entry Point identifiziert",
        risk="Falls app.py nicht der Entry Point ist, wird die Änderung am falschen Ort sein"
    )
    print(tracker.format_all())

    # Test Conflicts
    print("\n📊 Test: Conflict Detection (Guardrail #8)")
    print("-" * 80)

    conflict = detect_conflicts(
        contract_value="app.py",
        repo_value="main.py",
        field_name="entry_point"
    )
    if conflict:
        print(conflict.format())
