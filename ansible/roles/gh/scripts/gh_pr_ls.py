#!/usr/bin/env python3
"""List pull requests with mergeability and CI status details."""
from __future__ import annotations

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

Command = List[str]


class PullRequestAuthor(BaseModel):
    """Minimal author representation from GitHub."""

    model_config = ConfigDict(extra="ignore")

    login: Optional[str] = None


class PullRequest(BaseModel):
    """Pull request details returned by the GitHub CLI."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    number: int
    title: Optional[str] = None
    author: Optional[PullRequestAuthor] = None
    head_ref_name: str = Field(alias="headRefName")
    state: Optional[str] = None
    mergeable: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _coerce_author(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        author = values.get("author")
        if isinstance(author, str):
            values["author"] = {"login": author}
        return values

    def author_login(self) -> Optional[str]:
        if self.author:
            return self.author.login
        return None


def _print_error(message: str) -> None:
    """Print an error message to stderr."""
    print(f"❌ {message}", file=sys.stderr)


def _parse_json(output: str, description: str) -> Any:
    try:
        return json.loads(output)
    except (
        json.JSONDecodeError
    ) as exc:  # pragma: no cover - exercised via error path tests
        _print_error(f"Failed to parse JSON from '{description}': {exc}")
        raise SystemExit(1) from exc


async def run_command(
    command: Command,
    *,
    expect_json: bool = False,
    default: Any = None,
    exit_on_error: bool = True,
    description: Optional[str] = None,
) -> Any:
    """Run a command and optionally parse its JSON output."""
    desc = description or " ".join(command)
    try:
        completed = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=True,
        )
        stdout, stderr = await completed.communicate()
        if completed.returncode != 0:
            message = f"Command '{desc}' failed with exit code {completed.returncode}"
            if stderr:
                message = f"{message}: {stderr.strip()}"
            if exit_on_error:
                _print_error(message)
                raise SystemExit(completed.returncode or 1)
            _print_error(message)
            return default
    except FileNotFoundError as exc:
        _print_error(f"Command not found while executing '{desc}'")
        raise SystemExit(1) from exc

    output = stdout.strip()
    if expect_json:
        if not output:
            return default
        return _parse_json(output, desc)
    return output


async def _actions_in_progress(branch: str) -> str:
    data = await run_command(
        [
            "gh",
            "run",
            "list",
            "--branch",
            branch,
            "--status",
            "in_progress",
            "--limit",
            "1",
            "--json",
            "databaseId",
        ],
        expect_json=True,
        default=[],
        exit_on_error=False,
        description=f"gh run list --branch {branch} --status in_progress",
    )
    if isinstance(data, list) and data:
        return "true"
    return "false"


async def _latest_ci_status(branch: str) -> str:
    data = await run_command(
        [
            "gh",
            "run",
            "list",
            "--branch",
            branch,
            "--limit",
            "1",
            "--json",
            "status,conclusion",
        ],
        expect_json=True,
        default=[],
        exit_on_error=False,
        description=f"gh run list --branch {branch}",
    )
    if isinstance(data, list) and data:
        run = data[0]
        if isinstance(run, dict):
            status = run.get("status")
            conclusion = run.get("conclusion")
            if status == "completed" and isinstance(conclusion, str):
                return conclusion
            if isinstance(status, str):
                return status
    return "none"


async def gather_pull_requests(limit: int = 20) -> List[Dict[str, Any]]:
    prs_raw = await run_command(
        [
            "gh",
            "pr",
            "list",
            "--limit",
            str(limit),
            "--json",
            "number,title,author,headRefName,state,mergeable",
        ],
        expect_json=True,
        default=[],
        description="gh pr list",
    )

    if not isinstance(prs_raw, list):
        _print_error("Unexpected response from 'gh pr list'")
        raise SystemExit(1)

    pull_requests: List[PullRequest] = []
    for pr in prs_raw:
        if not isinstance(pr, dict):
            continue
        try:
            pull_requests.append(PullRequest.model_validate(pr))
        except ValidationError as exc:
            _print_error(f"Invalid pull request data: {exc}")
            raise SystemExit(1) from exc

    branches = [pr.head_ref_name for pr in pull_requests]

    summaries: List[Dict[str, Any]] = []
    for pr in pull_requests:
        summaries.append(
            {
                "number": pr.number,
                "title": pr.title,
                "author": pr.author_login(),
                "branch": pr.head_ref_name,
                "state": pr.state,
                "mergeable": pr.mergeable or "UNKNOWN",
            }
        )

    if not branches:
        return summaries

    actions_tasks = [asyncio.create_task(_actions_in_progress(branch)) for branch in branches]
    ci_tasks = [asyncio.create_task(_latest_ci_status(branch)) for branch in branches]

    actions_results = await asyncio.gather(*actions_tasks)
    ci_results = await asyncio.gather(*ci_tasks)

    for summary, actions_result, ci_result in zip(summaries, actions_results, ci_results):
        summary["actions_in_progress"] = actions_result
        summary["ci_status"] = ci_result

    return summaries


async def main() -> int:
    pull_requests = await gather_pull_requests()
    for pr in pull_requests:
        print(json.dumps(pr, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
