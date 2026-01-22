#!/usr/bin/env python3
"""
CLI für das Agent-System.

Usage:
    python run_agent.py "Füge Versicherungsvergleich hinzu"
"""

import sys
from pathlib import Path

# Füge agents/ zum Python Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from agents.tech_lead import TechLeadAgent
from agents.guardrails import print_guardrails_summary


def print_banner():
    """Druckt das Banner."""
    banner = """
╔════════════════════════════════════════════════════════════════════════╗
║                     ReturnGuard Agent System V1                        ║
║                    Tech Lead Orchestrator                              ║
╚════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_usage():
    """Druckt die Usage-Anleitung."""
    usage = """
Usage:
    python run_agent.py "<feature request>"
    python run_agent.py --guardrails  # Zeige alle Guardrails

Examples:
    python run_agent.py "Füge Versicherungsvergleich hinzu"
    python run_agent.py "Implementiere PDF-Export für Calculator"
    python run_agent.py "Füge Dark Mode hinzu"

Workflow:
    1. Tech Lead scannt Repo und erstellt Plan
    2. Contract-Template wird erstellt (muss ausgefüllt werden!)
    3. Contract wird validiert (Contract-First Enforcement)
    4. Patch wird erzeugt (Dry-Run, nur Diff)

Meilensteine:
    ✅ M1: Minimaler Orchestrator läuft
    ✅ M2: Repo-Scan verlässlich
    ✅ M3: Contract-First enforced
    ✅ M4: Patch-Erzeugung + Review (mit Guardrails)

Guardrails:
    3 Haupt + 6 Zusatz-Guardrails aktiv
    Siehe: python run_agent.py --guardrails
"""
    print(usage)


def main():
    """Haupt-Funktion."""
    print_banner()

    # Prüfe auf --guardrails Flag
    if "--guardrails" in sys.argv:
        print_guardrails_summary()
        sys.exit(0)

    # Prüfe Argumente
    if len(sys.argv) < 2:
        print("❌ Fehler: Feature Request fehlt!\n")
        print_usage()
        sys.exit(1)

    feature_request = " ".join(sys.argv[1:])

    # Validiere Feature Request
    if not feature_request.strip():
        print("❌ Fehler: Feature Request darf nicht leer sein!\n")
        print_usage()
        sys.exit(1)

    # Starte Tech Lead Agent
    try:
        agent = TechLeadAgent()
        result = agent.run(feature_request)

        # Erfolgs-Output
        print("\n" + "=" * 80)
        print("🎉 Agent-System abgeschlossen!")
        print("=" * 80)
        print("\n📁 Generierte Dateien:")
        for key, path in result.items():
            if key != "feature_slug":
                print(f"  ✓ {key}: {path}")

        print("\n📋 Nächste Schritte:")
        print(f"  1. Öffne contracts/{result['feature_slug']}.md")
        print("  2. Fülle das Contract-Template aus (siehe Platzhalter)")
        print("  3. Contract muss komplett sein bevor Backend-Phase startet!")
        print("\n  ⚠️  M2-M4 folgen: Repo-Scan, Contract-Enforcement, Patch-Erzeugung")

        print("\n💡 Tipp:")
        print("  - Contract definiert ALLE Funktionen, Typen, Fehlerfälle, UI-States")
        print("  - Je detaillierter der Contract, desto besser der generierte Code")
        print("  - Nutze die Beispiele im Template als Orientierung")

    except Exception as e:
        print(f"\n❌ Fehler beim Ausführen des Agent-Systems:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
