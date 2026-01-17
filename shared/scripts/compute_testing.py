#!/usr/bin/env python3
"""
Compute Testing metrics across repositories and emit docs/data/testing.json.

Metrics:
- coverage_overall, coverage_unit, coverage_integration, coverage_e2e (percent, optional)
- automation_rate (0..1): fraction of workflow runs with testing
- defect_leakage_rate (0..1): bugs opened in window / all issues closed in window

This initial implementation focuses on automation_rate and defect_leakage_rate using
GitHub API. Coverage values are left null until CI exposes standardized coverage artifacts.
"""
import os
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, List
import urllib.request

API = "https://api.github.com"
UTC = timezone.utc
TZ_Z = "+00:00"
WINDOW_DAYS_DEFAULT = int(os.environ.get("TESTING_WINDOW_DAYS", "30"))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

REPOS = [
    ("Honey-Badger-Labs", "sustainnet-observability"),
    ("Honey-Badger-Labs", "sustainnet-website"),
    ("Honey-Badger-Labs", "Family-Meal-Planner"),
    ("Honey-Badger-Labs", "Family-Meal-Planner-App"),
    ("Honey-Badger-Labs", "sustainnet-monorepo"),
]

HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def api_get(url: str) -> Dict:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_workflows(owner: str, repo: str) -> List[Dict]:
    url = f"{API}/repos/{owner}/{repo}/actions/workflows"
    data = api_get(url)
    return data.get("workflows", [])


def list_runs_for_workflow(owner: str, repo: str, workflow_id: int, since: datetime) -> List[Dict]:
    # Note: Created_at filter not directly supported; we will filter client-side
    url = f"{API}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs?per_page=100"
    data = api_get(url)
    runs = data.get("workflow_runs", [])
    out = []
    for r in runs:
        created = r.get("created_at")
        if not created:
            continue
        created_dt = datetime.fromisoformat(created.replace("Z", TZ_Z))
        if created_dt >= since:
            out.append(r)
    return out


def list_issues(owner: str, repo: str, state: str, since: datetime) -> List[Dict]:
    # Using /issues includes PRs; we filter out pull requests by presence of 'pull_request'
    url = f"{API}/repos/{owner}/{repo}/issues?state={state}&per_page=100"
    data = api_get(url)
    items = []
    for it in data:
        if it.get("pull_request"):
            continue
        created = it.get("created_at")
        updated = it.get("updated_at")
        closed = it.get("closed_at")
        # Use updated timestamps for windowing
        ts = closed or updated or created
        if not ts:
            continue
        dt = datetime.fromisoformat(ts.replace("Z", TZ_Z))
        if dt >= since:
            items.append(it)
    return items


def compute_repo_testing(owner: str, repo: str, window_days: int) -> Dict:
    since = datetime.now(tz=UTC) - timedelta(days=window_days)
    workflows = list_workflows(owner, repo)

    total_runs = 0
    test_runs = 0
    for wf in workflows:
        wf_id = wf.get("id")
        if not wf_id:
            continue
        runs = list_runs_for_workflow(owner, repo, wf_id, since)
        total_runs += len(runs)
        for r in runs:
            name = (r.get("name") or "").lower()
            display_title = (r.get("display_title") or "").lower()
            # Count runs that appear to execute tests
            if (
                "test" in name or "test" in display_title or
                "jest" in name or "vitest" in name or "playwright" in name or
                "coverage" in name or "coverage" in display_title
            ):
                test_runs += 1

    automation_rate = (test_runs / total_runs) if total_runs else 0.0

    # Defect leakage approximation: bugs opened in window / closed issues in window
    opened_bugs = [i for i in list_issues(owner, repo, state="open", since=since) if any(l.get("name", "").lower() == "bug" for l in i.get("labels", []))]
    closed_issues = list_issues(owner, repo, state="closed", since=since)
    defect_leakage_rate = (len(opened_bugs) / max(len(closed_issues), 1)) if closed_issues else 0.0

    return {
        "coverage_overall": None,
        "coverage_unit": None,
        "coverage_integration": None,
        "coverage_e2e": None,
        "automation_rate": automation_rate,
        "defect_leakage_rate": defect_leakage_rate,
        "window_days": window_days,
        "timestamp": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
        "repo": f"{owner}/{repo}",
        "source": "github_actions+issues",
    }


def main():
    window_days = WINDOW_DAYS_DEFAULT
    overall = {
        "coverage_overall": None,
        "coverage_unit": None,
        "coverage_integration": None,
        "coverage_e2e": None,
        "automation_rate": 0.0,
        "defect_leakage_rate": 0.0,
    }
    repos_out: Dict[str, Dict] = {}

    for owner, repo in REPOS:
        metrics = compute_repo_testing(owner, repo, window_days)
        repos_out[f"{owner}/{repo}"] = metrics
        # Aggregate automation rate and defect leakage as simple mean
        overall["automation_rate"] += metrics["automation_rate"]
        overall["defect_leakage_rate"] += metrics["defect_leakage_rate"]

        # Coverage remains None until data sources are connected

    if REPOS:
        overall["automation_rate"] /= len(REPOS)
        overall["defect_leakage_rate"] /= len(REPOS)

    out = {
        "overall": overall,
        "repos": repos_out,
        "window_days": window_days,
        "timestamp": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
    }

    # Write to docs/data/testing.json (ensure directory exists)
    target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "data", "testing.json")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote testing metrics to {target_path}")


if __name__ == "__main__":
    main()
