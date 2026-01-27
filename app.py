import streamlit as st
from datetime import datetime
import uuid
import json
from io import BytesIO

# PDF (reportlab ist bei dir verfügbar)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# Für Demo-Bilder + Text
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except Exception:
    PIL_OK = False


# -----------------------------
# ReturnGuard Handover – Streamlit Showcase
# v0.3: Wizard + PDF + Pitch Prefill
# -----------------------------

st.set_page_config(page_title="ReturnGuard – Übergabe-Check (Showcase)", layout="wide")

REQUIRED_SHOTS = [
    ("front", "Front"),
    ("rear", "Heck"),
    ("left", "Links"),
    ("right", "Rechts"),
    ("interior_front", "Innenraum vorne"),
    ("odometer", "Tacho / Kilometerstand"),
    ("wheels", "Felgen (optional)"),
]

# Wizard steps: required without wheels + optional wheels at end
WIZARD_STEPS = [x for x in REQUIRED_SHOTS if x[0] != "wheels"] + [("wheels", "Felgen (optional)")]

DAMAGE_CATEGORIES = ["Kratzer/Lack", "Delle", "Felge", "Scheibe", "Innenraum", "Sonstiges"]
POSITIONS = ["Front", "Heck", "Links", "Rechts", "Innen", "Unklar"]

WIZARD_HINTS = {
    "front": "Tipp: 3–4m Abstand, Auto komplett im Bild.",
    "rear": "Tipp: Kennzeichen sichtbar, kompletter Heckbereich.",
    "left": "Tipp: komplette Seite, Räder mit drauf.",
    "right": "Tipp: komplette Seite, Räder mit drauf.",
    "interior_front": "Tipp: Armaturen + Sitze vorne sichtbar.",
    "odometer": "Tipp: Zündung an, km-Stand gut lesbar.",
    "wheels": "Optional: 1–2 Bilder pro Seite reichen.",
}


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def ensure_state():
    if "vehicles" not in st.session_state:
        st.session_state.vehicles = {}
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
    if "selected_vehicle_id" not in st.session_state:
        st.session_state.selected_vehicle_id = None
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def vehicle_label(v: dict) -> str:
    plate = v.get("plate") or "—"
    brand = v.get("brand") or "—"
    model = v.get("model") or "—"
    vin = v.get("vin") or ""
    return f"{plate} · {brand} {model}" + (f" · VIN {vin}" if vin else "")


def get_vehicle_sessions(vehicle_id: str):
    return [s for s in st.session_state.sessions.values() if s["vehicle_id"] == vehicle_id]


def session_label(s: dict) -> str:
    t = "Übergabe" if s["type"] == "handover" else "Rückgabe"
    return f"{t} · {s['timestamp']} · {s.get('counterparty','').strip() or 'ohne Name'}"


def progress_required_photos(session: dict) -> tuple[int, int]:
    required_keys = [k for k, _ in REQUIRED_SHOTS if k != "wheels"]
    uploaded = sum(1 for k in required_keys if session["photos"].get(k))
    return uploaded, len(required_keys)


def is_optional(step_key: str) -> bool:
    return step_key == "wheels"


def step_has_photo(session: dict, step_key: str) -> bool:
    return bool(session["photos"].get(step_key))


def find_next_missing_required_index(session: dict) -> int:
    for i, (k, _) in enumerate(WIZARD_STEPS):
        if is_optional(k):
            continue
        if not step_has_photo(session, k):
            return i
    # all required done -> wheels step
    for i, (k, _) in enumerate(WIZARD_STEPS):
        if is_optional(k):
            return i
    return 0


# ---------- Export helpers (fix bytes -> metadata) ----------

def _json_safe(obj):
    if isinstance(obj, (bytes, bytearray)):
        return {"_type": "bytes", "len": len(obj)}
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    return obj


