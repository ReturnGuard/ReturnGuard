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
        # vehicles: {vehicle_id: {...}}
        st.session_state.vehicles = {}
    if "sessions" not in st.session_state:
        # sessions: {session_id: {...}}
        st.session_state.sessions = {}
    if "selected_vehicle_id" not in st.session_state:
        st.session_state.selected_vehicle_id = None


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def vehicle_label(v: dict) -> str:
    plate = v.get("plate") or "—"
    brand = v.get("brand") or "—"
    model = v.get("model") or "—"
    vin = v.get("vin") or ""
    return f"{plate} · {brand} {model}" + (f" · VIN {vin}" if vin else "")


def get_vehicle_sessions(vehicle_id: str):
    return [
        s for s in st.session_state.sessions.values()
        if s["vehicle_id"] == vehicle_id
    ]


def session_label(s: dict) -> str:
    t = "Übergabe" if s["type"] == "handover" else "Rückgabe"
    return f"{t} · {s['timestamp']} · {s.get('counterparty','').strip() or 'ohne Name'}"


def progress_required_photos(session: dict) -> tuple[int, int]:
    # Wheels optional -> exclude from required progress
    required_keys = [k for k, _ in REQUIRED_SHOTS if k != "wheels"]
    uploaded = 0
    for k in required_keys:
        if session["photos"].get(k):
            uploaded += 1
    return uploaded, len(required_keys)


