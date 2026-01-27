import streamlit as st
from datetime import datetime
import uuid
import json
from io import BytesIO

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm

# Images (placeholder generation + safe conversions)
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except Exception:
    PIL_OK = False

# -----------------------------
# ReturnGuard Handover – Streamlit Showcase
# Single-file prototype (no backend). Data stored in st.session_state.
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

    # Prefill state for pitch (form defaults)
    if "prefill_vehicle" not in st.session_state:
        st.session_state.prefill_vehicle = {
            "plate": "",
            "brand": "",
            "model": "",
            "vin": "",
            "note": "",
        }
    if "prefill_session" not in st.session_state:
        st.session_state.prefill_session = {
            "type": "handover",
            "counterparty": "",
        }


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
    uploaded = 0
    for k in required_keys:
        if session["photos"].get(k):
            uploaded += 1
    return uploaded, len(required_keys)


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
        "version": "showcase_v0.3_wizard_pdf_pitch",
        "export_mode": "metadata_only",
    }
    safe = _strip_image_bytes(raw)
    return json.dumps(safe, indent=2, ensure_ascii=False)


# ---------- Wizard helpers ----------

def wizard_steps():
    main = [(k, l) for (k, l) in REQUIRED_SHOTS if k != "wheels"]
    optional = [("wheels", "Felgen (optional)")]
    return main + optional


def is_step_optional(step_key: str) -> bool:
    return step_key == "wheels"


def step_has_photo(session: dict, step_key: str) -> bool:
    return bool(session["photos"].get(step_key))


def find_next_missing_required_index(session: dict) -> int:
    steps = wizard_steps()
    for i, (k, _) in enumerate(steps):
        if is_step_optional(k):
            continue
        if not step_has_photo(session, k):
            return i
    for i, (k, _) in enumerate(steps):
        if is_step_optional(k):
            return i
    return 0


# ---------- Pitch / Demo helpers ----------

def make_placeholder_png_bytes(title: str, subtitle: str = "", size=(1280, 720)) -> bytes:
    """
    Generates a simple labeled PNG as bytes.
    Used to make 1-click demo sessions without uploading real images.
    """
    if not PIL_OK:
        # Minimal fallback: create an empty-ish PNG via a tiny trick (still requires PIL)
        # If PIL is not available, raise and we’ll skip demo images.
        raise RuntimeError("Pillow (PIL) not available; cannot generate placeholder images.")

    img = Image.new("RGB", size, (245, 247, 249))
    draw = ImageDraw.Draw(img)

    # Try a default font; on Streamlit Cloud this usually works
    try:
        font_title = ImageFont.truetype("DejaVuSans.ttf", 72)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 32)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Big header
    draw.rectangle([40, 40, size[0]-40, size[1]-40], outline=(30, 30, 30), width=6)
    draw.text((80, 140), title, fill=(20, 20, 20), font=font_title)
    if subtitle:
        draw.text((80, 240), subtitle, fill=(60, 60, 60), font=font_sub)

    # Footer
    draw.text((80, size[1]-120), "ReturnGuard Showcase – Demo Foto", fill=(90, 90, 90), font=font_sub)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def load_pitch_demo():
    """
    One-click: creates vehicle + a closed demo session with placeholder images + a damage.
    """
    # Vehicle
    vid = new_id("veh")
    v = {
        "id": vid,
        "plate": "M-RG 2026",
        "brand": "Audi",
        "model": "A4 Avant",
        "vin": "WAUZZZDEMO123456",
        "note": "Pitch-Demo: Poolfahrzeug / Übergabeprotokoll",
        "created_at": now_iso(),
    }
    st.session_state.vehicles[vid] = v
    st.session_state.selected_vehicle_id = vid

    # Session (handover)
    sid = new_id("sess")
    s = {
        "id": sid,
        "vehicle_id": vid,
        "type": "handover",
        "timestamp": now_iso(),
        "counterparty": "Max Mustermann",
        "photos": {k: [] for k, _ in REQUIRED_SHOTS},
        "damages": [],
        "closed": True,  # close it so it appears as a “done” record
        "wizard_step": 0,
    }

    # Fill photos with placeholders (required + optional wheels)
    if PIL_OK:
        for key, label in REQUIRED_SHOTS:
            png = make_placeholder_png_bytes(
                title=f"{label}",
                subtitle=f"{v['plate']} · {v['brand']} {v['model']}"
            )
            s["photos"][key] = [{"name": f"{key}.png", "bytes": png}]

        # Add one damage with 2 photos
        dmg_png1 = make_placeholder_png_bytes("Schaden: Kratzer", "Stoßfänger vorne rechts")
        dmg_png2 = make_placeholder_png_bytes("Detailaufnahme", "Kratzer ~4cm")
        s["damages"].append({
            "id": new_id("dmg"),
            "timestamp": now_iso(),
            "category": "Kratzer/Lack",
            "position": "Front",
            "note": "Pitch-Demo: Kratzer am Stoßfänger (vorn rechts).",
            "photos": [
                {"name": "damage_1.png", "bytes": dmg_png1},
                {"name": "damage_2.png", "bytes": dmg_png2},
            ],
        })
    else:
        # If no PIL, still create the vehicle and session without images
        s["closed"] = False

    st.session_state.sessions[sid] = s
    st.session_state.active_session_id = sid