def _strip_image_bytes(data: dict) -> dict:
    data = json.loads(json.dumps(_json_safe(data), ensure_ascii=False))

    for sess in data.get("sessions", {}).values():
        photos = sess.get("photos", {}) or {}
        for key, items in photos.items():
            cleaned = []
            for it in items or []:
                size = None
                b = it.get("bytes")
                if isinstance(b, dict):
                    size = b.get("len")
                cleaned.append({"name": it.get("name"), "size_bytes": size})
            photos[key] = cleaned

        for dmg in sess.get("damages", []) or []:
            cleaned = []
            for it in dmg.get("photos", []) or []:
                size = None
                b = it.get("bytes")
                if isinstance(b, dict):
                    size = b.get("len")
                cleaned.append({"name": it.get("name"), "size_bytes": size})
            dmg["photos"] = cleaned

    return data


def export_state_as_json() -> str:
    raw = {
        "vehicles": st.session_state.vehicles,
        "sessions": st.session_state.sessions,
        "exported_at": now_iso(),
        "version": "showcase_v0.3_wizard_pdf_prefill",
        "export_mode": "metadata_only",
    }
    safe = _strip_image_bytes(raw)
    return json.dumps(safe, indent=2, ensure_ascii=False)


# ---------- PDF helpers ----------

def _pil_from_bytes(img_bytes: bytes):
    """Try to open image bytes with PIL. Returns PIL Image or None."""
    if not PIL_OK:
        return None
    try:
        im = Image.open(BytesIO(img_bytes))
        im = im.convert("RGB")
        return im
    except Exception:
        return None


def _draw_image_fit(c: canvas.Canvas, im_reader: ImageReader, x, y, w, h):
    """Draw image into a bounding box (w,h) keeping aspect ratio."""
    iw, ih = im_reader.getSize()
    if iw <= 0 or ih <= 0:
        return
    scale = min(w / iw, h / ih)
    dw = iw * scale
    dh = ih * scale
    dx = x + (w - dw) / 2
    dy = y + (h - dh) / 2
    c.drawImage(im_reader, dx, dy, dw, dh, preserveAspectRatio=True, mask='auto')