def export_state_as_json() -> str:
    data = {
        "vehicles": st.session_state.vehicles,
        "sessions": st.session_state.sessions,
        "exported_at": now_iso(),
        "version": "showcase_v0.1",
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


# -----------------------------
# UI
# -----------------------------
ensure_state()

st.title("🛡️ ReturnGuard – Fahrzeug Übergabe-Check (Streamlit Showcase)")
st.caption("Prototyp: geführte Fotos, Schadensdoku, Historie, Vorher/Nachher-Vergleich. (Ohne KI / ohne Backend)")

colA, colB = st.columns([1, 2], gap="large")

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
        s_type = st.radio("Session-Typ", options=["handover", "return"], format_func=lambda x: "Übergabe" if x == "handover" else "Rückgabe", horizontal=True)
        counterparty = st.text_input("Übergabe an / Rückgabe von (optional)", placeholder="Name (Mitarbeiter/Kunde)")
        if st.button("Neue Session starten", use_container_width=True):
            sid = new_id("sess")
            st.session_state.sessions[sid] = {
                "id": sid,
                "vehicle_id": selected,
                "type": s_type,
                "timestamp": now_iso(),
                "counterparty": counterparty.strip(),
                "photos": {k: [] for k, _ in REQUIRED_SHOTS},  # each key -> list of uploaded files (bytes)
                "damages": [],  # list of damage dicts
                "closed": False,
            }
            st.session_state.active_session_id = sid
            st.success("Session gestartet. Rechts kannst du jetzt den Check durchführen.")


with colB:
    vid = st.session_state.selected_vehicle_id

    if not vid:
        st.warning("Wähle links ein Fahrzeug aus, um rechts den Ablauf zu sehen.")
    else:
        sessions_for_vehicle = get_vehicle_sessions(vid)
        sessions_for_vehicle_sorted = sorted(sessions_for_vehicle, key=lambda s: s["timestamp"], reverse=True)

        # Active session handling
        active_sid = st.session_state.get("active_session_id")
        if active_sid and active_sid in st.session_state.sessions:
            active = st.session_state.sessions[active_sid]
            if active["vehicle_id"] != vid:
                # If vehicle changed, don't auto-switch active session
                active_sid = None

        st.subheader("📸 Ablauf")
        tabs = st.tabs(["1) Guided Check", "2) Historie", "3) Vorher/Nachher", "4) Export (Demo)"])

        # -----------------------------
        # Tab 1: Guided Check
        # -----------------------------
        with tabs[0]:
            if not st.session_state.get("active_session_id") or st.session_state.sessions.get(st.session_state.get("active_session_id"), {}).get("vehicle_id") != vid:
                st.info("Starte links eine neue Session, um den geführten Check zu nutzen.")
            else:
                sid = st.session_state.active_session_id
                session = st.session_state.sessions[sid]

                t_label = "Übergabe" if session["type"] == "handover" else "Rückgabe"
                st.markdown(f"### {t_label} · {session['timestamp']}")
                if session.get("counterparty"):
                    st.caption(f"Person: {session['counterparty']}")

                uploaded, total = progress_required_photos(session)
                st.progress(uploaded / total if total else 0.0)
                st.caption(f"Pflichtfotos: {uploaded}/{total} erledigt (Felgen optional)")

                # Guided required photos
                st.markdown("#### Pflichtfotos (geführt)")
                for key, label in REQUIRED_SHOTS:
                    with st.expander(f"{label}", expanded=False):
                        hint = {
                            "front": "Tipp: 3–4m Abstand, Auto komplett im Bild.",
                            "rear": "Tipp: Kennzeichen sichtbar, kompletter Heckbereich.",
                            "left": "Tipp: komplette Seite, Räder mit drauf.",
                            "right": "Tipp: komplette Seite, Räder mit drauf.",
                            "interior_front": "Tipp: Armaturen + Sitze vorne sichtbar.",
                            "odometer": "Tipp: Zündung an, km-Stand gut lesbar.",
                            "wheels": "Optional: 1–2 Bilder pro Seite reichen.",
                        }.get(key, "")

                        st.write(hint)

                        files = st.file_uploader(
                            f"Foto(s) hochladen – {label}",
                            type=["jpg", "jpeg", "png", "heic"],
                            accept_multiple_files=True,
                            key=f"u_{sid}_{key}",
                            disabled=session["closed"],
                        )

                        if files:
                            # store bytes
                            session["photos"][key] = [{"name": f.name, "bytes": f.getvalue()} for f in files]
                            st.success(f"{len(files)} Datei(en) gespeichert.")

                        # preview
                        stored = session["photos"].get(key) or []
                        if stored:
                            st.caption(f"Gespeichert: {len(stored)}")
                            cols = st.columns(min(4, len(stored)))
                            for i, item in enumerate(stored[:4]):
                                with cols[i % len(cols)]:
                                    st.image(item["bytes"], caption=item["name"], use_container_width=True)

                st.divider()
                st.markdown("#### Schäden hinzufügen (manuell)")

                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        cat = st.selectbox("Kategorie", DAMAGE_CATEGORIES, key=f"cat_{sid}", disabled=session["closed"])
                    with c2:
                        pos = st.selectbox("Position", POSITIONS, key=f"pos_{sid}", disabled=session["closed"])
                    with c3:
                        note = st.text_input("Notiz (optional)", key=f"note_{sid}", placeholder="z.B. Kratzer ca. 5cm, Stoßfänger unten", disabled=session["closed"])

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

                # list damages
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
                    if st.button("Session abschließen", type="primary", use_container_width=True, disabled=session["closed"]):
                        # Require mandatory photos except wheels
                        missing = []
                        for k, label in REQUIRED_SHOTS:
                            if k == "wheels":
                                continue
                            if not session["photos"].get(k):
                                missing.append(label)
                        if missing:
                            st.error("Noch fehlen Pflichtfotos: " + ", ".join(missing))
                        else:
                            session["closed"] = True
                            st.success("Session abgeschlossen (gespeichert in Historie).")
                with cR:
                    if st.button("Session verwerfen (Demo)", use_container_width=True):
                        del st.session_state.sessions[sid]
                        st.session_state.active_session_id = None
                        st.warning("Session verworfen.")

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
                        uploaded, total = progress_required_photos(s)
                        st.caption(f"Status: {'✅ abgeschlossen' if s['closed'] else '🟡 offen'} · Pflichtfotos {uploaded}/{total} · Schäden: {len(s['damages'])}")
                        # quick preview of the 4 main shots
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
                shot_pairs = [("front", "Front"), ("rear", "Heck"), ("left", "Links"), ("right", "Rechts"), ("interior_front", "Innenraum"), ("odometer", "Tacho")]

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
            st.write("Für Investor-/Stakeholder-Demos ist Export praktisch (z.B. als Protokoll-Quelle).")
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


# Footer
st.divider()
st.caption("Showcase v0.1 – Nächster Schritt: PDF-Protokoll + (optional) OCR-Scan-Simulation + Rollen/Cloud.")
