# Backend Changes

## Modified Files
- `app.py`

## app.py
```diff
--- a/app.py+++ b/app.py@@ -1,6 +1,32 @@ import streamlit as st
+from fpdf import FPDF
 
 def get_damage_costs(vehicle_class):
     pass
 
+def export_to_pdf(damages: dict, vehicle_class: str, total: float) -> bytes:
+    """Exportiert Calculator als PDF."""
+    pdf = FPDF()
+    pdf.add_page()
+    pdf.set_font("Arial", size=12)
+
+    # Header
+    pdf.cell(200, 10, txt="ReturnGuard Schadensrechner", ln=True, align='C')
+    pdf.ln(10)
+
+    # Fahrzeugklasse
+    pdf.cell(0, 10, txt=f"Fahrzeugklasse: {vehicle_class}", ln=True)
+    pdf.ln(5)
+
+    # Schäden
+    pdf.cell(0, 10, txt="Schäden:", ln=True)
+    for part, severity in damages.items():
+        pdf.cell(0, 10, txt=f"  {part}: Stufe {severity}", ln=True)
+
+    pdf.ln(5)
+    pdf.cell(0, 10, txt=f"Gesamtkosten: {total:.2f} EUR", ln=True)
+
+    # Output als bytes
+    return pdf.output(dest='S').encode('latin1')
+
 # Rest der App...

```

## Review Notes

- **Was**: PDF-Export Funktion `export_to_pdf()` hinzugefügt
- **Warum**: Contract fordert PDF-Export für Calculator-Ergebnisse
- **Risiko**: fpdf Dependency muss in requirements.txt (ist bereits vorhanden). Encoding latin1 könnte bei Umlauten Probleme machen.
- **Test**: Test mit pytest: Mock damages dict, prüfe PDF-Header (%PDF), prüfe dass output bytes sind
- **Dependencies**: fpdf: PDF-Generierung (bereits in requirements.txt). Wird genutzt um Calculator-Ergebnisse als downloadbare PDF zu exportieren.
- **Negative Tests**: test_export_empty_damages() - ValueError bei leerem dict, test_export_invalid_vehicle_class() - ValueError bei ungültiger Klasse, test_export_negative_total() - ValueError bei negativen Kosten
