# Contract: Lead-Formular mit Email-Integration auf Kontaktseite

## Funktionen

### Haupt-Funktion: validate_lead_form
```python
def validate_lead_form(name: str, email: str, phone: str, message: str, vehicle_type: str) -> dict:
    """
    Validiert Lead-Formular Eingaben und gibt Validierungsergebnis zurück.

    Args:
        name: Vollständiger Name des Kunden
            - Erlaubte Werte: Nicht-leerer String, min 2 Zeichen, max 100 Zeichen
            - Format: Buchstaben, Leerzeichen, Bindestriche erlaubt

        email: Email-Adresse des Kunden
            - Erlaubte Werte: Gültige Email-Adresse
            - Format: Standard Email-Format (name@domain.tld)

        phone: Telefonnummer des Kunden
            - Erlaubte Werte: Deutsche Telefonnummer
            - Format: Optional +49, Leerzeichen/Bindestriche erlaubt

        message: Nachricht/Anfrage des Kunden
            - Erlaubte Werte: Nicht-leerer String, min 10 Zeichen, max 1000 Zeichen
            - Format: Freitext

        vehicle_type: Fahrzeugklasse für Anfrage
            - Erlaubte Werte: Kompaktklasse, Mittelklasse, Oberklasse, Luxusklasse
            - Format: Exakt einer der 4 Werte

    Returns:
        dict: Validierungsergebnis
            - Struktur: {'is_valid': bool, 'errors': dict[str, str]}
            - errors ist leer bei erfolgreicher Validierung
            - errors enthält Feld-Namen als Keys und Fehlermeldungen als Values

    Raises:
        TypeError: Wenn Parameter nicht vom Typ str sind

    Examples:
        >>> validate_lead_form("Max Müller", "max@test.de", "+49 176 123456", "Ich brauche Hilfe", "Mittelklasse")
        {'is_valid': True, 'errors': {}}

        >>> validate_lead_form("A", "invalid", "", "Hi", "Andere")
        {'is_valid': False, 'errors': {'name': 'Name zu kurz...', 'email': 'Ungültige Email...', ...}}
    """
    pass
```

### Hilfs-Funktion: sanitize_phone
```python
def sanitize_phone(phone: str) -> str:
    """
    Normalisiert Telefonnummer (entfernt Leerzeichen, Bindestriche).

    Args:
        phone: Rohe Telefoneingabe

    Returns:
        str: Bereinigte Telefonnummer (nur Zahlen und +)

    Examples:
        >>> sanitize_phone("+49 176 123-456")
        "+49176123456"
    """
    pass
```

## Datenmodelle

### Input Model: LeadFormData
```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class LeadFormData:
    name: str  # Min 2, Max 100 Zeichen
    email: str  # Gültige Email
    phone: str  # Min 5, Max 20 Zeichen
    message: str  # Min 10, Max 1000 Zeichen
    vehicle_type: Literal['Kompaktklasse', 'Mittelklasse', 'Oberklasse', 'Luxusklasse']
```

### Output Model: ValidationResult
```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: dict[str, str]  # Feld -> Fehlermeldung

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0
```

## Fehlerfälle

### Was passiert bei...
- **Leerem Name**: errors['name'] = "Name ist erforderlich"
- **Name zu kurz (< 2 Zeichen)**: errors['name'] = "Name muss mindestens 2 Zeichen haben"
- **Name zu lang (> 100 Zeichen)**: errors['name'] = "Name darf maximal 100 Zeichen haben"
- **Ungültige Email**: errors['email'] = "Bitte geben Sie eine gültige Email-Adresse ein"
- **Leere Email**: errors['email'] = "Email ist erforderlich"
- **Leeres Telefon**: errors['phone'] = "Telefonnummer ist erforderlich"
- **Telefon zu kurz (< 5 Zeichen)**: errors['phone'] = "Telefonnummer zu kurz"
- **Leere Nachricht**: errors['message'] = "Nachricht ist erforderlich"
- **Nachricht zu kurz (< 10 Zeichen)**: errors['message'] = "Nachricht muss mindestens 10 Zeichen haben"
- **Nachricht zu lang (> 1000 Zeichen)**: errors['message'] = "Nachricht darf maximal 1000 Zeichen haben"
- **Ungültiger Fahrzeugtyp**: errors['vehicle_type'] = "Bitte wählen Sie einen Fahrzeugtyp aus"
- **None/Null Werte**: TypeError mit Message "Alle Felder müssen vom Typ str sein"

### Welche Exceptions können auftreten?
- `TypeError`: Wenn Parameter nicht vom Typ str sind (nur bei Programmierfehlern)
- KEINE weiteren Exceptions - Validierungsfehler werden als dict zurückgegeben

## UI-States

### Initial State (Formular leer)
- Anzeige: Leeres Formular mit Platzhaltern
- Alle Felder aktiviert, Submit-Button aktiv
- Keine Fehler sichtbar

### Loading State (nach Submit)
- Anzeige: Spinner mit Text "Anfrage wird gesendet..."
- Wann: Während Validierung + optionale Email-Versand
- Action: Formular disabled, Submit-Button disabled

### Error State (Validierung fehlgeschlagen)
- Anzeige: Rote Fehlermeldungen unter betroffenen Feldern
- Wann: ValidationResult.is_valid = False
- Action: User kann fehlerhafte Felder korrigieren, Submit erneut versuchen
- Format: Fehler direkt unter dem jeweiligen Input-Feld

### Success State (Formular erfolgreich gesendet)
- Anzeige: Grüne Success-Box "Vielen Dank! Wir melden uns innerhalb von 24h bei Ihnen."
- Wann: Validierung erfolgreich + Daten gespeichert
- Action: Formular wird zurückgesetzt (alle Felder leer)

