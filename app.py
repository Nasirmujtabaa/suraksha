import hashlib

import streamlit as st

import rag

st.set_page_config(page_title="Suraksha Safety Assistant", page_icon="🦺", layout="wide")

# ---------- UI text (English / Hindi / Kannada) ----------
T = {
    "en": {
        "title": "🦺 Suraksha Safety Assistant",
        "sub": "Ask a safety question. Answers come only from official manuals.",
        "emergency": "🚨 EMERGENCY: call **112** · Fire **101** · Ambulance **108**",
        "quick": "Quick hazards",
        "type": "Or type your question",
        "ask": "Ask",
        "voice": "🎤 Or ask by voice",
        "sources": "Sources (verify in the manual)",
        "page": "page",
        "not_found": "Not found in manuals. Contact your safety officer.",
        "disclaimer": "This assistant supports, but does not replace, your factory's official safety procedures. In an emergency, act first and call for help.",
        "lang": "Language",
        "thinking": "Searching manuals...",
        "heard": "Heard",
        "hazards": {
            "fire": "Fire", "chem": "Chemical spill", "guard": "Machine guarding",
            "elec": "Electric shock", "height": "Fall from height", "aid": "First aid",
            "confined": "Confined space", "ppe": "PPE",
        },
    },
    "hi": {
        "title": "🦺 सुरक्षा सहायक",
        "sub": "सुरक्षा से जुड़ा सवाल पूछें। उत्तर केवल आधिकारिक मैनुअल से दिए जाते हैं।",
        "emergency": "🚨 आपातकाल: **112** · अग्निशमन **101** · एम्बुलेंस **108**",
        "quick": "त्वरित खतरे",
        "type": "या अपना सवाल लिखें",
        "ask": "पूछें",
        "voice": "🎤 या आवाज़ से पूछें",
        "sources": "स्रोत (मैनुअल में जाँचें)",
        "page": "पृष्ठ",
        "not_found": "मैनुअल में नहीं मिला। अपने सुरक्षा अधिकारी से संपर्क करें।",
        "disclaimer": "यह सहायक आपकी फैक्ट्री की आधिकारिक सुरक्षा प्रक्रियाओं का विकल्प नहीं है, केवल सहायता करता है। आपात स्थिति में पहले कार्रवाई करें और मदद बुलाएँ।",
        "lang": "भाषा",
        "thinking": "मैनुअल में खोज रहे हैं...",
        "heard": "सुना गया",
        "hazards": {
            "fire": "आग", "chem": "रासायनिक रिसाव", "guard": "मशीन गार्ड",
            "elec": "बिजली का झटका", "height": "ऊँचाई से गिरना", "aid": "प्राथमिक उपचार",
            "confined": "सीमित स्थान", "ppe": "सुरक्षा उपकरण (PPE)",
        },
    },
    "kn": {
        "title": "🦺 ಸುರಕ್ಷಾ ಸಹಾಯಕ",
        "sub": "ಸುರಕ್ಷತೆಯ ಪ್ರಶ್ನೆ ಕೇಳಿ. ಉತ್ತರಗಳು ಅಧಿಕೃತ ಕೈಪಿಡಿಗಳಿಂದ ಮಾತ್ರ ಬರುತ್ತವೆ.",
        "emergency": "🚨 ತುರ್ತು: **112** · ಅಗ್ನಿಶಾಮಕ **101** · ಆಂಬ್ಯುಲೆನ್ಸ್ **108**",
        "quick": "ತ್ವರಿತ ಅಪಾಯಗಳು",
        "type": "ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಬರೆಯಿರಿ",
        "ask": "ಕೇಳಿ",
        "voice": "🎤 ಅಥವಾ ಧ್ವನಿಯಿಂದ ಕೇಳಿ",
        "sources": "ಮೂಲಗಳು (ಕೈಪಿಡಿಯಲ್ಲಿ ಪರಿಶೀಲಿಸಿ)",
        "page": "ಪುಟ",
        "not_found": "ಕೈಪಿಡಿಗಳಲ್ಲಿ ಸಿಗಲಿಲ್ಲ. ನಿಮ್ಮ ಸುರಕ್ಷತಾ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "disclaimer": "ಈ ಸಹಾಯಕವು ನಿಮ್ಮ ಕಾರ್ಖಾನೆಯ ಅಧಿಕೃತ ಸುರಕ್ಷತಾ ವಿಧಾನಗಳಿಗೆ ಬದಲಿ ಅಲ್ಲ, ಕೇವಲ ಸಹಾಯ ಮಾಡುತ್ತದೆ. ತುರ್ತು ಸ್ಥಿತಿಯಲ್ಲಿ ಮೊದಲು ಕ್ರಮ ಕೈಗೊಳ್ಳಿ ಮತ್ತು ಸಹಾಯ ಕರೆಯಿರಿ.",
        "lang": "ಭಾಷೆ",
        "thinking": "ಕೈಪಿಡಿಗಳಲ್ಲಿ ಹುಡುಕುತ್ತಿದೆ...",
        "heard": "ಕೇಳಿಸಿದ್ದು",
        "hazards": {
            "fire": "ಬೆಂಕಿ", "chem": "ರಾಸಾಯನಿಕ ಸೋರಿಕೆ", "guard": "ಯಂತ್ರ ರಕ್ಷಕ",
            "elec": "ವಿದ್ಯುತ್ ಆಘಾತ", "height": "ಎತ್ತರದಿಂದ ಬೀಳುವುದು", "aid": "ಪ್ರಥಮ ಚಿಕಿತ್ಸೆ",
            "confined": "ಮುಚ್ಚಿದ ಜಾಗ", "ppe": "ಸುರಕ್ಷಾ ಸಲಕರಣೆ (PPE)",
        },
    },
}

