"""
Diff Generator - Erzeugt PR-ready unified diffs.

M4 Guardrail: Output als unified diff, nicht direkt Files ändern.
"""

from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class FileDiff:
    """Ein unified diff für eine Datei."""
    file_path: str  # Relativer Pfad
    old_content: str
    new_content: str

    def to_unified_diff(self) -> str:
        """
        Erzeugt unified diff Format.

        Returns:
            Unified diff string (wie git diff)
        """
        import difflib

        old_lines = self.old_content.splitlines(keepends=True)
        new_lines = self.new_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{self.file_path}",
            tofile=f"b/{self.file_path}",
            lineterm=''
        )

        return ''.join(diff)


@dataclass
class ReviewNotes:
    """Review-Notes für Changes."""
    was: str  # Was wurde geändert?
    warum: str  # Warum diese Änderung?
    risiko: str  # Welche Risiken?
    test: str  # Wie testen?

    def to_markdown(self) -> str:
        """Formatiert als Markdown."""
        return f"""## Review Notes

- **Was**: {self.was}
- **Warum**: {self.warum}
- **Risiko**: {self.risiko}
- **Test**: {self.test}
"""


@dataclass
class PatchOutput:
    """Kompletter Patch-Output für eine Phase."""
    phase: str  # "Backend", "Frontend", "Testing"
    diffs: List[FileDiff]
    review_notes: ReviewNotes
    files_modified: List[str]
    files_created: List[str]

    def to_markdown(self) -> str:
        """
        Formatiert als PR-ready Markdown.

        Returns:
            Markdown mit Diffs + Review Notes
        """
        lines = [f"# {self.phase} Changes\n"]

        # Files modified
        if self.files_modified:
            lines.append("## Modified Files")
            for f in self.files_modified:
                lines.append(f"- `{f}`")
            lines.append("")

        # Files created
        if self.files_created:
            lines.append("## New Files")
            for f in self.files_created:
                lines.append(f"- `{f}`")
            lines.append("")

        # Diffs
        for diff in self.diffs:
            lines.append(f"## {diff.file_path}")
            lines.append("```diff")
            lines.append(diff.to_unified_diff())
            lines.append("```\n")

        # Review Notes
        lines.append(self.review_notes.to_markdown())

        return "\n".join(lines)


def create_example_patch() -> PatchOutput:
    """
    Erstellt Beispiel-Patch für M4 Demo.

    Zeigt wie Output aussehen würde.
    """
    # Beispiel: PDF-Export Function hinzufügen
    old_content = """import streamlit as st

def get_damage_costs(vehicle_class):
    pass

# Rest der App...
"""

    new_content = """import streamlit as st
from fpdf import FPDF

def get_damage_costs(vehicle_class):
    pass

def export_to_pdf(damages: dict, vehicle_class: str, total: float) -> bytes:
    \"\"\"Exportiert Calculator als PDF.\"\"\"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.cell(200, 10, txt="ReturnGuard Schadensrechner", ln=True, align='C')
    pdf.ln(10)

    # Fahrzeugklasse
    pdf.cell(0, 10, txt=f"Fahrzeugklasse: {vehicle_class}", ln=True)
    pdf.ln(5)

    # Schäden
    pdf.cell(0, 10, txt="Schäden:", ln=True)
    for part, severity in damages.items():
        pdf.cell(0, 10, txt=f"  {part}: Stufe {severity}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, txt=f"Gesamtkosten: {total:.2f} EUR", ln=True)

    # Output als bytes
    return pdf.output(dest='S').encode('latin1')

# Rest der App...
"""

    diff = FileDiff(
        file_path="app.py",
        old_content=old_content,
        new_content=new_content
    )

    notes = ReviewNotes(
        was="PDF-Export Funktion `export_to_pdf()` hinzugefügt",
        warum="Contract fordert PDF-Export für Calculator-Ergebnisse",
        risiko="fpdf Dependency muss in requirements.txt (ist bereits vorhanden). "
               "Encoding latin1 könnte bei Umlauten Probleme machen.",
        test="Test mit pytest: Mock damages dict, prüfe PDF-Header (%PDF), "
             "prüfe dass output bytes sind"
    )

    patch = PatchOutput(
        phase="Backend",
        diffs=[diff],
        review_notes=notes,
        files_modified=["app.py"],
        files_created=[]
    )

    return patch


# CLI Test
if __name__ == "__main__":
    print("🔍 M4 Patch Output Format - Beispiel\n")
    print("=" * 80)

    patch = create_example_patch()
    print(patch.to_markdown())

    print("\n" + "=" * 80)
    print("✅ Dies ist das Format für M4 Patch-Output")
    print("   - Unified diffs (PR-ready)")
    print("   - Review Notes (Was/Warum/Risiko/Test)")
    print("   - Dry-run by default (keine Files geändert)")
