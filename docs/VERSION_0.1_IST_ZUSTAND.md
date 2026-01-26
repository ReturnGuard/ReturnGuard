# ReturnGuard - Version 0.1 IST-Zustand
## Investor Prototype Documentation

**Erstellt:** 2026-01-26
**Status:** Baseline für Weiterentwicklung
**Branch:** `claude/returnguard-investor-prototype-jOtsL`

---

## 1. Executive Summary

ReturnGuard ist eine Streamlit-basierte Web-App für den deutschen Markt, die Leasingnehmern bei der Fahrzeugrückgabe hilft. Die App verfügt über ein 3-View-System (Investor/B2C/B2B) mit Sidebar-Navigation.

---

## 2. Aktuelle Architektur

### 2.1 View-System
| View | Zielgruppe | Seiten |
|------|------------|--------|
| **Investor** | Business Stakeholder | About, Services, Legal |
| **B2C** | Privatkunden | Home, Calculator, FAQ, Blog, Contact, About, Legal |
| **B2B** | Firmenkunden/Flotten | Services, Contact, Legal |

### 2.2 Technologie-Stack
- **Frontend:** Streamlit (Python)
- **Styling:** 886 Zeilen Custom CSS
- **Hosting:** Streamlit Cloud (returnguard.streamlit.app)
- **Dependencies:** streamlit, fpdf

---

## 3. Implementierte Features (v0.1)

### 3.1 Schadensrechner (Calculator)
- 20 Fahrzeugbereiche bewertbar (Außen + Innen)
- 5 Schadensstufen (0-4)
- 4 Fahrzeugklassen mit Preis-Multiplikatoren
- Dynamische Kostenberechnung
- Ersparnis-Prognose (60% Reduzierung)

### 3.2 Lead-Formular (Contact)
- Validierte Eingabefelder (Name, Email, Telefon)
- Schadens-Checkboxen (6 Kategorien)
- Optionale SVG-Auto-Grafik
- Foto-Upload (max 5 Bilder)
- **HINWEIS:** Kein Email-Versand implementiert!

### 3.3 Investor-Dashboard
- 4 KPIs: 1.200+ Fälle, 2.500€ Ersparnis, 98% Erfolg, 14 Screening-Punkte
- 14-Punkte Screening-Katalog
- 3 Referenzfälle mit dokumentierter Ersparnis

### 3.4 Content-Seiten
- FAQ mit 10 Fragen
- Blog mit Checkliste und 6 Artikel-Vorschauen
- About/Vision Seite
- Services Übersicht
- Legal (Impressum, Datenschutz, AGB)

### 3.5 UX/Design
- Responsive Design (Mobile + Desktop)
- Floating CTAs (Telefon, WhatsApp, Calculator)
- Social Proof Banner
- Testimonials (6 Kundenstimmen)
- Partner-Logos (TÜV, DEKRA, DAV, VDA)

---

## 4. Pakete/Pricing (aktuell dargestellt)

| Paket | Preis | Leistungen |
|-------|-------|------------|
| Basis | 99€ | Grundcheck, 20 Fotos, PDF-Bericht, 48h |
| Standard | 199€ | Umfassende Prüfung, 50 Fotos, 1h Beratung, 24h |
| Premium | 299€ | Rechtliche Prüfung, 2h Anwalt, 24/7 Support |
| VIP | 999€ | Full-Service, Vor-Ort bundesweit, Garantie, Manager |

---

## 5. LÜCKEN-ANALYSE: Geschäftsmodell vs. Darstellung

### 5.1 Geplantes Geschäftsmodell (laut Briefing)

**Revenue Streams:**
1. **Lead-Generierung → Verkauf an Werkstätten/Aufbereiter**
2. **Gutachter-Provisionen** (Schadensbewertung)
3. **Anwaltsvermittlung** (Streitfälle → Verkehrsrecht)
4. **B2B Flottenmanagement**

**Positionierung:** Vermittlungsplattform (aus Haftung)

### 5.2 Aktuelle Darstellung (v0.1)

**Problem:** Die App stellt ReturnGuard als **Beratungsunternehmen** dar, nicht als **Vermittlungsplattform**.

| Aspekt | Geplant | Aktuell (v0.1) | Gap |
|--------|---------|----------------|-----|
| Lead → Werkstätten | Revenue Stream | Nicht erwähnt | FEHLT |
| Lead → Aufbereiter | Revenue Stream | Nicht erwähnt | FEHLT |
| Anwaltsvermittlung | Revenue Stream | Nur am Rande | SCHWACH |
| Haftungsfreistellung | Kernstrategie | Nicht kommuniziert | FEHLT |
| Revenue-Übersicht für Investoren | Dashboard | Nur KPIs | FEHLT |
| Werkstatt-Netzwerk | USP | Nicht erwähnt | FEHLT |
| Aufbereiter-Netzwerk | USP | Nicht erwähnt | FEHLT |

---

## 6. Nicht implementierte Use Cases

### 6.1 Primäre Revenue-Generatoren (FEHLEN)
- [ ] **Werkstatt-Matching:** Leads von Kunden → Werkstätten annehmen Reparaturaufträge
- [ ] **Aufbereiter-Matching:** Leads → Aufbereiter für Innen-/Außenreinigung
- [ ] **Anwalts-Matching:** Streitfälle → Fachanwälte für Verkehrsrecht
- [ ] **Revenue-Dashboard für Investoren:** Wo kommt das Geld her?

### 6.2 Plattform-Features (FEHLEN)
- [ ] Werkstatt/Aufbereiter-Ansicht (B2B Dienstleister)
- [ ] Angebots-Management (Werkstätten sehen Leads, geben Angebote ab)
- [ ] Provision-Tracking
- [ ] Vertragsabwicklung (als Vermittler)

### 6.3 Investor-Relevante Metriken (FEHLEN)
- [ ] CAC (Customer Acquisition Cost)
- [ ] LTV (Lifetime Value)
- [ ] Lead-Conversion-Rate
- [ ] Durchschnittliche Provision pro Lead
- [ ] Werkstatt-/Aufbereiter-Pool-Größe
- [ ] Geografische Abdeckung

---

## 7. Empfohlene Prioritäten

### Phase 1: Investor-Story vervollständigen
1. Revenue-Streams klar darstellen
2. Unit Economics visualisieren
3. Marktpotenzial zeigen

### Phase 2: Plattform-Charakter zeigen
1. Werkstatt/Aufbereiter-Flow (Mock)
2. Lead-Verteilung visualisieren
3. Provision-Modell erklären

### Phase 3: Zusätzliche Use Cases
1. Streitfall-Management → Anwaltsvermittlung
2. B2B Flottenmanagement-Dashboard
3. Smart Repair vs. Vollreparatur Empfehlungen

---

## 8. Technische Schulden

- Email-Integration fehlt (Formulare speichern nichts)
- Kein Backend/Datenbank
- Keine Authentifizierung
- Keine echte Lead-Verwaltung
- SVG-Diagramm auf Safari Mobile deaktiviert

---

## 9. Dateien (v0.1)

```
/home/user/ReturnGuard/
├── app.py                 # Haupt-App (2.824 Zeilen)
├── requirements.txt       # streamlit, fpdf
├── agents/                # Feature-Development-Pipeline
├── contracts/             # Contract-First Design
├── docs/                  # Dokumentation
└── .devcontainer/         # Dev Environment
```

---

*Dokumentation erstellt für Weiterentwicklung als Investor-Prototyp.*
