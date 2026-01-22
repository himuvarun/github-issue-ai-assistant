import os
import json
import re
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

# =================================================
# ENV SETUP
# =================================================
load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HUGGINGFACEHUB_API_TOKEN is not set")

# =================================================
# LLM CONFIG (Instruction-tuned, JSON-friendly)
# =================================================
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.1,
    max_new_tokens=512,
)

# =================================================
# FEW-SHOT PROMPT (STRONG, MINIMAL)
# =================================================
PROMPT = PromptTemplate(
    input_variables=["title", "body", "comments"],
    template="""
You are an AI assistant helping engineers triage GitHub issues.

STRICT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- Output must start with {{ and end with }}
- Avoid using "other" unless no category fits

JSON schema:
{{
  "summary": "",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1-5 with justification",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": ""
}}

### Example 1
Issue:
Title: App crashes on login
Description: App crashes when password is incorrect.

Output:
{{
  "summary": "The application crashes during login when invalid credentials are entered.",
  "type": "bug",
  "priority_score": "5 - core authentication flow is broken",
  "suggested_labels": ["bug", "login"],
  "potential_impact": "Users are unable to access the application."
}}

### Example 2
Issue:
Title: How do I configure authentication?
Description: I cannot find documentation for auth setup.

Output:
{{
  "summary": "The user is asking how to configure authentication.",
  "type": "question",
  "priority_score": "2 - informational request",
  "suggested_labels": ["question", "documentation"],
  "potential_impact": "No direct impact; affects developer understanding."
}}

### Now analyze this issue

Issue:
Title: {title}

Description:
{body}

Comments:
{comments}

Output:
"""
)

# =================================================
# JSON EXTRACTION (SAFE & ROBUST)
# =================================================
def extract_json(text: str):
    if not text:
        return None

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None

# =================================================
# MAIN ANALYSIS FUNCTION
# =================================================
def analyze_issue_with_llm(issue: dict):
    title = issue.get("title", "")
    body = issue.get("body", "")
    comments = "\n".join(issue.get("comments", []))

    prompt = PROMPT.format(
        title=title[:300],
        body=body[:1500],
        comments=comments[:1000],
    )

    try:
        raw = llm(prompt)
        parsed = extract_json(str(raw))

        if parsed:
            return parsed

        raise ValueError("Invalid JSON from LLM")

    except Exception:
        # =================================================
        # SMART DETERMINISTIC FALLBACK (LESS 'other')
        # =================================================
        text = (title + " " + body).lower()

        if any(k in text for k in ["crash", "error", "bug", "fail", "exception"]):
            issue_type = "bug"
        elif any(k in text for k in ["feature", "request", "enhancement", "add", "support"]):
            issue_type = "feature_request"
        elif any(k in text for k in ["doc", "documentation", "readme", "example", "typo"]):
            issue_type = "documentation"
        elif any(k in text for k in ["how", "why", "what", "can i", "?"]):
            issue_type = "question"
        else:
            issue_type = "other"

        return {
            "summary": title or "GitHub issue analysis",
            "type": issue_type,
            "priority_score": "3 - inferred priority",
            "suggested_labels": [issue_type, "triage"],
            "potential_impact": (
                "May negatively affect users if unresolved."
                if issue_type == "bug"
                else "Limited direct impact."
            ),
        }

# =================================================
# PR SUPPORT (SAFE EXTENSION)
# =================================================
def analyze_pull_request_with_llm(pr: dict):
    return {
        "summary": "This is a pull request, not a GitHub issue.",
        "type": "other",
        "priority_score": "2 - informational",
        "suggested_labels": ["pull-request"],
        "potential_impact": "No direct user impact; code under review.",
    }