# Retrieval queries are in English (the manuals are English); the ANSWER is in the chosen language.
HAZARDS = [
    ("🔥", "fire", "Fire safety precautions, fire alarm and means of escape in case of fire"),
    ("☣️", "chem", "Chemical spill or leak emergency procedure and handling of hazardous chemicals"),
    ("⚙️", "guard", "Requirements for fencing and guarding of machinery"),
    ("⚡", "elec", "Electrical safety and what to do in case of electric shock"),
    ("🪜", "height", "Safety requirements for working at height and prevention of falls"),
    ("🩹", "aid", "First aid arrangements and first aid for injuries and burns"),
    ("🕳️", "confined", "Safety precautions for entering confined spaces, tanks and pits"),
    ("🦺", "ppe", "Personal protective equipment requirements for workers"),
]

# ---------- Big touch-friendly buttons for tablets ----------
st.markdown(
    """
    <style>
    div.stButton > button {min-height: 4.2rem; font-size: 1.25rem; font-weight: 600; border-radius: 14px;}
    </style>
    """,
    unsafe_allow_html=True,
)

lang_label = {"English": "en", "हिन्दी": "hi", "ಕನ್ನಡ": "kn"}
choice = st.sidebar.radio("Language / भाषा / ಭಾಷೆ", list(lang_label.keys()))
lang = lang_label[choice]
t = T[lang]


# ---------- Cached resources ----------
@st.cache_resource(show_spinner="Loading safety manuals...")
def get_store():
    return rag.load_index()


@st.cache_resource
def get_llm():
    return rag.get_llm()


@st.cache_data(show_spinner=False)
def cached_answer(question: str, language: str):
    # Same question + language -> same answer, and saves API calls.
    return rag.answer_question(question, language, get_store(), get_llm())


def transcribe(audio_bytes: bytes, language: str) -> str:
    from groq import Groq

    client = Groq(api_key=rag.get_secret("GROQ_API_KEY"))
    res = client.audio.transcriptions.create(
        file=("question.wav", audio_bytes),
        model=rag.get_secret("GROQ_STT_MODEL", "whisper-large-v3"),
        language=language,
        temperature=0,
    )
    return getattr(res, "text", str(res)).strip()


# ---------- Page ----------
st.title(t["title"])
st.caption(t["sub"])
st.error(t["emergency"])

# First start on a fresh server: build the index from the PDFs in data/
if not (rag.INDEX_DIR / "index.faiss").exists():
    with st.spinner("First start: reading the manuals (takes 2-4 minutes, please wait)..."):
        try:
            import build_index

            build_index.main()
        except SystemExit as e:
            st.error(f"Could not build index: {e}")
            st.stop()

try:
    get_store()
    get_llm()
except Exception as e:  # missing index / missing key
    st.error(f"Setup problem: {e}")
    st.stop()

if "q" not in st.session_state:
    st.session_state.q = ""
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

new_q = None

st.subheader(t["quick"])
for row in range(0, len(HAZARDS), 4):
    cols = st.columns(4)
    for col, (icon, key, query) in zip(cols, HAZARDS[row:row + 4]):
        if col.button(f"{icon} {t['hazards'][key]}", use_container_width=True, key=f"hz_{key}"):
            new_q = query

typed = st.text_input(t["type"], key="typed")
if st.button(f"🔎 {t['ask']}", use_container_width=True, key="ask_btn") and typed.strip():
    new_q = typed.strip()

audio = st.audio_input(t["voice"])
if audio is not None:
    data = audio.getvalue()
    digest = hashlib.md5(data).hexdigest()
    if digest != st.session_state.last_audio:     # transcribe each recording only once
        st.session_state.last_audio = digest
        try:
            heard = transcribe(data, lang)
            if heard:
                new_q = heard
        except Exception as e:
            st.warning(f"Voice not understood, please type your question. ({e})")

if new_q:
    st.session_state.q = new_q

q = st.session_state.q
if q:
    st.divider()
    st.markdown(f"### ❓ {q}")
    with st.spinner(t["thinking"]):
        try:
            result = cached_answer(q, lang)
        except Exception as e:
            st.error(f"Could not get an answer right now: {e}")
            st.stop()

    if result["found"]:
        st.success(result["answer"])
        with st.expander(t["sources"], expanded=True):
            for s in result["sources"]:
                st.markdown(f"**[{s['n']}] 📄 {s['name']}, {t['page']} {s['page']}**")
                st.caption(s["text"])
    else:
        st.warning(t["not_found"])
        with st.expander("Closest passages found (NOT a confirmed answer)"):
            for s in result["sources"]:
                st.markdown(f"**[{s['n']}] 📄 {s['name']}, {t['page']} {s['page']}**")
                st.caption(s["text"])

st.divider()
st.caption(f"⚠️ {t['disclaimer']}")