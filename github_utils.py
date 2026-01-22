import requests

GITHUB_API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "AI-GitHub-Issue-Assistant"
}


def parse_repo_url(repo_url: str):
    """
    Parse a GitHub repository URL and return (owner, repo).

    Expected format:
    https://github.com/{owner}/{repo}
    """
    parts = repo_url.rstrip("/").split("/")

    # Example:
    # https://github.com/facebook/react
    # ['https:', '', 'github.com', 'facebook', 'react']
    if len(parts) < 5 or parts[-3] != "github.com":
        raise ValueError(
            "Invalid GitHub repository URL. "
            "Use format: https://github.com/owner/repo"
        )

    return parts[-2], parts[-1]


def fetch_issue(owner: str, repo: str, issue_number: int):
    issue_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = f"{issue_url}/comments"

    issue_res = requests.get(issue_url, headers=HEADERS)

    if issue_res.status_code == 404:
        raise ValueError("Issue or Pull Request not found.")
    if issue_res.status_code == 403:
        raise ValueError("GitHub API rate limit exceeded.")
    if issue_res.status_code != 200:
        raise ValueError(f"GitHub API error: {issue_res.status_code}")

    issue = issue_res.json()

    is_pr = "pull_request" in issue

    comments_res = requests.get(comments_url, headers=HEADERS)
    comments = (
        [c.get("body", "") for c in comments_res.json()]
        if comments_res.status_code == 200
        else []
    )

    return {
        "title": issue.get("title", ""),
        "body": issue.get("body", ""),
        "comments": comments,
        "is_pull_request": is_pr
    }
