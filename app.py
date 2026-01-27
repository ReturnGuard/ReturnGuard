import streamlit as st
from datetime import datetime
import uuid
import json
from io import BytesIO
import base64
import html as html_lib

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except Exception:
    PIL_OK = False


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
    if "pitch_vehicle_id" not in st.session_state:
        st.session_state.pitch_vehicle_id = None


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
    for i, (k, _) in enumerate(WIZARD_STEPS):
        if is_optional(k):
            return i
    return 0


# ---------- Export helpers (bytes -> metadata) ----------

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
        "version": "showcase_v0.3c_before_after_protocol",
        "export_mode": "metadata_only",
    }
    safe = _strip_image_bytes(raw)
    return json.dumps(safe, indent=2, ensure_ascii=False)


# ---------- Demo images ----------

def make_demo_image_bytes(label: str, w=1280, h=720) -> bytes:
    if not PIL_OK:
        return b""
    img = Image.new("RGB", (w, h), (240, 240, 240))
    draw = ImageDraw.Draw(img)
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


# ---------- Pitch prefill ----------

def pitch_prefill_fields():
    st.session_state["plate_in"] = "M-RG 2026"
    st.session_state["brand_in"] = "Audi"
    st.session_state["model_in"] = "A3 Sportback"
    st.session_state["vin_in"] = "WAUZZZDEMO1234567"
    st.session_state["note_in"] = "Pitch-Demo Fahrzeug (Pool / Mietwagen)"
    st.session_state["counterparty_in"] = "Max Mustermann"
    st.session_state["s_type_in"] = "handover"


def _ensure_pitch_vehicle() -> str:
    """
    Ensure there is ONE pitch vehicle that both sessions attach to.
    """
    if st.session_state.pitch_vehicle_id and st.session_state.pitch_vehicle_id in st.session_state.vehicles:
        return st.session_state.pitch_vehicle_id

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
    st.session_state.pitch_vehicle_id = vid
    return vid


def _create_demo_session(vehicle_id: str, session_type: str, label_prefix: str, add_extra_damage: bool) -> str:
    sid = new_id("sess")
    s = {
        "id": sid,
        "vehicle_id": vehicle_id,
        "type": session_type,
        "timestamp": now_iso(),
        "counterparty": st.session_state.get("counterparty_in", "Max Mustermann"),
        "photos": {k: [] for k, _ in REQUIRED_SHOTS},
        "damages": [],
        "closed": True,          # demo sessions are closed
        "wizard_step": 0,
    }

    # Photos
    for k, label in REQUIRED_SHOTS:
        if k == "wheels":
            s["photos"][k] = [
                {"name": f"{label_prefix}_{k}_1.png", "bytes": make_demo_image_bytes(f"{label_prefix} Felge links")},
                {"name": f"{label_prefix}_{k}_2.png", "bytes": make_demo_image_bytes(f"{label_prefix} Felge rechts")},
            ]
        else:
            s["photos"][k] = [{"name": f"{label_prefix}_{k}.png", "bytes": make_demo_image_bytes(f"{label_prefix} {label}")}]

    # Base damage (both can have one, so it's realistic)
    base_dmg = {
        "id": new_id("dmg"),
        "timestamp": now_iso(),
        "category": "Kratzer/Lack",
        "position": "Front",
        "note": f"{label_prefix}: kleiner Kratzer am Stoßfänger (Demo)",
        "photos": [{"name": f"{label_prefix}_damage_front.png", "bytes": make_demo_image_bytes(f"{label_prefix} Schaden Front")}],
    }
    s["damages"].append(base_dmg)

    # Extra damage only on AFTER to show delta
    if add_extra_damage:
        extra = {
            "id": new_id("dmg"),
            "timestamp": now_iso(),
            "category": "Felge",
            "position": "Rechts",
            "note": "NEU: Felgenschaden (Demo) – sichtbar nach Rückgabe",
            "photos": [{"name": "after_damage_wheel.png", "bytes": make_demo_image_bytes("NACHHER Schaden Felge")}],
        }
        s["damages"].append(extra)

    st.session_state.sessions[sid] = s
    return sid


