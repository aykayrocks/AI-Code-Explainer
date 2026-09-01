import os
import json

from dotenv import load_dotenv
from google import genai
import streamlit as st

load_dotenv()

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

MODEL_NAME = "gemini-3.6-flash"

LANGUAGES = [
    "Auto-detect",
    "Python",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "C",
    "C#",
    "Go",
    "Rust",
]

# --------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------

EXPLAIN_SYSTEM_PROMPT = """You are a friendly, patient programming tutor who explains code
to beginners. You will be given a code snippet (and possibly its language).

Respond ONLY with a single valid JSON object with exactly these keys:

{
  "language": "detected or given programming language",
  "summary": "1-3 sentence plain-English summary of what the code does overall",
  "how_it_works": "a clear, step-by-step walkthrough in beginner-friendly language, formatted as a markdown numbered list",
  "time_complexity": "Big-O time complexity with a short one-sentence justification",
  "space_complexity": "Big-O space complexity with a short one-sentence justification",
  "key_elements": [
    {"name": "function or variable name", "role": "what it does / why it matters"}
  ],
  "potential_issues": "any bugs, edge cases, or bad practices you notice, or 'None spotted' if the code looks fine"
}

Keep language simple and avoid jargon where possible. If the code is incomplete or invalid,
still do your best to explain what is there and note the issue in potential_issues."""

IMPROVE_SYSTEM_PROMPT = """You are an expert code reviewer. You will be given a code snippet.

Rewrite it to be cleaner, more readable, and more idiomatic, WITHOUT changing its behavior.

Respond ONLY with a single valid JSON object:

{
  "improved_code": "the improved code as a plain string",
  "changes_made": "a markdown bullet list explaining each change and why it helps"
}"""

OPTIMIZE_SYSTEM_PROMPT = """You are an expert in algorithmic optimization. You will be given a
code snippet.

Rewrite it to be more performant (better time and/or space complexity where possible),
WITHOUT changing its observable behavior.

Respond ONLY with a single valid JSON object:

{
  "optimized_code": "the optimized code as a plain string",
  "original_complexity": "Big-O time/space of the original code",
  "optimized_complexity": "Big-O time/space of the optimized code",
  "explanation": "a markdown bullet list explaining what changed and why it's faster/leaner"
}"""

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("No Gemini API key found. Check your .env file.")

    return genai.Client(api_key=api_key)


def call_gemini_json(system_prompt: str, user_content: str) -> dict:
    """Call Gemini and parse its response as JSON."""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"{system_prompt}\n\n{user_content}",
        config={
            "response_mime_type": "application/json",
        },
    )

    raw_text = response.text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")

        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:]

        raw_text = raw_text.strip()

    return json.loads(raw_text)


def build_user_message(code: str, language: str) -> str:

    if language != "Auto-detect":
        lang_hint = f"Language: {language}\n\n"
    else:
        lang_hint = ""

    return f"{lang_hint}Code:\n```\n{code}\n```"


# --------------------------------------------------------------------------
# Page Configuration
# --------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Code Detangler",
    page_icon="💻",
    layout="centered"
)


# --------------------------------------------------------------------------
# Custom Styling
# --------------------------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600;700&family=Space+Mono&display=swap');


/* ============================================================
   BACKGROUND
============================================================ */

.stApp {
    background-color: #e0c5c4 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #e0c5c4 !important;
}


/* ============================================================
   MAIN CONTAINER
============================================================ */

.block-container {
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 3rem !important;
    padding-bottom: 4rem !important;
}


/* ============================================================
   HIDE SIDEBAR
============================================================ */

[data-testid="stSidebar"] {
    display: none !important;
}


/* ============================================================
   TITLE
============================================================ */

.hero {
    width: 100%;
    text-align: center;
    margin: 0 auto 40px auto;
}

.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 70px !important;
    font-weight: 700 !important;
    color: #470020 !important;
    text-align: center !important;
    line-height: 1.1 !important;
    margin: 0 !important;
    padding: 0 !important;
}

.hero p {
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    color: #8a8282 !important;
    text-align: center !important;
    margin-top: 12px !important;
}


/* ============================================================
   GENERAL FONT
============================================================ */

.stApp {
    font-family: 'Poppins', sans-serif !important;
}

.stApp p {
    font-family: 'Poppins', sans-serif !important;
}

.stApp label {
    font-family: 'Poppins', sans-serif !important;
}


/* ============================================================
   SELECT BOX
============================================================ */

[data-testid="stSelectbox"] label {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: none !important;
    border-radius: 13px !important;
    min-height: 45px !important;
}


/* ============================================================
   CODE INPUT
============================================================ */

