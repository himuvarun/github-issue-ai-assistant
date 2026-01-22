from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from github_utils import parse_repo_url, fetch_issue
from llm_utils import analyze_issue_with_llm, analyze_pull_request_with_llm

app = FastAPI(title="AI-Powered GitHub Issue Assistant")

class AnalyzeRequest(BaseModel):
    repo_url: HttpUrl
    issue_number: int

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        owner, repo = parse_repo_url(str(request.repo_url))
        data = fetch_issue(owner, repo, request.issue_number)

        # 🧠 AGENTIC ROUTING
        if data["is_pull_request"]:
            return analyze_pull_request_with_llm(data)

        return analyze_issue_with_llm(data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