def pitch_create_before():
    pitch_prefill_fields()
    vid = _ensure_pitch_vehicle()
    sid = _create_demo_session(vehicle_id=vid, session_type="handover", label_prefix="VORHER", add_extra_damage=False)
    st.session_state.selected_vehicle_id = vid
    st.session_state.active_session_id = sid


def pitch_create_after():
    pitch_prefill_fields()
    vid = _ensure_pitch_vehicle()
    sid = _create_demo_session(vehicle_id=vid, session_type="return", label_prefix="NACHHER", add_extra_damage=True)
    st.session_state.selected_vehicle_id = vid
    st.session_state.active_session_id = sid


# ---------- Protocol (HTML download) ----------

def _b64_img_tag(img_bytes: bytes, max_width_px=520) -> str:
    if not img_bytes:
        return ""
    b64 = base64.b64encode(img_bytes).decode("ascii")
    return f'<img src="data:image/png;base64,{b64}" style="max-width:{max_width_px}px;width:100%;border:1px solid #ddd;border-radius:8px;" />'


def build_session_protocol_html(vehicle: dict, session: dict) -> str:
    plate = html_lib.escape(vehicle.get("plate", "—"))
    brand = html_lib.escape(vehicle.get("brand", "—"))
    model = html_lib.escape(vehicle.get("model", "—"))
    vin = html_lib.escape((vehicle.get("vin") or "—"))
    note = html_lib.escape((vehicle.get("note") or "").strip())

    t_label = "Übergabe" if session.get("type") == "handover" else "Rückgabe"
    timestamp = html_lib.escape(session.get("timestamp", ""))
    person = html_lib.escape((session.get("counterparty") or "—").strip() or "—")

    grid_keys = [
        ("front", "Front"),
        ("rear", "Heck"),
        ("left", "Links"),
        ("right", "Rechts"),
        ("interior_front", "Innenraum"),
        ("odometer", "Tacho"),
    ]

    def first_img_bytes(key: str):
        arr = session.get("photos", {}).get(key) or []
        if not arr:
            return b""
        return arr[0].get("bytes") or b""

    grid_items = []
    for key, label in grid_keys:
        img = first_img_bytes(key)
        img_html = _b64_img_tag(img, max_width_px=420) if img else '<div class="empty">Kein Foto</div>'
        grid_items.append(f"""
            <div class="card">
              <div class="card-title">{html_lib.escape(label)}</div>
              {img_html}
            </div>
        """)

    damages = session.get("damages", []) or []
    dmg_blocks = []
    if not damages:
        dmg_blocks.append('<div class="muted">— keine Schäden erfasst —</div>')
    else:
        for i, d in enumerate(damages, start=1):
            cat = html_lib.escape(d.get("category", "—"))
            pos = html_lib.escape(d.get("position", "—"))
            ts = html_lib.escape(d.get("timestamp", ""))
            dnote = html_lib.escape((d.get("note") or "").strip())

            photos = d.get("photos", []) or []
            photo_htmls = []
            for ph in photos[:2]:
                img = ph.get("bytes") or b""
                if img:
                    photo_htmls.append(_b64_img_tag(img, max_width_px=420))
            photos_html = "".join(photo_htmls) if photo_htmls else '<div class="muted">Keine Schadensfotos</div>'

            dmg_blocks.append(f"""
                <div class="damage">
                  <div class="damage-title">{i}. {cat} · {pos} · {ts}</div>
                  {"<div class='muted'>Notiz: " + dnote + "</div>" if dnote else ""}
                  <div class="damage-photos">{photos_html}</div>
                </div>
            """)

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>ReturnGuard Protokoll</title>
<style>
  body {{ font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial; margin: 28px; color:#111; }}
  .header {{ display:flex; justify-content:space-between; align-items:flex-start; gap:20px; }}
  h1 {{ margin:0 0 6px 0; font-size:20px; }}
  .meta {{ font-size:12px; line-height:1.6; }}
  .badge {{ display:inline-block; padding:4px 10px; border-radius:999px; background:#f2f2f2; font-size:12px; }}
  .grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:14px; margin-top:16px; }}
  .card {{ border:1px solid #e5e5e5; border-radius:12px; padding:10px; }}
  .card-title {{ font-weight:700; margin-bottom:8px; font-size:13px; }}
  .empty {{ border:1px dashed #ccc; border-radius:10px; padding:18px; text-align:center; color:#666; }}
  .section-title {{ margin-top:18px; font-weight:800; }}
  .muted {{ color:#666; font-size:12px; }}
  .damage {{ border:1px solid #e5e5e5; border-radius:12px; padding:10px; margin-top:10px; }}
  .damage-title {{ font-weight:800; font-size:13px; margin-bottom:6px; }}
  .damage-photos {{ display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:10px; }}
  .footer {{ margin-top:18px; font-size:11px; color:#666; border-top:1px solid #eee; padding-top:10px; }}
  @media print {{
    body {{ margin: 10mm; }}
    .damage, .card {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>ReturnGuard – Übergabeprotokoll</h1>
      <div class="badge">{html_lib.escape(t_label)}</div>
      <div class="meta">
        <div><b>Datum/Zeit:</b> {timestamp}</div>
        <div><b>Person:</b> {person}</div>
        <div><b>Fahrzeug:</b> {plate} · {brand} {model}</div>
        <div><b>VIN:</b> {vin}</div>
        {f"<div><b>Notiz:</b> {note}</div>" if note else ""}
      </div>
    </div>
    <div class="meta" style="text-align:right;">
      <div><b>Session-ID:</b> {html_lib.escape(session.get("id",""))}</div>
      <div><b>Fahrzeug-ID:</b> {html_lib.escape(vehicle.get("id",""))}</div>
    </div>
  </div>

  <div class="section-title">Fotos (Kernansichten)</div>
  <div class="grid">
    {''.join(grid_items)}
  </div>

  <div class="section-title">Schäden (manuell erfasst)</div>
  {''.join(dmg_blocks)}

  <div class="footer">
    Erstellt am {html_lib.escape(now_iso())} · ReturnGuard Showcase v0.3c · Tipp: Im Browser „Drucken“ → „Als PDF speichern“.
  </div>
</body>
</html>
"""
    return html


# -----------------------------
# UI
# -----------------------------
ensure_state()

st.title("🛡️ ReturnGuard – Fahrzeug Übergabe-Check (Showcase)")
st.caption("Wizard-Fotos (1/6), Historie, Vorher/Nachher, Protokoll-Download, Pitch-Buttons (Vorher/Nachher).")

with st.expander("⚡ Pitch-Modus (Vorher/Nachher in 2 Klicks)", expanded=True):
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])

    with c1:
        if st.button("🧪 Felder vorausfüllen", use_container_width=True):
            pitch_prefill_fields()
            st.success("Felder sind vorausgefüllt.")

    with c2:
        if st.button("🚀 Demo VORHER (Übergabe)", type="primary", use_container_width=True):
            pitch_create_before()
            st.success("VORHER erstellt. Jetzt Tab 3 oder Historie zeigen.")
            st.rerun()

    with c3:
        if st.button("🚀 Demo NACHHER (Rückgabe)", type="primary", use_container_width=True):
            pitch_create_after()
            st.success("NACHHER erstellt (mit zusätzlichem Schaden).")
            st.rerun()

    with c4:
        st.caption("Pitch-Ablauf: VORHER klicken → NACHHER klicken → Tab 3 Vergleich → Historie → Protokolle ziehen.")

colA, colB = st.columns([1, 2], gap="large")

# ---------- Left column ----------
with colA:
    st.subheader("🚗 Fahrzeuge")

    with st.expander("➕ Neues Fahrzeug anlegen", expanded=True):
        plate = st.text_input("Kennzeichen*", placeholder="M-AB 1234", key="plate_in")
        brand = st.text_input("Marke*", placeholder="Audi", key="brand_in")
        model = st.text_input("Modell*", placeholder="A3 Sportback", key="model_in")
        vin = st.text_input("FIN/VIN (optional)", placeholder="WAUZZZ...", key="vin_in")
        note = st.text_area("Notiz (optional)", placeholder="z.B. Poolfahrzeug…", height=80, key="note_in")

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
        counterparty = st.text_input("Übergabe an / Rückgabe von (optional)", placeholder="Name", key="counterparty_in")

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

        st.subheader("📸 Ablauf")
        tabs = st.tabs(["1) Guided Check", "2) Historie", "3) Vorher/Nachher", "4) Export (Demo)"])

        # Tab 1: Wizard (kurz gehalten – Fokus Pitch)
        with tabs[0]:
            active_sid = st.session_state.get("active_session_id")
            if not active_sid or active_sid not in st.session_state.sessions or st.session_state.sessions[active_sid]["vehicle_id"] != vid:
                st.info("Starte links eine neue Session, um den Wizard zu nutzen.")
            else:
                sid = active_sid
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
                st.caption(f"Pflichtfotos: {done_required}/{total_required} erledigt (Felgen optional).")

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
                    else:
                        f = files
                        session["photos"][step_key] = [{"name": f.name, "bytes": f.getvalue()}]
                    st.success("Gespeichert.")

                stored = session["photos"].get(step_key) or []
                if stored and stored[0].get("bytes"):
                    st.image(stored[0]["bytes"], caption=stored[0].get("name", ""), use_container_width=True)

                navL, navR = st.columns(2)
                with navL:
                    if st.button("⬅️ Zurück", use_container_width=True, disabled=session["closed"] or step_index == 0):
                        session["wizard_step"] = step_index - 1
                        st.rerun()
                with navR:
                    next_disabled = session["closed"] or (not optional and not step_has_photo(session, step_key))
                    if st.button("Weiter ➡️", use_container_width=True, disabled=next_disabled):
                        if step_index < len(WIZARD_STEPS) - 1:
                            session["wizard_step"] = step_index + 1
                            st.rerun()

        # Tab 2: Historie + Download (FIXED key!)
        with tabs[1]:
            st.markdown("### Historie")
            if not sessions_for_vehicle_sorted:
                st.info("Noch keine Sessions.")
            else:
                for s in sessions_for_vehicle_sorted:
                    with st.expander(session_label(s), expanded=False):
                        done_required, total_required = progress_required_photos(s)
                        st.caption(
                            f"Status: {'✅ abgeschlossen' if s['closed'] else '🟡 offen'} · "
                            f"Pflichtfotos {done_required}/{total_required} · Schäden: {len(s['damages'])}"
                        )

                        protocol_html = build_session_protocol_html(vehicle, s)
                        file_name = f"ReturnGuard_Protokoll_{vehicle.get('plate','Fahrzeug')}_{s.get('timestamp','')}.html".replace(" ", "_").replace(":", "-")

                        st.download_button(
                            "📄 Protokoll herunterladen (HTML → im Browser als PDF speichern)",
                            data=protocol_html.encode("utf-8"),
                            file_name=file_name,
                            mime="text/html",
                            use_container_width=True,
                            key=f"dl_protocol_{s['id']}"  # <- FIX: unique key prevents DuplicateElementId
                        )

        # Tab 3: Vorher/Nachher
        with tabs[2]:
            st.markdown("### Vorher/Nachher Vergleich")
            if len(sessions_for_vehicle_sorted) < 2:
                st.info("Für den Vergleich brauchst du mindestens zwei Sessions (z.B. Demo Vorher + Nachher).")
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

        # Tab 4: Export
        with tabs[3]:
            st.markdown("### Export (Demo)")
            st.write("Exportiert werden **nur Metadaten** (keine Bild-Bytes).")
            json_str = export_state_as_json()
            st.download_button(
                "JSON Export herunterladen",
                data=json_str.encode("utf-8"),
                file_name="returnguard_handover_showcase.json",
                mime="application/json",
                use_container_width=True,
                key="dl_json_export"
            )
            with st.expander("JSON Vorschau", expanded=False):
                st.code(json_str, language="json")

st.divider()
st.caption("Showcase v0.3c – Duplicate-ID Fix + Pitch Vorher/Nachher + Protokoll-Download (HTML).")
