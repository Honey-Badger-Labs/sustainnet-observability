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
from typing import Dict, List
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
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code} fetching {url}: {e.reason}")
        raise
    except urllib.error.URLError as e:
        print(f"URL error fetching {url}: {e.reason}")
        raise


def list_workflows(owner: str, repo: str) -> List[Dict]:
    workflows: List[Dict] = []
    page = 1
    while True:
        url = f"{API}/repos/{owner}/{repo}/actions/workflows?per_page=100&page={page}"
        data = api_get(url)
        page_workflows = data.get("workflows", [])
        if not page_workflows:
            break
        workflows.extend(page_workflows)
        if len(page_workflows) < 100:
            break
        page += 1
    return workflows


def list_runs_for_workflow(owner: str, repo: str, workflow_id: int, since: datetime) -> List[Dict]:
    # Note: Created_at filter not directly supported; we will filter client-side
    out: List[Dict] = []
    page = 1
    while True:
        url = f"{API}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs?per_page=100&page={page}"
        data = api_get(url)
        runs = data.get("workflow_runs", [])
        if not runs:
            break
        for r in runs:
            created = r.get("created_at")
            if not created:
                continue
            created_dt = datetime.fromisoformat(created.replace("Z", TZ_Z))
            if created_dt >= since:
                out.append(r)
        if len(runs) < 100:
            break
        page += 1
    return out


def list_issues(owner: str, repo: str, state: str, since: datetime) -> List[Dict]:
    # Using /issues includes PRs; we filter out pull requests by presence of 'pull_request'
    items: List[Dict] = []
    page = 1
    while True:
        url = f"{API}/repos/{owner}/{repo}/issues?state={state}&per_page=100&page={page}"
        data = api_get(url)
        # GitHub returns a list of issues for this endpoint
        if not data:
            break
        page_has_recent = False
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
                page_has_recent = True
                items.append(it)
        # Issues are returned in descending order of recency; once a page has no
        # items in the window, subsequent pages will be older as well.
        if not page_has_recent:
            break
        page += 1
    return items


def compute_repo_testing(owner: str, repo: str, window_days: int) -> Dict:
    since = datetime.now(tz=UTC) - timedelta(days=window_days)
    workflows = list_workflows(owner, repo)

    total_runs = 0
    test_runs = 0
    for wf in workflows:
        wf_id = wf.get("id")
        wf_name = (wf.get("name") or "").lower()
        wf_path = (wf.get("path") or "").lower()
        if not wf_id:
            continue
        # Only count workflows that are actually test workflows
        # Match patterns like "test.yml", "run-tests", "ci-test", etc.
        # Exclude pure deployment workflows but keep "deploy-tests", "test-deploy", etc.
        test_keywords = ["test", "jest", "vitest", "playwright", "cypress", "e2e", "unit-test", "integration-test"]
        has_test_keyword = any(keyword in wf_name or keyword in wf_path for keyword in test_keywords)
        # It's a test workflow if it has test keywords and isn't ONLY about deployment
        is_test_workflow = has_test_keyword and not (
            ("deploy" in wf_name or "deploy" in wf_path) and 
            not any(test_kw in wf_name or test_kw in wf_path for test_kw in ["test"])
        )
        if not is_test_workflow:
            continue
        runs = list_runs_for_workflow(owner, repo, wf_id, since)
        total_runs += len(runs)
        # Count successful test runs
        for r in runs:
            # Only count runs that completed (success or failure are both valid test runs)
            conclusion = (r.get("conclusion") or "").lower()
            if conclusion in ["success", "failure"]:
                test_runs += 1

    automation_rate = (test_runs / total_runs) if total_runs else 0.0

    # Defect leakage: bugs found in production (opened recently) vs total closed features/fixes
    # A more accurate measure: bugs labeled as 'bug' opened in window / closed issues that were enhancements or features
    all_opened = list_issues(owner, repo, state="open", since=since)
    opened_bugs = [i for i in all_opened if any(l.get("name", "").lower() == "bug" for l in i.get("labels", []))]
    closed_issues = list_issues(owner, repo, state="closed", since=since)
    # Filter closed issues to exclude bugs (we want features/enhancements closed)
    closed_non_bugs = [i for i in closed_issues if not any(l.get("name", "").lower() == "bug" for l in i.get("labels", []))]
    # Defect leakage = bugs found / work items delivered
    # Return None if no work was delivered in the window (can't calculate meaningful rate)
    defect_leakage_rate = (len(opened_bugs) / len(closed_non_bugs)) if len(closed_non_bugs) > 0 else None

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
        "defect_leakage_rate": 0.0,  # Will be set to None if no repos have data
    }
    repos_out: Dict[str, Dict] = {}

    for owner, repo in REPOS:
        metrics = compute_repo_testing(owner, repo, window_days)
        repos_out[f"{owner}/{repo}"] = metrics
        # Aggregate automation rate and defect leakage as simple mean
        overall["automation_rate"] += metrics["automation_rate"]
        # Only aggregate defect leakage if it's not None
        if metrics["defect_leakage_rate"] is not None:
            overall["defect_leakage_rate"] += metrics["defect_leakage_rate"]

        # Coverage remains None until data sources are connected

    if REPOS:
        overall["automation_rate"] /= len(REPOS)
        # Only average defect leakage if we have data
        repos_with_leakage = sum(1 for r in repos_out.values() if r["defect_leakage_rate"] is not None)
        if repos_with_leakage > 0:
            overall["defect_leakage_rate"] /= repos_with_leakage
        else:
            overall["defect_leakage_rate"] = None

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
