import os
from typing import Literal

import httpx
from mcp.server.fastmcp import FastMCP

GitHubOperation = Literal[
    "get_repository",
    "list_issues",
    "get_file",
]

CommitState = Literal[
    "open",
    "closed",
    "all",
]


def get_github_token() -> str:
    """Get the GitHub Personal Access Token."""

    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    if not token:
        raise ValueError(
            "GITHUB_PERSONAL_ACCESS_TOKEN environment variable "
            "is not configured"
        )

    return token


def github_headers(token: str) -> dict[str, str]:
    """Build GitHub API request headers."""

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def get_repository(
    owner: str,
    repo: str,
    token: str,
) -> dict:
    """Get information about a GitHub repository."""

    url = f"https://api.github.com/repos/{owner}/{repo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=github_headers(token),
        )

    response.raise_for_status()

    return response.json()


async def list_issues(
    owner: str,
    repo: str,
    token: str,
    state: Literal["open", "closed", "all"] = "open",
) -> list[dict]:
    """List issues from a GitHub repository."""

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=github_headers(token),
            params={
                "state": state,
            },
        )

    response.raise_for_status()

    return response.json()


async def get_file(
    owner: str,
    repo: str,
    path: str,
    token: str,
) -> dict:
    """Get a file from a GitHub repository."""

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=github_headers(token),
        )

    response.raise_for_status()

    return response.json()

async def get_commits(
    owner: str,
    repo: str,
    token: str,
    limit: int = 10,
) -> list[dict]:
    """Get recent commits from a GitHub repository."""

    if limit < 1:
        raise ValueError("limit must be greater than zero")

    if limit > 100:
        raise ValueError("limit cannot be greater than 100")

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=github_headers(token),
            params={
                "per_page": limit,
            },
        )

    response.raise_for_status()

    commits = response.json()

    return [
        {
            "sha": commit["sha"],
            "message": commit["commit"]["message"],
            "author": (
                commit["commit"]["author"]["name"]
            ),
            "date": (
                commit["commit"]["author"]["date"]
            ),
            "html_url": commit["html_url"],
        }
        for commit in commits
    ]


async def get_repository_status(
    owner: str,
    repo: str,
    token: str,
) -> dict:
    """Get the current status of a GitHub repository."""

    repository_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}"
    )

    async with httpx.AsyncClient() as client:
        repository_response = await client.get(
            repository_url,
            headers=github_headers(token),
        )

        repository_response.raise_for_status()

        repository = repository_response.json()

        default_branch = repository[
            "default_branch"
        ]

        branch_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/branches/"
            f"{default_branch}"
        )

        branch_response = await client.get(
            branch_url,
            headers=github_headers(token),
        )

        branch_response.raise_for_status()

        branch = branch_response.json()

    return {
        "owner": owner,
        "repository": repo,
        "visibility": repository["visibility"],
        "default_branch": default_branch,
        "protected": branch["protected"],
        "latest_commit_sha": (
            branch["commit"]["sha"]
        ),
        "html_url": repository["html_url"],
    }


async def get_last_change(
    owner: str,
    repo: str,
    token: str,
) -> dict:
    """Get the most recent commit/change."""

    commits = await get_commits(
        owner=owner,
        repo=repo,
        token=token,
        limit=1,
    )

    if not commits:
        raise ValueError(
            "No commits found in the repository"
        )

    return commits[0]


def register(mcp: FastMCP) -> None:
    """Register GitHub MCP tools."""

    @mcp.tool()
    async def github_repository(
        owner: str,
        repo: str,
    ) -> dict:
        """Get information about a GitHub repository.

        Use this tool whenever the user asks for information
        about a GitHub repository.

        Examples:
        - show information about my repository
        - get details for owner/repo
        - what is the description of this GitHub repository

        Args:
            owner: GitHub repository owner or organization.
            repo: GitHub repository name.

        Returns:
            GitHub repository information.
        """

        try:
            token = get_github_token()

            return await get_repository(
                owner=owner,
                repo=repo,
                token=token,
            )

        except (httpx.HTTPError, ValueError) as exc:
            raise ValueError(str(exc)) from exc

    @mcp.tool()
    async def github_issues(
        owner: str,
        repo: str,
        state: Literal["open", "closed", "all"] = "open",
    ) -> list[dict]:
        """List issues from a GitHub repository.

        Use this tool whenever the user asks to see,
        find, or list GitHub issues.

        Examples:
        - show open issues
        - list closed issues
        - show all issues in owner/repo

        Args:
            owner: GitHub repository owner or organization.
            repo: GitHub repository name.
            state: Issue state: open, closed, or all.

        Returns:
            List of GitHub issues.
        """

        try:
            token = get_github_token()

            return await list_issues(
                owner=owner,
                repo=repo,
                token=token,
                state=state,
            )

        except (httpx.HTTPError, ValueError) as exc:
            raise ValueError(str(exc)) from exc

    @mcp.tool()
    async def github_file(
        owner: str,
        repo: str,
        path: str,
    ) -> dict:
        """Get a file from a GitHub repository.

        Use this tool whenever the user asks to read
        a file from a GitHub repository.

        Examples:
        - read README.md
        - get src/main.py
        - show the contents of config.json

        Args:
            owner: GitHub repository owner or organization.
            repo: GitHub repository name.
            path: Path to the file inside the repository.

        Returns:
            GitHub file metadata and content information.
        """

        try:
            token = get_github_token()

            return await get_file(
                owner=owner,
                repo=repo,
                path=path,
                token=token,
            )

        except (httpx.HTTPError, ValueError) as exc:
            raise ValueError(str(exc)) from exc

    @mcp.tool()
    async def github_commits(
        owner: str,
        repo: str,
        limit: int = 10,
    ) -> list[dict]:
        """Get recent commits from a GitHub repository.

        Use this tool when the user asks about:
        - recent commits
        - commit history
        - latest commits
        - who committed changes
        - recent changes

        Args:
            owner: GitHub repository owner or organization.
            repo: GitHub repository name.
            limit: Number of commits to return.

        Returns:
            A list of recent commits.
        """

        try:
            token = get_github_token()

            return await get_commits(
                owner=owner,
                repo=repo,
                token=token,
                limit=limit,
            )

        except (httpx.HTTPError, ValueError) as exc:
            raise ValueError(str(exc)) from exc

    @mcp.tool()
    async def github_status(
        owner: str,
        repo: str,
    ) -> dict:
        """Get the current status of a GitHub repository.

        Use this tool when the user asks:
        - what is the repository status
        - what branch is the repository using
        - what is the latest commit
        - is the branch protected
        - show repository information

        Args:
            owner: GitHub repository owner or organization.
            repo: GitHub repository name.

        Returns:
            Current repository status.
        """

        try:
            token = get_github_token()

            return await get_repository_status(
                owner=owner,
                repo=repo,
                token=token,
            )

        except (httpx.HTTPError, ValueError) as exc:
            raise ValueError(str(exc)) from exc

    @mcp.tool()
    async def github_last_change(
        owner: str,
        repo: str,
    ) -> dict:
        """Get the latest change in a GitHub repository.

        Use this tool when the user asks:
        - what was the last change
        - what changed most recently
        - what was the latest commit
        - who made the last change
        - when was the repository last changed

        Args:
            owner: GitHub repository owner or organization.
            repo: GitHub repository name.

        Returns:
            Information about the latest commit.
        """

        try:
            token = get_github_token()

            return await get_last_change(
                owner=owner,
                repo=repo,
                token=token,
            )

        except (httpx.HTTPError, ValueError) as exc:
            raise ValueError(str(exc)) from exc

