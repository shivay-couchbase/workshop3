import os
import logging
from typing import List, Dict, Optional

import httpx
from dotenv import load_dotenv
from langchain_core.tools import tool
from typing_extensions import TypedDict

# -------- ENV & LOGGING --------
load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("prtools")
logging.getLogger("httpx").setLevel(logging.WARNING)

# -------- COMMENT STRUCTURE --------
class ReviewComment(TypedDict):
    path: str
    line: int
    body: str

# -------- GITHUB API WRAPPER --------
class GitHubPRService:
    """
    Handles GitHub PR integration for file retrieval and batch posting of review comments.
    """

    def __init__(self, token: str, repo: str, pr_number: str):
        for arg, name in zip([token, repo, pr_number], ["TOKEN_GITHUB", "GITHUB_REPO", "PR_NUMBER"]):
            if not arg:
                raise ValueError(f"Required environment variable missing: {name}")
        self.token = token
        self.repo = repo
        self.pr_number = pr_number
        self.base_url = f"https://api.github.com/repos/{self.repo}/pulls/{self.pr_number}"

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def get_diff_files(self) -> List[Dict[str, str]]:
        """
        Returns PR files along with their diff patches.
        """
        url = f"{self.base_url}/files"
        try:
            resp = httpx.get(url, headers=self.headers, timeout=10.0)
            resp.raise_for_status()
            parsed = resp.json()
            return [
                {"filename": f["filename"], "patch": f.get("patch", "")}
                for f in parsed if f.get("patch")
            ]
        except Exception as e:
            log.error(f"Failed to fetch PR files: {e}")
            return []

    def submit_review_comments(self, comments: List[ReviewComment]) -> str:
        """
        Posts a batch of inline review comments on the pull request.
        """
        if not comments:
            return "No comments provided."
        review_endpoint = f"https://api.github.com/repos/{self.repo}/pulls/{self.pr_number}/reviews"
        payload = {
            "body": "Automated Review by AI.",
            "event": "COMMENT",
            "comments": comments,
        }
        try:
            resp = httpx.post(review_endpoint, headers=self.headers, json=payload, timeout=10.0)
            resp.raise_for_status()
            return "Comments have been posted."
        except Exception as e:
            log.error(f"Error posting inline comments: {e}")
            return "Posting comments failed."

# -------- SERVICE INSTANTIATION --------
def get_github_service() -> Optional[GitHubPRService]:
    try:
        return GitHubPRService(
            os.getenv("TOKEN_GITHUB", ""),
            os.getenv("GITHUB_REPO", ""),
            os.getenv("PR_NUMBER", ""),
        )
    except Exception as e:
        log.warning(f"GitHubPRService not available: {e}")
        return None

# -------- LANGCHAIN TOOL WRAPPERS --------

@tool
def fetch_pr_files_tool() -> List[Dict[str, str]]:
    """
    Returns pull request files and unified diffs suitable for code review.
    """
    github = get_github_service()
    if github:
        return github.get_diff_files()
    log.warning("Unable to instantiate GitHubPRService.")
    return []

@tool
def post_inline_comments_tool(comments: List[ReviewComment]) -> str:
    """
    Submits inline code review comments for the associated GitHub pull request.
    """
    github = get_github_service()
    if github:
        return github.submit_review_comments(comments)
    return "Cannot post comments: GitHubPRService unavailable."
