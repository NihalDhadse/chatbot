import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Nova AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>

    /* ---------- Background ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.35),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(6, 182, 212, 0.30),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(236, 72, 153, 0.25),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #080b18 0%,
                #11152a 50%,
                #090d1a 100%
            );

        color: white;
    }

    /* ---------- Main container ---------- */

    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* ---------- Animated blobs ---------- */

    .blob {
        position: fixed;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        filter: blur(100px);
        opacity: 0.18;
        z-index: 0;
        animation: float 8s ease-in-out infinite;
        pointer-events: none;
    }

    .blob-one {
        background: #7c3aed;
        top: 5%;
        left: 5%;
    }

    .blob-two {
        background: #06b6d4;
        bottom: 5%;
        right: 5%;
        animation-delay: 2s;
    }

    .blob-three {
        background: #ec4899;
        top: 45%;
        right: 35%;
        animation-delay: 4s;
    }

    @keyframes float {
        0%, 100% {
            transform: translate(0px, 0px) scale(1);
        }

        50% {
            transform: translate(30px, -40px) scale(1.15);
        }
    }

    /* ---------- Header ---------- */

    .hero {
        text-align: center;
        padding: 25px 20px 20px;
        position: relative;
        z-index: 1;
    }

    .logo {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 70px;
        height: 70px;
        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #06b6d4
            );

        box-shadow:
            0 0 35px rgba(124, 58, 237, 0.5);

        font-size: 34px;
        animation: pulse 3s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.4);
        }

        50% {
            transform: scale(1.05);
            box-shadow: 0 0 50px rgba(6, 182, 212, 0.55);
        }
    }

    .title {
        font-size: 48px;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 5px;

        background:
            linear-gradient(
                90deg,
                #c084fc,
                #22d3ee,
                #f472b6
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: #a5b4fc;
        font-size: 16px;
    }

    /* ---------- Glass card ---------- */

    .glass {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        border-radius: 24px;
        padding: 20px;

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.35);
    }

    /* ---------- Chat messages ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.035);
        margin-bottom: 12px;
        padding: 8px;
        animation: messageIn 0.35s ease;
    }

    @keyframes messageIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ---------- Chat input ---------- */

    [data-testid="stChatInput"] {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 20px;
    }

    [data-testid="stChatInput"] textarea {
        color: white !important;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(15, 23, 42, 0.98),
                rgba(8, 11, 24, 0.98)
            );

        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .sidebar-title {
        font-size: 24px;
        font-weight: 700;

        background:
            linear-gradient(
                90deg,
                #c084fc,
                #22d3ee
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .status {
        padding: 12px 15px;
        border-radius: 14px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.2);
        color: #86efac;
        margin-top: 15px;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05);
        color: white;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: #8b5cf6;
        background: rgba(124, 58, 237, 0.2);
    }

    </style>

    <div class="blob blob-one"></div>
    <div class="blob blob-two"></div>
    <div class="blob blob-three"></div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Model
# -----------------------------

model = ChatGroq(
    model="openai/gpt-oss-120b",
    max_tokens=500,
)

# -----------------------------
# Session state
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">✨ Nova AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="status">
            🟢 AI is online
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 🤖 Model")

    st.info("Groq • GPT-OSS 120B")

    st.markdown("### ⚙️ Controls")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption("Built with Streamlit + LangChain + Groq")


# -----------------------------
# Header
# -----------------------------



for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# User input
# -----------------------------

user_input = st.chat_input(
    "Message Nova AI..."
)

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("✨ Thinking..."):

            try:

                response = model.invoke(
                    user_input
                )

                answer = response.content

            except Exception as e:

                answer = (
                    "⚠️ Something went wrong.\n\n"
                    f"`{str(e)}`"
                )

            st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )