# 🧑‍💻 AI Code Explainer

A simple Generative AI app that explains programming code in beginner-friendly language —
built with **Python**, **Streamlit**, and the **Claude (Anthropic) API**.

Paste in a code snippet and get:
- ✅ A plain-English summary of what it does
- ✅ A step-by-step breakdown of how it works
- ✅ Time complexity and space complexity (Big-O), with justification
- ✅ Key functions/variables and their roles
- ✅ Potential issues or bugs

**Bonus features:**
- 🌐 Multi-language support: Python, C++, Java, JavaScript, TypeScript, C, C#, Go, Rust
- ✨ "Improve This Code" — get a cleaner, more idiomatic rewrite
- ⚡ "Optimize This Code" — get a more performant version with before/after complexity

## Demo

![screenshot placeholder](docs/screenshot.png)

## Tech Stack

- **Frontend / App:** [Streamlit](https://streamlit.io/)
- **LLM:** [Anthropic Claude API](https://www.anthropic.com/api)
- **Language:** Python 3.9+

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ai-code-explainer.git
cd ai-code-explainer
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API key

Get a free API key from the [Anthropic Console](https://console.anthropic.com/).

Either export it as an environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"   # On Windows: set ANTHROPIC_API_KEY=...
```

or copy `.env.example` to `.env` and fill it in, or just paste it into the app's sidebar
at runtime — nothing is stored on disk.

### 4. Run the app

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## How It Works

1. The user pastes a code snippet and picks a language (or leaves it on auto-detect).
2. The app sends the code to Claude with a system prompt that asks for a structured
   JSON response covering the summary, step-by-step explanation, complexity analysis,
   key elements, and potential issues.
3. The JSON is parsed and rendered in a clean, structured layout using Streamlit.
4. The "Improve" and "Optimize" buttons use two more focused prompts that return a
   rewritten version of the code plus an explanation of the changes.

## Project Structure

```
ai-code-explainer/
├── app.py              # Streamlit app (UI + Claude API calls)
├── requirements.txt     # Python dependencies
├── .env.example          # Template for environment variables
├── .gitignore
└── README.md
```

## Possible Future Improvements

- Syntax-aware auto-detection of the input language
- Support for uploading whole files instead of pasting snippets
- Side-by-side diff view for "Improve"/"Optimize" results
- Caching identical requests to save API calls

## License

MIT — feel free to use this for your own learning or club projects.
