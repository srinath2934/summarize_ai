<div align="center">

# ⚡ Summarize AI

**AI-powered text summarizer with structured output**

Built with **LangGraph** · **Groq (Llama 3.3 70B)** · **Pydantic** · **Flask**

---

</div>

## 🎥 Demo

<div align="center">

<video src="https://raw.githubusercontent.com/srinath2934/summarize_ai/main/assets/demo.mp4" controls autoplay muted loop width="100%">
</video>

</div>

---

## 🧠 What It Does

Paste any text → get a **structured JSON summary** with:
- 📌 **Title** — auto-generated descriptive title
- 📝 **Summary** — concise 2-3 sentence summary
- 🔑 **Key Points** — 3-5 bullet point takeaways

---

## 🏗️ Architecture

```
Frontend (HTML/JS)
    │
    │  POST /api/summarize  { "text": "..." }
    ▼
Flask Server (app.py)
    │
    │  calls run_summarizer()
    ▼
LangGraph + Pydantic (sumai.py)
    │
    │  structured_llm.invoke()
    ▼
Groq API (Llama 3.3 70B)
    │
    │  returns SummaryOutput
    ▼
Structured JSON Response ✅
```

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|---|---|---|
| **AI Model** | Groq + Llama 3.3 70B | Fast LLM inference |
| **Orchestration** | LangGraph | Stateful workflow graph |
| **Validation** | Pydantic BaseModel | Structured JSON output |
| **Backend** | Flask | REST API server |
| **Frontend** | HTML + CSS + JS | Simple dark-themed UI |
| **Memory** | MemorySaver | Persistent conversation context |

---

## 📂 Project Structure

```
SUMMARIZE AI/
├── backend/
│   ├── app.py           # Flask server (POST /api/summarize)
│   ├── sumai.py          # LangGraph + Pydantic + Groq engine
│   └── test.py           # Standalone test script
├── frontend/
│   └── index.html        # Dark-themed UI
├── env/
│   └── .env              # API key (git-ignored)
├── assets/
│   └── demo.mp4          # Demo video
├── requirements.txt      # Python dependencies
├── .gitignore            # Protects secrets & venv
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/SUMMARIZE-AI.git
cd SUMMARIZE-AI
python -m venv venv
venv\Scripts\activate       # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add API Key
Create `env/.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> Get a free key at [console.groq.com](https://console.groq.com)

### 4. Run
```bash
python backend/app.py
```
Open **http://localhost:5000** → paste text → hit Summarize ⚡

---

## 📡 API Reference

### `POST /api/summarize`

**Request:**
```json
{
  "text": "Your long text here...",
  "thread_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "thread_id": "abc-123",
  "data": {
    "title": "AI in Healthcare",
    "summary": "The article discusses how AI is transforming...",
    "key_points": [
      "AI improves disease detection",
      "Personalized treatment plans",
      "Data privacy remains a concern"
    ]
  }
}
```

### `GET /api/health`
```json
{ "status": "ok", "service": "Summarize AI" }
```

---

## 📜 License

MIT

---

<div align="center">

Built with ☕ and AI

</div>
