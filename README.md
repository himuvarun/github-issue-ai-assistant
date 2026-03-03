# 🤖 AI-Powered GitHub Issue Assistant

An AI-powered web application that analyzes GitHub issues and produces a **structured, actionable summary** to help engineering teams quickly understand, prioritize, and triage incoming issues.

This project was built as part of the **Seedling Labs Engineering Intern Craft**, showcasing **agentic thinking**, **robust prompt engineering**, and **clean system design**.

---

## 🎯 Problem Statement

At Seedling Labs, development moves fast. Efficiently understanding and prioritizing new GitHub issues is critical to maintaining both **quality and velocity**.

This application:
- Accepts a **public GitHub repository URL** and an **issue number**
- Fetches issue details via the GitHub API
- Uses an **LLM-powered AI agent** to analyze the issue
- Returns a **strictly structured JSON summary**
- Displays results in a clean, developer-friendly UI

---

## 🚀 Features

- 🧾 Input: GitHub Repository URL + Issue Number
- 🔗 GitHub API integration (title, body, comments)
- 🧠 AI-powered issue analysis using an LLM
- 📦 Strict JSON output (schema enforced)
- 🖥️ Streamlit-based frontend
- ⚠️ Graceful error handling for:
  - Invalid repositories
  - Non-existent issues
  - Pull Requests (PRs)
  - Empty comments
  - Very long issue bodies
  - LLM failures (deterministic fallback)

---

## 🧠 AI-Generated Output Format

```json
{
  "summary": "A one-sentence summary of the user's problem or request.",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1 to 5 with a brief justification",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "A brief sentence on the potential impact on users if unresolved"
}

## 🧱 System Architecture
Streamlit UI
     ↓
FastAPI Backend
     ↓
GitHub REST API  +  LLM (Hugging Face)
     ↓
Structured JSON Output

🧰 Tech Stack

Backend: FastAPI (Python)
Frontend: Streamlit
LLM: Hugging Face hosted model
LLM Orchestration: LangChain
APIs: GitHub REST API

🧠 Prompt Engineering Strategy
Few-Shot Prompting

To ensure reliable and schema-correct JSON output, the AI core uses few-shot prompting with representative examples (e.g., bug reports, feature requests).

This stabilizes:
Output structure
Issue type classification
Priority justification
Robustness
Strict instructions: “Return ONLY valid JSON”
Safe JSON extraction logic
Deterministic rule-based fallback if the LLM fails
This guarantees valid output for every request.

⚙️ Setup Instructions (Under 5 Minutes)

1️⃣ Clone the Repository
git clone https://github.com/<your-username>/github-issue-ai-assistant.git
cd github-issue-ai-assistant

2️⃣ Create Virtual Environment
python -m venv venv
Activate:
Windows
venv\Scripts\activate

macOS / Linux
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

🔑 Environment Variables
Create a .env file in the project root:
HUGGINGFACEHUB_API_TOKEN=your_hugging_face_token_here

You can generate a token from: https://huggingface.co/settings/tokens

▶️ Running the Application

Start Backend (FastAPI)
uvicorn api:app --reload

Start Frontend (Streamlit)
streamlit run app.py

🧪 Edge Case Handling

This project explicitly handles:
Issues with no comments
Extremely long issue bodies (safe truncation)
Pull Requests passed instead of issues
GitHub API failures
Invalid user input
LLM malformed output (fallback logic)

📁 Project Structure
.
├── api.py              # FastAPI backend
├── app.py              # Streamlit frontend
├── github_utils.py     # GitHub API helpers
├── llm_utils.py        # LLM logic & prompt engineering
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── .env.example        # Environment variable template

🌱 Future Improvements

Cache repeated issue analyses
Support Pull Request analysis
Add label auto-application via GitHub API
Batch issue analysis

📌 Conclusion

This project demonstrates:
Practical agentic AI system design
Strong prompt engineering with few-shot learning
Clean backend/frontend separation
Real-world robustness and edge-case handling
It represents a realistic microcosm of production AI work at Seedling Labs.