def apply_form_prefill():
    """
    Prefills the manual forms with demo values, without auto-creating records.
    """
    st.session_state.prefill_vehicle = {
        "plate": "M-RG 2026",
        "brand": "Audi",
        "model": "A4 Avant",
        "vin": "WAUZZZDEMO123456",
        "note": "Pitch: schnelle Demo – später echte Daten",
    }
    st.session_state.prefill_session = {
        "type": "handover",
        "counterparty": "Max Mustermann",
    }


# ---------- PDF helpers ----------

def bytes_to_pil_image(img_bytes: bytes):
    if not PIL_OK:
        return None
    try:
        im = Image.open(BytesIO(img_bytes))
        # Normalize for reportlab
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        if im.mode == "RGBA":
            # Flatten alpha on white
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        return im
    except Exception:
        return None


def pil_to_png_bytes(im: "Image.Image") -> bytes:
    buf = BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def session_to_pdf_bytes(vehicle: dict, session: dict) -> bytes:
    """
    Creates a simple A4 PDF: header + key data + photo grid + damages list.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    page_w, page_h = A4

    margin = 18 * mm
    y = page_h - margin

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "ReturnGuard – Übergabeprotokoll (Showcase)")
    y -= 10 * mm

    # Vehicle + session info
    c.setFont("Helvetica", 10)
    lines = [
        f"Kennzeichen: {vehicle.get('plate','—')}",
        f"Fahrzeug: {vehicle.get('brand','—')} {vehicle.get('model','—')}",
        f"VIN: {vehicle.get('vin','—')}",
        f"Session: {'Übergabe' if session.get('type')=='handover' else 'Rückgabe'}",
        f"Datum/Uhrzeit: {session.get('timestamp','—')}",
        f"Person: {session.get('counterparty','') or '—'}",
        f"Status: {'abgeschlossen' if session.get('closed') else 'offen'}",
    ]
    for ln in lines:
        c.drawString(margin, y, ln)
        y -= 5 * mm

    y -= 4 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Pflichtfotos")
    y -= 7 * mm

    # Photo grid: 2 columns, 3 rows per page section (fits the main ones)
    # We'll include first image of each key
    keys = [k for k, _ in REQUIRED_SHOTS]  # includes wheels
    col_count = 2
    cell_w = (page_w - 2 * margin - 10 * mm) / col_count
    cell_h = 42 * mm
    gap_x = 10 * mm
    gap_y = 8 * mm

    def draw_photo_cell(x, y_top, label, img_bytes):
        # label
        c.setFont("Helvetica", 9)
        c.drawString(x, y_top, label)
        # image box
        box_y_top = y_top - 4 * mm
        box_h = cell_h - 6 * mm
        box_w = cell_w
        c.rect(x, box_y_top - box_h, box_w, box_h)

        if img_bytes:
            if PIL_OK:
                im = bytes_to_pil_image(img_bytes)
                if im:
                    # Resize to fit box while preserving aspect
                    im_w, im_h = im.size
                    scale = min(box_w / im_w, box_h / im_h)
                    new_w = int(im_w * scale)
                    new_h = int(im_h * scale)
                    im2 = im.resize((new_w, new_h))
                    png = pil_to_png_bytes(im2)
                    reader = ImageReader(BytesIO(png))
                    # center inside box
                    ix = x + (box_w - new_w) / 2
                    iy = (box_y_top - box_h) + (box_h - new_h) / 2
                    c.drawImage(reader, ix, iy, width=new_w, height=new_h, preserveAspectRatio=True, mask='auto')
                    return

            # fallback: cannot render -> just note
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(x + 2 * mm, box_y_top - 8 * mm, "(Bild konnte nicht gerendert werden)")

    # Draw photos
    x0 = margin
    cur_y = y

    i = 0
    for key in keys:
        label = dict(REQUIRED_SHOTS).get(key, key)
        img_list = session.get("photos", {}).get(key) or []
        img_bytes = img_list[0].get("bytes") if img_list else None

        col = i % col_count
        row = i // col_count
        x = x0 + col * (cell_w + gap_x)
        y_top = cur_y - row * (cell_h + gap_y)

        # new page if needed
        if y_top - cell_h < margin + 60 * mm:
            c.showPage()
            y_top = page_h - margin
            cur_y = y_top
            i = 0
            col = 0
            row = 0
            x = x0
            y = page_h - margin

            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, y, "Pflichtfotos (Fortsetzung)")
            y -= 7 * mm
            cur_y = y
            y_top = cur_y

        draw_photo_cell(x, y_top, label, img_bytes)
        i += 1

    # Damages section (new page if tight)
    c.showPage()
    y = page_h - margin
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Schäden")
    y -= 8 * mm

    damages = session.get("damages", []) or []
    if not damages:
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, "Keine Schäden erfasst.")
        y -= 6 * mm
    else:
        for d in damages:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin, y, f"{d.get('category','—')} · {d.get('position','—')} · {d.get('timestamp','—')}")
            y -= 5 * mm
            c.setFont("Helvetica", 9)
            note = d.get("note") or ""
            if note:
                c.drawString(margin, y, f"Notiz: {note[:120]}")
                y -= 5 * mm

            # Damage photos: up to 2 thumbnails
            photos = d.get("photos", []) or []
            thumb_w = 70 * mm
            thumb_h = 40 * mm
            x = margin
            for idx, ph in enumerate(photos[:2]):
                img_bytes = ph.get("bytes")
                c.rect(x, y - thumb_h, thumb_w, thumb_h)
                if img_bytes and PIL_OK:
                    im = bytes_to_pil_image(img_bytes)
                    if im:
                        im_w, im_h = im.size
                        scale = min(thumb_w / im_w, thumb_h / im_h)
                        new_w = int(im_w * scale)
                        new_h = int(im_h * scale)
                        im2 = im.resize((new_w, new_h))
                        png = pil_to_png_bytes(im2)
                        reader = ImageReader(BytesIO(png))
                        ix = x + (thumb_w - new_w) / 2
                        iy = (y - thumb_h) + (thumb_h - new_h) / 2
                        c.drawImage(reader, ix, iy, width=new_w, height=new_h, preserveAspectRatio=True, mask='auto')
                x += thumb_w + 10 * mm

            y -= (thumb_h + 8 * mm)

            if y < margin + 30 * mm:
                c.showPage()
                y = page_h - margin
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, y, "Schäden (Fortsetzung)")
                y -= 8 * mm

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(margin, 12 * mm, "Showcase: Dieses Dokument dient als Demo-Protokoll. V1 ohne KI-Schadenabgleich.")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


# -----------------------------
# UI
# -----------------------------
ensure_state()

st.title("🛡️ ReturnGuard – Fahrzeug Übergabe-Check (Showcase)")
st.caption("Wizard-Fotos + Schäden + Historie + Vorher/Nachher + PDF-Protokoll + Pitch-Demo (1 Klick).")

# Top pitch buttons
topL, topR = st.columns([1, 1])
with topL:
    if st.button("🚀 Pitch-Demo laden (1 Klick)", type="primary", use_container_width=True):
        load_pitch_demo()
        st.success("Pitch-Demo geladen: Fahrzeug + abgeschlossene Session + Fotos + Schaden.")
        st.rerun()
with topR:
    if st.button("✨ Felder vorfüllen (für manuelles Anlegen)", use_container_width=True):
        apply_form_prefill()
        st.success("Formularfelder vorgefüllt.")
        st.rerun()

colA, colB = st.columns([1, 2], gap="large")

# ---------- Left column ----------
with colA:
    st.subheader("🚗 Fahrzeuge")

    with st.expander("➕ Neues Fahrzeug anlegen", expanded=True):
        plate = st.text_input("Kennzeichen*", placeholder="M-AB 1234", value=st.session_state.prefill_vehicle["plate"])
        brand = st.text_input("Marke*", placeholder="Audi", value=st.session_state.prefill_vehicle["brand"])
        model = st.text_input("Modell*", placeholder="A3 Sportback", value=st.session_state.prefill_vehicle["model"])
        vin = st.text_input("FIN/VIN (optional)", placeholder="WAUZZZ...", value=st.session_state.prefill_vehicle["vin"])
        note = st.text_area("Notiz (optional)", placeholder="z.B. Poolfahrzeug, Winterräder an Bord…", height=80, value=st.session_state.prefill_vehicle["note"])

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
        st.info("Noch keine Fahrzeuge. Nutze oben den Pitch-Demo-Button oder lege links eins an.")
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

        # Prefill session fields
        s_type = st.radio(
            "Session-Typ",
            options=["handover", "return"],
            format_func=lambda x: "Übergabe" if x == "handover" else "Rückgabe",
            horizontal=True,
            index=0 if st.session_state.prefill_session["type"] == "handover" else 1
        )
        counterparty = st.text_input(
            "Übergabe an / Rückgabe von (optional)",
            placeholder="Name (Mitarbeiter/Kunde)",
            value=st.session_state.prefill_session["counterparty"]
        )

        if st.button("Neue Session starten", use_container_width=True):
            sid = new_id("sess")
            st.session_state.sessions[sid] = {
                "id": sid,
                "vehicle_id": selected,
                "type": s_type,
                "timestamp": now_iso(),
                "counterparty": counterparty.strip(),
                "photos": {k: [] for k, _ in REQUIRED_SHOTS},
                "damages": [],
                "closed": False,
                "wizard_step": 0,
            }
            st.session_state.active_session_id = sid
            st.success("Session gestartet. Rechts kannst du jetzt den Check durchführen.")
            st.rerun()


# ---------- Right column ----------
with colB:
    vid = st.session_state.selected_vehicle_id

    if not vid:
        st.warning("Wähle links ein Fahrzeug aus oder klicke oben auf „Pitch-Demo laden“.")
    else:
        sessions_for_vehicle = get_vehicle_sessions(vid)
        sessions_for_vehicle_sorted = sorted(sessions_for_vehicle, key=lambda s: s["timestamp"], reverse=True)

        # Active session handling (if vehicle changed, drop active)
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
                st.info("Starte links eine neue Session, um den geführten Check zu nutzen.")
            else:
                sid = st.session_state.active_session_id
                session = st.session_state.sessions[sid]

                if "wizard_step" not in session:
                    session["wizard_step"] = 0

                t_label = "Übergabe" if session["type"] == "handover" else "Rückgabe"
                st.markdown(f"### {t_label} · {session['timestamp']}")
                if session.get("counterparty"):
                    st.caption(f"Person: {session['counterparty']}")

                steps = wizard_steps()
                total_required = len([1 for k, _ in steps if not is_step_optional(k)])
                done_required, _ = progress_required_photos(session)

                st.progress(done_required / total_required if total_required else 0.0)
                st.caption(f"Pflichtfotos: {done_required}/{total_required} erledigt (Felgen optional am Ende).")

                cJ1, cJ2 = st.columns([1, 1])
                with cJ1:
                    if st.button("➡️ Zum nächsten fehlenden Pflichtfoto", use_container_width=True, disabled=session["closed"]):
                        session["wizard_step"] = find_next_missing_required_index(session)
                        st.rerun()
                with cJ2:
                    if st.button("🔁 Schritt zurücksetzen (auf 1/6)", use_container_width=True, disabled=session["closed"]):
                        session["wizard_step"] = 0
                        st.rerun()

                st.divider()

                if session["wizard_step"] < 0:
                    session["wizard_step"] = 0
                if session["wizard_step"] >= len(steps):
                    session["wizard_step"] = len(steps) - 1

                step_index = session["wizard_step"]
                step_key, step_label = steps[step_index]
                optional = is_step_optional(step_key)

                if not optional:
                    st.markdown(f"## Schritt {step_index+1}/{total_required}: **{step_label}**")
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
                        f = files[0] if isinstance(files, list) else files
                        if hasattr(f, "getvalue"):
                            session["photos"][step_key] = [{"name": f.name, "bytes": f.getvalue()}]
                            st.success("1 Datei gespeichert.")

                stored = session["photos"].get(step_key) or []
                if stored:
                    st.caption(f"Gespeichert: {len(stored)}")
                    cols = st.columns(min(4, len(stored)))
                    for i, item in enumerate(stored[:4]):
                        with cols[i % len(cols)]:
                            st.image(item["bytes"], caption=item["name"], use_container_width=True)
                else:
                    if optional:
                        st.info("Optional – kannst du überspringen.")
                    else:
                        st.warning("Noch kein Foto gespeichert.")

                navL, navM, navR = st.columns([1, 1, 1])
                with navL:
                    if st.button("⬅️ Zurück", use_container_width=True, disabled=session["closed"] or step_index == 0):
                        session["wizard_step"] = max(0, step_index - 1)
                        st.rerun()
                with navM:
                    if st.button("⏭️ Überspringen", use_container_width=True, disabled=session["closed"] or not optional):
                        st.info("Optional übersprungen. Du kannst die Session trotzdem abschließen, wenn Pflichtfotos vollständig sind.")
                with navR:
                    next_disabled = session["closed"]
                    if not optional and not step_has_photo(session, step_key):
                        next_disabled = True

                    if st.button("Weiter ➡️", use_container_width=True, disabled=next_disabled):
                        if step_index < len(steps) - 1:
                            session["wizard_step"] = step_index + 1
                            st.rerun()
                        else:
                            st.success("Wizard fertig. Unten kannst du Schäden erfassen oder die Session abschließen.")

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
                                "note": note.strip(),
                                "photos": [{"name": f.name, "bytes": f.getvalue()} for f in dmg_files],
                            }
                            session["damages"].append(dmg)
                            st.success("Schaden gespeichert.")

                if session["damages"]:
                    st.markdown("#### Gespeicherte Schäden")
                    for d in session["damages"][::-1]:
                        with st.expander(f"{d['category']} · {d['position']} · {d['timestamp']}", expanded=False):
                            if d.get("note"):
                                st.write(d["note"])
                            cols = st.columns(min(4, len(d["photos"])))
                            for i, ph in enumerate(d["photos"][:4]):
                                with cols[i % len(cols)]:
                                    st.image(ph["bytes"], caption=ph["name"], use_container_width=True)

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
                            st.rerun()
                with cR:
                    if st.button("🗑️ Session verwerfen (Demo)", use_container_width=True):
                        del st.session_state.sessions[sid]
                        st.session_state.active_session_id = None
                        st.warning("Session verworfen.")
                        st.rerun()

        # -----------------------------
        # Tab 2: History (PDF Export here)
        # -----------------------------
        with tabs[1]:
            st.markdown("### Historie")
            if not sessions_for_vehicle_sorted:
                st.info("Noch keine Sessions für dieses Fahrzeug.")
            else:
                vehicle = st.session_state.vehicles.get(vid, {})

                for s in sessions_for_vehicle_sorted:
                    with st.expander(session_label(s), expanded=False):
                        done_required, total_required = progress_required_photos(s)
                        st.caption(
                            f"Status: {'✅ abgeschlossen' if s['closed'] else '🟡 offen'} · "
                            f"Pflichtfotos {done_required}/{total_required} · Schäden: {len(s['damages'])}"
                        )

                        preview_keys = ["front", "rear", "left", "right"]
                        pcols = st.columns(4)
                        for i, k in enumerate(preview_keys):
                            imgs = s["photos"].get(k) or []
                            if imgs:
                                with pcols[i]:
                                    st.image(imgs[0]["bytes"], caption=k, use_container_width=True)

                        st.divider()
                        st.markdown("#### PDF-Protokoll")
                        try:
                            pdf_bytes = session_to_pdf_bytes(vehicle, s)
                            filename = f"ReturnGuard_Protokoll_{vehicle.get('plate','FZG')}_{s['id']}.pdf".replace(" ", "_")
                            st.download_button(
                                "📄 PDF herunterladen",
                                data=pdf_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error("PDF konnte nicht erzeugt werden.")
                            st.code(str(e))

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
                        if imgs:
                            st.image(imgs[0]["bytes"], use_container_width=True)
                        else:
                            st.info("Kein Foto.")
                    with cb:
                        st.write("**Session B**")
                        imgs = sb["photos"].get(key) or []
                        if imgs:
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

# Footer
st.divider()
if not PIL_OK:
    st.caption("Hinweis: Pillow (PIL) ist nicht verfügbar → Pitch-Demo erzeugt keine Demo-Bilder. Uploads funktionieren trotzdem.")
st.caption("Showcase v0.3 (Wizard + PDF + Pitch-Demo) – Next: Rollen (MA/Chef) + Scan-Simulation + Cloud-Speicher.")
