# Contract: Füge PDF-Export für Calculator hinzu

## Funktionen

### Haupt-Funktion
```python
def feature_function(param: Type) -> ReturnType:
    """
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
        {'result': 'success', 'status': 'ok'}
    """
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
            st.success(f"Ergebnis: {result}")
        except ValueError as e:
            st.error(f"Validierungsfehler: {e}")
        except Exception as e:
            st.error(f"Fehler: {e}")
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