def build_session_pdf_bytes(vehicle: dict, session: dict) -> bytes:
    """
    Create a simple, pitch-friendly PDF:
    - Header: vehicle + session
    - Grid of key photos (front/rear/left/right/interior/odometer) if readable
    - Damages list + first damage photo thumbnails
    If an image format can't be decoded (e.g., HEIC), we list filename instead.
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    margin = 36
    y = H - margin

    # Header
    title = "ReturnGuard – Übergabeprotokoll"
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, title)
    y -= 22

    c.setFont("Helvetica", 10)
    t_label = "Übergabe" if session["type"] == "handover" else "Rückgabe"
    c.drawString(margin, y, f"Session: {t_label} · {session.get('timestamp','')}")
    y -= 14

    person = session.get("counterparty", "").strip() or "—"
    c.drawString(margin, y, f"Person: {person}")
    y -= 14

    plate = vehicle.get("plate", "—")
    brand = vehicle.get("brand", "—")
    model = vehicle.get("model", "—")
    vin = vehicle.get("vin", "").strip() or "—"
    c.drawString(margin, y, f"Fahrzeug: {plate} · {brand} {model} · VIN: {vin}")
    y -= 18

    # Photos grid
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Fotos (Pflicht / Kernansichten)")
    y -= 10

    grid_keys = [
        ("front", "Front"),
        ("rear", "Heck"),
        ("left", "Links"),
        ("right", "Rechts"),
        ("interior_front", "Innenraum"),
        ("odometer", "Tacho"),
    ]

    # Grid layout: 2 columns, 3 rows
    box_w = (W - 2 * margin - 12) / 2
    box_h = 115
    x1 = margin
    x2 = margin + box_w + 12

    y0 = y - 8
    c.setFont("Helvetica", 9)

    row = 0
    col = 0
    for key, label in grid_keys:
        bx = x1 if col == 0 else x2
        by = y0 - (row + 1) * (box_h + 18)

        # label
        c.setFont("Helvetica-Bold", 9)
        c.drawString(bx, by + box_h + 6, label)
        c.setFont("Helvetica", 8)

        stored = session.get("photos", {}).get(key) or []
        if stored:
            item = stored[0]
            name = item.get("name", "")
            img_bytes = item.get("bytes", b"")
            pil = _pil_from_bytes(img_bytes)
            if pil is not None:
                img_reader = ImageReader(pil)
                c.rect(bx, by, box_w, box_h, stroke=1, fill=0)
                _draw_image_fit(c, img_reader, bx, by, box_w, box_h)
            else:
                c.rect(bx, by, box_w, box_h, stroke=1, fill=0)
                c.drawString(bx + 6, by + box_h - 16, "Bildformat nicht lesbar")
                c.drawString(bx + 6, by + box_h - 30, f"Datei: {name}")
        else:
            c.rect(bx, by, box_w, box_h, stroke=1, fill=0)
            c.drawString(bx + 6, by + box_h - 16, "Kein Foto")

        col += 1
        if col == 2:
            col = 0
            row += 1

    # Move y to below grid
    y = y0 - 3 * (box_h + 18) - 10

    # Damages
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Schäden (manuell erfasst)")
    y -= 14

    damages = session.get("damages", []) or []
    c.setFont("Helvetica", 10)

    if not damages:
        c.drawString(margin, y, "— keine Schäden erfasst —")
        y -= 14
    else:
        for idx, d in enumerate(damages, start=1):
            if y < margin + 120:
                c.showPage()
                y = H - margin
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, y, "Schäden (Fortsetzung)")
                y -= 16
                c.setFont("Helvetica", 10)

            cat = d.get("category", "—")
            pos = d.get("position", "—")
            ts = d.get("timestamp", "")
            note = (d.get("note", "") or "").strip()

            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin, y, f"{idx}. {cat} · {pos} · {ts}")
            y -= 12

            c.setFont("Helvetica", 10)
            if note:
                c.drawString(margin, y, f"Notiz: {note}")
                y -= 12

            # damage photo thumbnails (max 2)
            photos = d.get("photos", []) or []
            thumb_w = (W - 2 * margin - 12) / 2
            thumb_h = 90
            bx1 = margin
            bx2 = margin + thumb_w + 12
            by = y - thumb_h - 6

            if photos:
                for j in range(min(2, len(photos))):
                    bx = bx1 if j == 0 else bx2
                    item = photos[j]
                    name = item.get("name", "")
                    img_bytes = item.get("bytes", b"")
                    pil = _pil_from_bytes(img_bytes)
                    c.rect(bx, by, thumb_w, thumb_h, stroke=1, fill=0)
                    if pil is not None:
                        img_reader = ImageReader(pil)
                        _draw_image_fit(c, img_reader, bx, by, thumb_w, thumb_h)
                    else:
                        c.setFont("Helvetica", 8)
                        c.drawString(bx + 6, by + thumb_h - 16, "Bildformat nicht lesbar")
                        c.drawString(bx + 6, by + thumb_h - 30, f"Datei: {name}")
                        c.setFont("Helvetica", 10)

                y = by - 12
            else:
                c.drawString(margin, y, "Keine Schadensfotos")
                y -= 12

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(margin, margin - 10, f"Erstellt am {now_iso()} · ReturnGuard Showcase v0.3")

    c.save()
    return buf.getvalue()


# ---------- Pitch / Demo helpers ----------

def make_demo_image_bytes(label: str, w=1280, h=720) -> bytes:
    """Creates a simple labeled PNG image for pitch sessions."""
    if not PIL_OK:
        # fallback: empty bytes (won't crash export, but preview won't show)
        return b""
    img = Image.new("RGB", (w, h), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    # Try default font
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    text = f"DEMO FOTO\n{label}\n{now_iso()}"
    draw.rectangle([40, 40, w - 40, h - 40], outline=(50, 50, 50), width=6)
    draw.text((80, 120), text, fill=(10, 10, 10), font=font, spacing=10)

    out = BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def pitch_prefill_fields():
    st.session_state["plate_in"] = "M-RG 2026"
    st.session_state["brand_in"] = "Audi"
    st.session_state["model_in"] = "A3 Sportback"
    st.session_state["vin_in"] = "WAUZZZDEMO1234567"
    st.session_state["note_in"] = "Pitch-Demo Fahrzeug (Pool / Mietwagen)"
    st.session_state["counterparty_in"] = "Max Mustermann"
    st.session_state["s_type_in"] = "handover"


def pitch_create_demo_vehicle_and_session():
    # Create vehicle
    vid = new_id("veh")
    v = {
        "id": vid,
        "plate": st.session_state.get("plate_in", "M-RG 2026"),
        "brand": st.session_state.get("brand_in", "Audi"),
        "model": st.session_state.get("model_in", "A3 Sportback"),
        "vin": st.session_state.get("vin_in", "WAUZZZDEMO1234567"),
        "note": st.session_state.get("note_in", "Pitch-Demo Fahrzeug"),
        "created_at": now_iso(),
    }
    st.session_state.vehicles[vid] = v
    st.session_state.selected_vehicle_id = vid

    # Create session
    sid = new_id("sess")
    s = {
        "id": sid,
        "vehicle_id": vid,
        "type": st.session_state.get("s_type_in", "handover"),
        "timestamp": now_iso(),
        "counterparty": st.session_state.get("counterparty_in", "Max Mustermann"),
        "photos": {k: [] for k, _ in REQUIRED_SHOTS},
        "damages": [],
        "closed": False,
        "wizard_step": 0,
    }

    # Add demo photos for all required shots
    for k, label in REQUIRED_SHOTS:
        if k == "wheels":
            # optional: leave empty or add 2 demo pics
            s["photos"][k] = [
                {"name": f"demo_{k}_1.png", "bytes": make_demo_image_bytes("Felge links (Demo)")},
                {"name": f"demo_{k}_2.png", "bytes": make_demo_image_bytes("Felge rechts (Demo)")},
            ]
        else:
            s["photos"][k] = [{"name": f"demo_{k}.png", "bytes": make_demo_image_bytes(label)}]

    # Add one demo damage
    dmg = {
        "id": new_id("dmg"),
        "timestamp": now_iso(),
        "category": "Kratzer/Lack",
        "position": "Front",
        "note": "Demo-Schaden: kleiner Kratzer am Stoßfänger",
        "photos": [{"name": "demo_damage_front.png", "bytes": make_demo_image_bytes("Schaden Front (Demo)")}],
    }
    s["damages"].append(dmg)

    st.session_state.sessions[sid] = s
    st.session_state.active_session_id = sid


# -----------------------------
# UI
# -----------------------------
ensure_state()

st.title("🛡️ ReturnGuard – Fahrzeug Übergabe-Check (Showcase)")
st.caption("Wizard-Fotos (1/6), Schadensdoku, Historie, Vorher/Nachher, PDF-Protokoll, Pitch-Buttons.")

with st.expander("⚡ Pitch-Modus (1 Klick statt Tipparbeit)", expanded=True):
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🧪 Felder vorausfüllen", use_container_width=True):
            pitch_prefill_fields()
            st.success("Felder sind vorausgefüllt.")
    with c2:
        if st.button("🚀 Demo-Fahrzeug + Demo-Session erzeugen", type="primary", use_container_width=True):
            pitch_prefill_fields()
            pitch_create_demo_vehicle_and_session()
            st.success("Demo ist erstellt. Rechts kannst du sofort zeigen + PDF ziehen.")
            st.rerun()
    with c3:
        st.caption("Für den Pitch: Klick auf Demo → gehe rechts auf Historie → PDF herunterladen. Fertig. 😄")

colA, colB = st.columns([1, 2], gap="large")

# ---------- Left column ----------
with colA:
    st.subheader("🚗 Fahrzeuge")

    with st.expander("➕ Neues Fahrzeug anlegen", expanded=True):
        plate = st.text_input("Kennzeichen*", placeholder="M-AB 1234", key="plate_in")
        brand = st.text_input("Marke*", placeholder="Audi", key="brand_in")
        model = st.text_input("Modell*", placeholder="A3 Sportback", key="model_in")
        vin = st.text_input("FIN/VIN (optional)", placeholder="WAUZZZ...", key="vin_in")
        note = st.text_area("Notiz (optional)", placeholder="z.B. Poolfahrzeug, Winterräder an Bord…", height=80, key="note_in")

        if st.button("Fahrzeug speichern", type="primary", use_container_width=True):
            if not plate.strip() or not brand.strip() or not model.strip():
                st.error("Bitte mindestens Kennzeichen, Marke und Modell ausfüllen.")
            else:
                vid = new_id("veh")
                st.session_state.vehicles[vid] = {
                    "id": vid,
                    "plate": plate.strip(),
                    "brand": brand.strip(),
                    "model": model.strip(),
                    "vin": vin.strip(),
                    "note": note.strip(),
                    "created_at": now_iso(),
                }
                st.session_state.selected_vehicle_id = vid
                st.success("Fahrzeug angelegt.")

    if not st.session_state.vehicles:
        st.info("Noch keine Fahrzeuge. Nutze oben den Pitch-Modus oder lege eins an.")
    else:
        vehicle_options = list(st.session_state.vehicles.keys())
        labels = {vid: vehicle_label(st.session_state.vehicles[vid]) for vid in vehicle_options}

        selected = st.selectbox(
            "Fahrzeug auswählen",
            options=vehicle_options,
            format_func=lambda vid: labels[vid],
            index=vehicle_options.index(st.session_state.selected_vehicle_id)
            if st.session_state.selected_vehicle_id in vehicle_options else 0
        )
        st.session_state.selected_vehicle_id = selected

        v = st.session_state.vehicles[selected]
        st.markdown("**Details**")
        st.write(f"- Kennzeichen: **{v['plate']}**")
        st.write(f"- Fahrzeug: **{v['brand']} {v['model']}**")
        if v.get("vin"):
            st.write(f"- VIN: `{v['vin']}`")
        if v.get("note"):
            st.write(f"- Notiz: {v['note']}")

        st.divider()
        st.subheader("🧾 Session starten")

        s_type = st.radio(
            "Session-Typ",
            options=["handover", "return"],
            format_func=lambda x: "Übergabe" if x == "handover" else "Rückgabe",
            horizontal=True,
            key="s_type_in",
        )
        counterparty = st.text_input("Übergabe an / Rückgabe von (optional)", placeholder="Name (Mitarbeiter/Kunde)", key="counterparty_in")

        if st.button("Neue Session starten", use_container_width=True):
            sid = new_id("sess")
            st.session_state.sessions[sid] = {
                "id": sid,
                "vehicle_id": selected,
                "type": s_type,
                "timestamp": now_iso(),
                "counterparty": (counterparty or "").strip(),
                "photos": {k: [] for k, _ in REQUIRED_SHOTS},
                "damages": [],
                "closed": False,
                "wizard_step": 0,
            }
            st.session_state.active_session_id = sid
            st.success("Session gestartet. Rechts kannst du jetzt den Check durchführen.")


# ---------- Right column ----------
with colB:
    vid = st.session_state.selected_vehicle_id

    if not vid:
        st.warning("Wähle links ein Fahrzeug aus oder nutze den Pitch-Modus.")
    else:
        vehicle = st.session_state.vehicles[vid]
        sessions_for_vehicle = get_vehicle_sessions(vid)
        sessions_for_vehicle_sorted = sorted(sessions_for_vehicle, key=lambda s: s["timestamp"], reverse=True)

        # Active session handling
        active_sid = st.session_state.get("active_session_id")
        if active_sid and active_sid in st.session_state.sessions:
            active = st.session_state.sessions[active_sid]
            if active["vehicle_id"] != vid:
                st.session_state.active_session_id = None
                active_sid = None

        st.subheader("📸 Ablauf")
        tabs = st.tabs(["1) Guided Check", "2) Historie", "3) Vorher/Nachher", "4) Export (Demo)"])

        # -----------------------------
        # Tab 1: Guided Check (WIZARD)
        # -----------------------------
        with tabs[0]:
            if not st.session_state.get("active_session_id") or st.session_state.sessions.get(st.session_state.get("active_session_id"), {}).get("vehicle_id") != vid:
                st.info("Starte links eine neue Session, um den Wizard zu nutzen.")
            else:
                sid = st.session_state.active_session_id
                session = st.session_state.sessions[sid]

                if "wizard_step" not in session:
                    session["wizard_step"] = 0

                t_label = "Übergabe" if session["type"] == "handover" else "Rückgabe"
                st.markdown(f"### {t_label} · {session['timestamp']}")
                if session.get("counterparty"):
                    st.caption(f"Person: {session['counterparty']}")

                total_required = len([1 for k, _ in WIZARD_STEPS if not is_optional(k)])
                done_required, _ = progress_required_photos(session)
                st.progress(done_required / total_required if total_required else 0.0)
                st.caption(f"Pflichtfotos: {done_required}/{total_required} erledigt (Felgen optional am Ende).")

                cJ1, cJ2 = st.columns([1, 1])
                with cJ1:
                    if st.button("➡️ Zum nächsten fehlenden Pflichtfoto", use_container_width=True, disabled=session["closed"]):
                        session["wizard_step"] = find_next_missing_required_index(session)
                        st.rerun()
                with cJ2:
                    if st.button("🔁 Schritt 1/6", use_container_width=True, disabled=session["closed"]):
                        session["wizard_step"] = 0
                        st.rerun()

                st.divider()

                # Clamp wizard step
                session["wizard_step"] = max(0, min(session["wizard_step"], len(WIZARD_STEPS) - 1))
                step_index = session["wizard_step"]
                step_key, step_label = WIZARD_STEPS[step_index]
                optional = is_optional(step_key)

                if not optional:
                    st.markdown(f"## Schritt {step_index + 1}/{total_required}: **{step_label}**")
                else:
                    st.markdown(f"## Optional: **{step_label}**")

                st.write(WIZARD_HINTS.get(step_key, ""))

                allow_multi = True if optional else False

                files = st.file_uploader(
                    f"Foto hochladen – {step_label}",
                    type=["jpg", "jpeg", "png", "heic"],
                    accept_multiple_files=allow_multi,
                    key=f"wiz_{sid}_{step_key}_{step_index}",
                    disabled=session["closed"],
                )

                if files:
                    if allow_multi:
                        session["photos"][step_key] = [{"name": f.name, "bytes": f.getvalue()} for f in files]
                        st.success(f"{len(files)} Datei(en) gespeichert.")
                    else:
                        # accept_multiple_files=False -> UploadedFile
                        f = files
                        session["photos"][step_key] = [{"name": f.name, "bytes": f.getvalue()}]
                        st.success("1 Datei gespeichert.")

                stored = session["photos"].get(step_key) or []
                if stored and stored[0].get("bytes"):
                    st.caption(f"Gespeichert: {len(stored)}")
                    cols = st.columns(min(4, len(stored)))
                    for i, item in enumerate(stored[:4]):
                        with cols[i % len(cols)]:
                            st.image(item["bytes"], caption=item.get("name", ""), use_container_width=True)
                else:
                    if optional:
                        st.info("Optional – kannst du überspringen.")
                    else:
                        st.warning("Noch kein Foto gespeichert.")

                navL, navM, navR = st.columns([1, 1, 1])
                with navL:
                    if st.button("⬅️ Zurück", use_container_width=True, disabled=session["closed"] or step_index == 0):
                        session["wizard_step"] = step_index - 1
                        st.rerun()

                with navM:
                    if st.button("⏭️ Überspringen", use_container_width=True, disabled=session["closed"] or not optional):
                        st.info("Optional übersprungen. Pflichtfotos reichen zum Abschluss.")
                with navR:
                    next_disabled = session["closed"]
                    if not optional and not step_has_photo(session, step_key):
                        next_disabled = True

                    if st.button("Weiter ➡️", use_container_width=True, disabled=next_disabled):
                        if step_index < len(WIZARD_STEPS) - 1:
                            session["wizard_step"] = step_index + 1
                            st.rerun()
                        else:
                            st.success("Wizard fertig. Unten kannst du Schäden erfassen oder abschließen.")

                st.divider()

                st.markdown("### Schäden hinzufügen (manuell)")
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        cat = st.selectbox("Kategorie", DAMAGE_CATEGORIES, key=f"cat_{sid}", disabled=session["closed"])
                    with c2:
                        pos = st.selectbox("Position", POSITIONS, key=f"pos_{sid}", disabled=session["closed"])
                    with c3:
                        note = st.text_input(
                            "Notiz (optional)",
                            key=f"note_{sid}",
                            placeholder="z.B. Kratzer ca. 5cm, Stoßfänger unten",
                            disabled=session["closed"],
                        )

                    dmg_files = st.file_uploader(
                        "Schadensfoto(s) hochladen",
                        type=["jpg", "jpeg", "png", "heic"],
                        accept_multiple_files=True,
                        key=f"dmg_{sid}",
                        disabled=session["closed"],
                    )

                    add = st.button("Schaden speichern", type="secondary", use_container_width=True, disabled=session["closed"])
                    if add:
                        if not dmg_files:
                            st.error("Bitte mindestens ein Schadensfoto hochladen.")
                        else:
                            dmg = {
                                "id": new_id("dmg"),
                                "timestamp": now_iso(),
                                "category": cat,
                                "position": pos,
                                "note": (note or "").strip(),
                                "photos": [{"name": f.name, "bytes": f.getvalue()} for f in dmg_files],
                            }
                            session["damages"].append(dmg)
                            st.success("Schaden gespeichert.")

                if session["damages"]:
                    st.markdown("#### Gespeicherte Schäden")
                    for d in session["damages"][::-1]:
                        with st.expander(f"{d['category']} · {d['position']} · {d['timestamp']}", expanded=False):
                            if (d.get("note") or "").strip():
                                st.write(d["note"])
                            phs = d.get("photos") or []
                            if phs and phs[0].get("bytes"):
                                cols = st.columns(min(4, len(phs)))
                                for i, ph in enumerate(phs[:4]):
                                    with cols[i % len(cols)]:
                                        st.image(ph["bytes"], caption=ph.get("name", ""), use_container_width=True)

                st.divider()
                cL, cR = st.columns([1, 1])
                with cL:
                    if st.button("✅ Session abschließen", type="primary", use_container_width=True, disabled=session["closed"]):
                        missing = []
                        for k, label in REQUIRED_SHOTS:
                            if k == "wheels":
                                continue
                            if not session["photos"].get(k):
                                missing.append(label)
                        if missing:
                            st.error("Noch fehlen Pflichtfotos: " + ", ".join(missing))
                            session["wizard_step"] = find_next_missing_required_index(session)
                            st.rerun()
                        else:
                            session["closed"] = True
                            st.success("Session abgeschlossen (gespeichert in Historie).")
                with cR:
                    if st.button("🗑️ Session verwerfen (Demo)", use_container_width=True):
                        del st.session_state.sessions[sid]
                        st.session_state.active_session_id = None
                        st.warning("Session verworfen.")
                        st.rerun()

        # -----------------------------
        # Tab 2: History (PDF HERE)
        # -----------------------------
        with tabs[1]:
            st.markdown("### Historie")
            if not sessions_for_vehicle_sorted:
                st.info("Noch keine Sessions für dieses Fahrzeug.")
            else:
                for s in sessions_for_vehicle_sorted:
                    with st.expander(session_label(s), expanded=False):
                        done_required, total_required = progress_required_photos(s)
                        st.caption(
                            f"Status: {'✅ abgeschlossen' if s['closed'] else '🟡 offen'} · "
                            f"Pflichtfotos {done_required}/{total_required} · Schäden: {len(s['damages'])}"
                        )

                        # PDF button
                        pdf_bytes = build_session_pdf_bytes(vehicle, s)
                        file_name = f"ReturnGuard_Protokoll_{vehicle.get('plate','Fahrzeug')}_{s.get('timestamp','')}.pdf".replace(" ", "_").replace(":", "-")
                        st.download_button(
                            "📄 PDF-Protokoll herunterladen",
                            data=pdf_bytes,
                            file_name=file_name,
                            mime="application/pdf",
                            use_container_width=True
                        )

                        preview_keys = ["front", "rear", "left", "right"]
                        pcols = st.columns(4)
                        for i, k in enumerate(preview_keys):
                            imgs = s["photos"].get(k) or []
                            if imgs and imgs[0].get("bytes"):
                                with pcols[i]:
                                    st.image(imgs[0]["bytes"], caption=k, use_container_width=True)

        # -----------------------------
        # Tab 3: Before/After compare
        # -----------------------------
        with tabs[2]:
            st.markdown("### Vorher/Nachher Vergleich")
            if len(sessions_for_vehicle_sorted) < 2:
                st.info("Für den Vergleich brauchst du mindestens zwei Sessions (z.B. Übergabe + Rückgabe).")
            else:
                options = [s["id"] for s in sessions_for_vehicle_sorted]
                labels = {s["id"]: session_label(s) for s in sessions_for_vehicle_sorted}

                c1, c2 = st.columns(2)
                with c1:
                    sid_a = st.selectbox("Session A (Vorher)", options=options, format_func=lambda x: labels[x], key="cmp_a")
                with c2:
                    sid_b = st.selectbox("Session B (Nachher)", options=options, format_func=lambda x: labels[x], key="cmp_b")

                sa = st.session_state.sessions[sid_a]
                sb = st.session_state.sessions[sid_b]

                st.caption("Tipp: Wähle A=Übergabe und B=Rückgabe.")
                shot_pairs = [
                    ("front", "Front"),
                    ("rear", "Heck"),
                    ("left", "Links"),
                    ("right", "Rechts"),
                    ("interior_front", "Innenraum"),
                    ("odometer", "Tacho"),
                ]

                for key, label in shot_pairs:
                    st.markdown(f"#### {label}")
                    ca, cb = st.columns(2)
                    with ca:
                        st.write("**Session A**")
                        imgs = sa["photos"].get(key) or []
                        if imgs and imgs[0].get("bytes"):
                            st.image(imgs[0]["bytes"], use_container_width=True)
                        else:
                            st.info("Kein Foto.")
                    with cb:
                        st.write("**Session B**")
                        imgs = sb["photos"].get(key) or []
                        if imgs and imgs[0].get("bytes"):
                            st.image(imgs[0]["bytes"], use_container_width=True)
                        else:
                            st.info("Kein Foto.")

                st.divider()
                st.markdown("#### Schäden (Listenvergleich)")
                cA, cB = st.columns(2)
                with cA:
                    st.write("**Session A – Schäden**")
                    if sa["damages"]:
                        for d in sa["damages"]:
                            st.write(f"- {d['category']} · {d['position']} ({d['timestamp']})")
                    else:
                        st.write("—")
                with cB:
                    st.write("**Session B – Schäden**")
                    if sb["damages"]:
                        for d in sb["damages"]:
                            st.write(f"- {d['category']} · {d['position']} ({d['timestamp']})")
                    else:
                        st.write("—")

        # -----------------------------
        # Tab 4: Export
        # -----------------------------
        with tabs[3]:
            st.markdown("### Export (Demo)")
            st.write("Exportiert werden **nur Metadaten** (keine Bild-Bytes), damit der Showcase stabil bleibt.")

            try:
                json_str = export_state_as_json()

                st.download_button(
                    "JSON Export herunterladen",
                    data=json_str.encode("utf-8"),
                    file_name="returnguard_handover_showcase.json",
                    mime="application/json",
                    use_container_width=True
                )

                with st.expander("JSON Vorschau", expanded=False):
                    st.code(json_str, language="json")

            except Exception as e:
                st.error("Export ist fehlgeschlagen (Demo-Schutz).")
                st.code(str(e))

st.divider()
st.caption("Showcase v0.3 – Wizard + PDF + Pitch Prefill. Nächster Schritt: Rollen/Cloud oder echter OCR-Scan in iOS.")
