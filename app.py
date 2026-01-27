import streamlit as st
from datetime import datetime
import uuid
import json

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
        "version": "showcase_v0.2_wizard",
        "export_mode": "metadata_only",
    }
    safe = _strip_image_bytes(raw)
    return json.dumps(safe, indent=2, ensure_ascii=False)


# ---------- Wizard helpers ----------

WIZARD_HINTS = {
    "front": "Tipp: 3–4m Abstand, Auto komplett im Bild.",
    "rear": "Tipp: Kennzeichen sichtbar, kompletter Heckbereich.",
    "left": "Tipp: komplette Seite, Räder mit drauf.",
    "right": "Tipp: komplette Seite, Räder mit drauf.",
    "interior_front": "Tipp: Armaturen + Sitze vorne sichtbar.",
    "odometer": "Tipp: Zündung an, km-Stand gut lesbar.",
    "wheels": "Optional: 1–2 Bilder pro Seite reichen.",
}


def wizard_steps():
    # Pflichtschritte ohne wheels + optionaler wheels-Schritt am Ende
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
    # If all required present, jump to optional wheels step
    for i, (k, _) in enumerate(steps):
        if is_step_optional(k):
            return i
    return 0


# -----------------------------
# UI
# -----------------------------
ensure_state()

st.title("🛡️ ReturnGuard – Fahrzeug Übergabe-Check (Showcase)")
st.caption("Prototyp: Wizard-Fotos (1/6), Schadensdoku, Historie, Vorher/Nachher-Vergleich. (Ohne KI / ohne Backend)")

colA, colB = st.columns([1, 2], gap="large")

# ---------- Left column ----------
with colA:
    st.subheader("🚗 Fahrzeuge")

    with st.expander("➕ Neues Fahrzeug anlegen", expanded=True):
        plate = st.text_input("Kennzeichen*", placeholder="M-AB 1234")
        brand = st.text_input("Marke*", placeholder="Audi")
        model = st.text_input("Modell*", placeholder="A3 Sportback")
        vin = st.text_input("FIN/VIN (optional)", placeholder="WAUZZZ...")
        note = st.text_area("Notiz (optional)", placeholder="z.B. Poolfahrzeug, Winterräder an Bord…", height=80)

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
        st.info("Noch keine Fahrzeuge. Lege links eins an, dann kannst du eine Übergabe starten.")
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
            horizontal=True
        )
        counterparty = st.text_input("Übergabe an / Rückgabe von (optional)", placeholder="Name (Mitarbeiter/Kunde)")

        if st.button("Neue Session starten", use_container_width=True):
            sid = new_id("sess")
            st.session_state.sessions[sid] = {
                "id": sid,
                "vehicle_id": selected,
                "type": s_type,
                "timestamp": now_iso(),
                "counterparty": counterparty.strip(),
                "photos": {k: [] for k, _ in REQUIRED_SHOTS},  # list of dicts {name, bytes}
                "damages": [],
                "closed": False,
                "wizard_step": 0,  # NEW: wizard state stored per session
            }
            st.session_state.active_session_id = sid
            st.success("Session gestartet. Rechts kannst du jetzt den Check durchführen.")


# ---------- Right column ----------
with colB:
    vid = st.session_state.selected_vehicle_id

    if not vid:
        st.warning("Wähle links ein Fahrzeug aus, um rechts den Ablauf zu sehen.")
    else:
        sessions_for_vehicle = get_vehicle_sessions(vid)
        sessions_for_vehicle_sorted = sorted(sessions_for_vehicle, key=lambda s: s["timestamp"], reverse=True)

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

                # Initialize wizard_step if older sessions exist
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

                # Smart jump button (useful after refresh)
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

                # Clamp wizard step
                if session["wizard_step"] < 0:
                    session["wizard_step"] = 0
                if session["wizard_step"] >= len(steps):
                    session["wizard_step"] = len(steps) - 1

                step_index = session["wizard_step"]
                step_key, step_label = steps[step_index]
                optional = is_step_optional(step_key)

                # Wizard header
                req_idx = step_index + 1
                # Show as 1/6 for required steps; wheels as "Optional"
                if not optional:
                    st.markdown(f"## Schritt {req_idx}/{total_required}: **{step_label}**")
                else:
                    st.markdown(f"## Optional: **{step_label}**")

                st.write(WIZARD_HINTS.get(step_key, ""))

                # Uploader behavior:
                # - Required steps: single photo is enough (accept_multiple_files=False)
                # - Wheels: allow multiple
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
                        # single file
                        f = files[0] if isinstance(files, list) else files
                        # In Streamlit, with accept_multiple_files=False, "files" is UploadedFile not list.
                        # But to be safe we handle both.
                        if hasattr(f, "getvalue"):
                            session["photos"][step_key] = [{"name": f.name, "bytes": f.getvalue()}]
                            st.success("1 Datei gespeichert.")

                # Preview current step photo(s)
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

                # Wizard navigation
                navL, navM, navR = st.columns([1, 1, 1])
                with navL:
                    if st.button("⬅️ Zurück", use_container_width=True, disabled=session["closed"] or step_index == 0):
                        session["wizard_step"] = max(0, step_index - 1)
                        st.rerun()

                with navM:
                    # Skip only allowed for optional wheels
                    if st.button("⏭️ Überspringen", use_container_width=True, disabled=session["closed"] or not optional):
                        # Move to end (summary area conceptually)
                        session["wizard_step"] = step_index  # stay; optional skip simply means "not required"
                        st.info("Optional übersprungen. Du kannst die Session trotzdem abschließen, wenn Pflichtfotos vollständig sind.")
                        # no rerun needed

                with navR:
                    # Next requires photo if required step
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

                # Damage section (same as before)
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

                # Session close / discard
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
                            # jump to first missing step
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
        # Tab 2: History
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

                        preview_keys = ["front", "rear", "left", "right"]
                        pcols = st.columns(4)
                        for i, k in enumerate(preview_keys):
                            imgs = s["photos"].get(k) or []
                            if imgs:
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
st.caption("Showcase v0.2 (Wizard) – Nächster Schritt: PDF-Protokoll + (optional) Scan-Simulation + Rollen/Cloud.")