## Integration

### Wo wird das Feature eingebaut?
- Datei: `app.py`
- Seite: Contact Page (st.session_state.page == 'contact')
- Position: Neue Sektion "Lead-Formular" unter den bestehenden Kontaktdaten (nach Zeile 2027)

### Wie wird es aufgerufen?
```python
# In Contact Page Section (nach statischen Infos)
st.markdown("### 📝 Anfrage senden")

# Session State für Formular-Reset
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Formular nur zeigen wenn nicht gerade submitted
if not st.session_state.form_submitted:
    with st.form("lead_form"):
        name = st.text_input("Name *", placeholder="Max Mustermann")
        email = st.text_input("Email *", placeholder="max@beispiel.de")
        phone = st.text_input("Telefon *", placeholder="+49 176 12345678")
        vehicle_type = st.selectbox(
            "Fahrzeugklasse *",
            ['Kompaktklasse', 'Mittelklasse', 'Oberklasse', 'Luxusklasse']
        )
        message = st.text_area(
            "Ihre Nachricht *",
            placeholder="Beschreiben Sie Ihr Anliegen...",
            height=150
        )

        submitted = st.form_submit_button("Anfrage senden")

        if submitted:
            with st.spinner("Anfrage wird gesendet..."):
                # Validierung
                result = validate_lead_form(name, email, phone, message, vehicle_type)

                if result['is_valid']:
                    # Erfolg
                    st.session_state.form_submitted = True
                    st.rerun()
                else:
                    # Fehler anzeigen
                    for field, error_msg in result['errors'].items():
                        st.error(f"{error_msg}")

# Success State
if st.session_state.form_submitted:
    st.success("✅ Vielen Dank! Wir melden uns innerhalb von 24h bei Ihnen.")
    if st.button("Neue Anfrage"):
        st.session_state.form_submitted = False
        st.rerun()
```

## Validierung

### Input-Validierung (Backend)
```python
def validate_lead_form(name: str, email: str, phone: str, message: str, vehicle_type: str) -> dict:
    errors = {}

    # Name validieren
    if not name or not name.strip():
        errors['name'] = "Name ist erforderlich"
    elif len(name.strip()) < 2:
        errors['name'] = "Name muss mindestens 2 Zeichen haben"
    elif len(name.strip()) > 100:
        errors['name'] = "Name darf maximal 100 Zeichen haben"

    # Email validieren
    if not email or not email.strip():
        errors['email'] = "Email ist erforderlich"
    else:
        # Regex für Email-Validierung
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            errors['email'] = "Bitte geben Sie eine gültige Email-Adresse ein"

    # Telefon validieren
    phone_clean = sanitize_phone(phone)
    if not phone or not phone.strip():
        errors['phone'] = "Telefonnummer ist erforderlich"
    elif len(phone_clean) < 5:
        errors['phone'] = "Telefonnummer zu kurz"
    elif len(phone_clean) > 20:
        errors['phone'] = "Telefonnummer zu lang"

    # Nachricht validieren
    if not message or not message.strip():
        errors['message'] = "Nachricht ist erforderlich"
    elif len(message.strip()) < 10:
        errors['message'] = "Nachricht muss mindestens 10 Zeichen haben"
    elif len(message.strip()) > 1000:
        errors['message'] = "Nachricht darf maximal 1000 Zeichen haben"

    # Fahrzeugtyp validieren
    valid_types = ['Kompaktklasse', 'Mittelklasse', 'Oberklasse', 'Luxusklasse']
    if vehicle_type not in valid_types:
        errors['vehicle_type'] = "Bitte wählen Sie einen Fahrzeugtyp aus"

    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }
```

### Output-Validierung (Tests)
```python
def test_valid_form():
    result = validate_lead_form(
        "Max Müller",
        "max@test.de",
        "+49 176 123456",
        "Ich brauche Hilfe bei meiner Leasingrückgabe",
        "Mittelklasse"
    )
    assert result['is_valid'] == True
    assert len(result['errors']) == 0

def test_empty_name():
    result = validate_lead_form("", "max@test.de", "+49 176 123", "Test message here", "Mittelklasse")
    assert result['is_valid'] == False
    assert 'name' in result['errors']
```

## Performance

### Erwartete Performance
- Ausführungszeit: < 100ms für Validierung (synchron, kein API-Call)
- Memory: < 1 MB
- Caching: NICHT nötig (simple Validierung)

### Kein Caching erforderlich
Validierung ist stateless und sehr schnell - kein @st.cache_data nötig.

---

## Dependencies

### Neue Dependencies
KEINE - Nur Standard-Library (re für Email-Validierung)

### Bestehende Dependencies
- streamlit (bereits vorhanden)

## Tests (Guardrail #5: Negative Tests)

### Positive Tests
- ✅ Gültige Eingabe: Alle Felder korrekt ausgefüllt
- ✅ Grenzwerte: Name mit genau 2 Zeichen, Nachricht mit genau 10 Zeichen

### Negative Tests (Contract-Verletzungen)
- ❌ Leere Felder: Name, Email, Telefon, Nachricht jeweils leer
- ❌ Zu kurze Werte: Name 1 Zeichen, Nachricht 5 Zeichen
- ❌ Zu lange Werte: Name 101 Zeichen, Nachricht 1001 Zeichen
- ❌ Ungültige Email: "invalid", "test@", "@test.de", "test"
- ❌ Ungültiger Fahrzeugtyp: "Sportwagen", "", None
- ❌ Nur Leerzeichen: "   " in Name/Email/Telefon/Nachricht

---

## ✅ CONTRACT VOLLSTÄNDIG - Bereit für M3 Validierung!