[data-testid="stTextArea"] label {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

[data-testid="stTextArea"] textarea {
    background-color: #171717 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 15px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 15px !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.18) !important;
}

/* Code box when clicked */
[data-testid="stTextArea"] textarea:focus {
    background-color: #171717 !important;
    color: #FFFFFF !important;
    border: 1px solid #FFFFFF !important;
    box-shadow: 0 0 0 1px #FFFFFF !important;
}

/* Placeholder */
[data-testid="stTextArea"] textarea::placeholder {
    color: #888888 !important;
    opacity: 1 !important;
}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {
    background-color: #FFF0F1 !important;
    color: #4A202B !important;
    border: none !important;
    border-radius: 20px !important;
    min-height: 48px !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 7px 18px rgba(0, 0, 0, 0.12) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 22px rgba(0, 0, 0, 0.18) !important;
}


/* ============================================================
   HEADINGS
============================================================ */

.stApp h2,
.stApp h3 {
    font-family: 'Poppins', sans-serif !important;
    color: #FFFFFF !important;
}


/* ============================================================
   NORMAL OUTPUT TEXT
============================================================ */

.stApp .stMarkdown {
    font-family: 'Poppins', sans-serif !important;
}


/* ============================================================
   CODE OUTPUT
============================================================ */

.stCode {
    border-radius: 14px !important;
}


/* ============================================================
   INFO / WARNING BOXES
============================================================ */

[data-testid="stAlert"] {
    border-radius: 13px !important;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    color: #000000;
    font-size: 13px;
    margin-top: 45px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>AI Code Detangler</h1>
    <p>Untangle your code. Understand how it works.</p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Language Selection
# --------------------------------------------------------------------------

language = st.selectbox(
    "Programming Language",
    LANGUAGES,
    index=0
)


# --------------------------------------------------------------------------
# Main Input
# --------------------------------------------------------------------------

code_input = st.text_area(
    "Paste your code",
    height=285,
    placeholder="""def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)"""
)


# --------------------------------------------------------------------------
# Buttons
# --------------------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    explain_clicked = st.button(
        "🔍 Explain Code",
        use_container_width=True,
        type="primary"
    )

with col2:
    improve_clicked = st.button(
        "✨ Improve Code",
        use_container_width=True
    )

with col3:
    optimize_clicked = st.button(
        "⚡ Optimize Code",
        use_container_width=True
    )


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

if (
    explain_clicked
    or improve_clicked
    or optimize_clicked
) and not code_input.strip():

    st.warning("Please paste some code first.")


has_key = bool(os.environ.get("GEMINI_API_KEY"))

if (
    explain_clicked
    or improve_clicked
    or optimize_clicked
) and not has_key:

    st.error(
        "Gemini API key not found. Make sure your .env file contains GEMINI_API_KEY."
    )


# --------------------------------------------------------------------------
# Explain Code
# --------------------------------------------------------------------------

if explain_clicked and code_input.strip() and has_key:

    with st.spinner("Analyzing your code..."):

        try:

            result = call_gemini_json(
                EXPLAIN_SYSTEM_PROMPT,
                build_user_message(code_input, language)
            )

            st.subheader(
                f"Explanation ({result.get('language', language)})"
            )

            st.markdown("### What does it do?")

            st.write(
                result.get("summary", "")
            )

            st.markdown("### How does it work?")

            st.markdown(
                result.get("how_it_works", "")
            )

            st.markdown("### Complexity")

            c1, c2 = st.columns(2)

            with c1:

                st.markdown("**Time Complexity**")

                st.info(
                    result.get(
                        "time_complexity",
                        "N/A"
                    )
                )

            with c2:

                st.markdown("**Space Complexity**")

                st.info(
                    result.get(
                        "space_complexity",
                        "N/A"
                    )
                )

            key_elements = result.get(
                "key_elements",
                []
            )

            if key_elements:

                st.markdown("### Key Functions & Variables")

                for item in key_elements:

                    st.markdown(
                        f"- **`{item.get('name', '')}`** — "
                        f"{item.get('role', '')}"
                    )

            st.markdown("### Potential Issues")

            st.info(
                result.get(
                    "potential_issues",
                    "None spotted"
                )
            )

        except json.JSONDecodeError:

            st.error(
                "Gemini returned a response that wasn't valid JSON. Please try again."
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )


# --------------------------------------------------------------------------
# Improve Code
# --------------------------------------------------------------------------

if improve_clicked and code_input.strip() and has_key:

    with st.spinner("Improving your code..."):

        try:

            result = call_gemini_json(
                IMPROVE_SYSTEM_PROMPT,
                build_user_message(code_input, language)
            )

            st.subheader("Improved Code")

            st.code(
                result.get(
                    "improved_code",
                    ""
                ),
                language=(
                    language.lower()
                    if language != "Auto-detect"
                    else None
                )
            )

            st.markdown("### What changed?")

            st.markdown(
                result.get(
                    "changes_made",
                    ""
                )
            )

        except json.JSONDecodeError:

            st.error(
                "Gemini returned a response that wasn't valid JSON. Please try again."
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )


# --------------------------------------------------------------------------
# Optimize Code
# --------------------------------------------------------------------------

if optimize_clicked and code_input.strip() and has_key:

    with st.spinner("Looking for a faster approach..."):

        try:

            result = call_gemini_json(
                OPTIMIZE_SYSTEM_PROMPT,
                build_user_message(code_input, language)
            )

            st.subheader("Optimized Code")

            st.code(
                result.get(
                    "optimized_code",
                    ""
                ),
                language=(
                    language.lower()
                    if language != "Auto-detect"
                    else None
                )
            )

            st.markdown("### Complexity Comparison")

            c1, c2 = st.columns(2)

            with c1:

                st.markdown("**Original**")

                st.info(
                    result.get(
                        "original_complexity",
                        "N/A"
                    )
                )

            with c2:

                st.markdown("**Optimized**")

                st.info(
                    result.get(
                        "optimized_complexity",
                        "N/A"
                    )
                )

            st.markdown("### What changed?")

            st.markdown(
                result.get(
                    "explanation",
                    ""
                )
            )

        except json.JSONDecodeError:

            st.error(
                "Gemini returned a response that wasn't valid JSON. Please try again."
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------

st.markdown("""
<div class="footer">
    Built with Python · Streamlit · Gemini
    <br>
    Made by Akshara
</div>
""", unsafe_allow_html=True)
