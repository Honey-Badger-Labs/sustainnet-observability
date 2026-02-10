#!/usr/bin/env python3
"""
Compute DORA metrics across SustainNet repositories using GitHub API.

Outputs JSON to docs/data/dora.json with:
- deployment_frequency (per day, last 30 days)
- lead_time_hours (median hours from commit to production deploy)
- change_failure_rate (failed prod deploys / total prod deploys)
- time_to_restore_hours (avg hours from failed prod deploy to next success)

Environment:
  GITHUB_TOKEN (recommended; falls back to unauthenticated limited access)

Usage:
  python3 shared/scripts/compute_dora.py --window-days 30 --repos-file shared/scripts/repos.txt
"""

import argparse
import json
import os
import statistics
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests

API = "https://api.github.com"
UTC = timezone.utc
TZ_Z = "+00:00"

# Explicit production workflow hints per repo (filenames or tokens)
PRODUCTION_HINTS = {
    "Honey-Badger-Labs/sustainnet-observability": ["production-deploy.yml", "production-deploy"],
    "Honey-Badger-Labs/sustainnet-website": ["production", "deploy", "prod", "production-deploy"],
    "Honey-Badger-Labs/Family-Meal-Planner": ["prod", "production", "deploy"],
    "Honey-Badger-Labs/Family-Meal-Planner-App": ["prod", "production", "deploy"],
    "Honey-Badger-Labs/sustainnet-monorepo": ["prod", "production", "deploy"],
}


def iso(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat().replace(TZ_Z, "Z")


def gh_get(url: str, token: Optional[str], params: Dict = None) -> Dict:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, params=params or {})
    r.raise_for_status()
    return r.json()


def list_workflows(owner: str, repo: str, token: Optional[str]) -> List[Dict]:
    out = []
    page = 1
    while True:
        data = gh_get(f"{API}/repos/{owner}/{repo}/actions/workflows", token, {"per_page": 100, "page": page})
        out.extend(data.get("workflows", []))
        if len(data.get("workflows", [])) < 100:
            break
        page += 1
    return out


def list_runs_for_workflow(owner: str, repo: str, workflow_id: int, token: Optional[str], since: datetime) -> List[Dict]:
    out = []
    page = 1
    while True:
        data = gh_get(
            f"{API}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs",
            token,
            {"per_page": 100, "page": page, "created": f">={iso(since)}"},
        )
        out.extend(data.get("workflow_runs", []))
        if len(data.get("workflow_runs", [])) < 100:
            break
        page += 1
    return out


def get_commit(owner: str, repo: str, sha: str, token: Optional[str]) -> Optional[Dict]:
    try:
        return gh_get(f"{API}/repos/{owner}/{repo}/commits/{sha}", token)
    except requests.HTTPError:
        return None


def is_production_run(run: Dict, owner: str, repo: str) -> bool:
    name = (run.get("name") or "").lower()
    display_title = (run.get("display_title") or "").lower()
    path = (run.get("path") or "").lower()
    full = f"{owner}/{repo}"
    tokens = PRODUCTION_HINTS.get(full, [])
    # Exact token match first
    for t in tokens:
        if t.lower() in name or t.lower() in display_title or t.lower() in path:
            return True
    # Fallback heuristic: look for production+deployment patterns
    text = " ".join([name, display_title, path])
    has_prod = any(kw in text for kw in ("prod", "production"))
    has_deploy = any(kw in text for kw in ("deploy", "release", "deployment"))
    # Accept if both production and deployment indicators, OR if just production (tends to be explicit)
    # Check for main/master branch but use word boundaries to avoid false matches
    has_main_branch = any(branch in text.split() for branch in ("main", "master"))
    return has_prod or (has_deploy and has_main_branch)


def compute_repo_metrics(owner: str, repo: str, token: Optional[str], window_days: int) -> Dict:
    since = datetime.now(UTC) - timedelta(days=window_days)
    workflows = list_workflows(owner, repo, token)
    prod_runs: List[Dict] = []

    for wf in workflows:
        runs = list_runs_for_workflow(owner, repo, wf["id"], token, since)
        prod_runs.extend([r for r in runs if is_production_run(r, owner, repo)])

    if not prod_runs:
        return {
            "deployments": 0,
            "deployment_frequency_per_day": 0,
            "lead_time_hours_median": None,
            "change_failure_rate": None,
            "time_to_restore_hours_avg": None,
        }

    # Sort by created_at
    prod_runs.sort(key=lambda r: r.get("created_at") or r.get("run_started_at") or "")

    total = len(prod_runs)
    failures = [r for r in prod_runs if (r.get("conclusion") or "").lower() in {"failure", "cancelled", "timed_out"}]
    successes = [r for r in prod_runs if (r.get("conclusion") or "").lower() == "success"]

    # Deployment frequency
    dep_freq = round(total / float(window_days), 3)

    # Lead time: from head commit author date to run updated_at
    lead_times: List[float] = []
    skipped_commits = 0
    for r in successes:
        head_sha = r.get("head_sha")
        updated_at = r.get("updated_at") or r.get("created_at") or r.get("run_started_at")
        if not head_sha or not updated_at:
            continue
        commit = get_commit(owner, repo, head_sha, token)
        if not commit:
            skipped_commits += 1
            continue
        commit_dt_s = (
            commit.get("commit", {})
            .get("author", {})
            .get("date")
        ) or commit.get("commit", {}).get("committer", {}).get("date")
        if not commit_dt_s:
            continue
        try:
            commit_dt = datetime.fromisoformat(commit_dt_s.replace("Z", TZ_Z))
            done_dt = datetime.fromisoformat(updated_at.replace("Z", TZ_Z))
            hours = (done_dt - commit_dt).total_seconds() / 3600.0
            if hours >= 0:
                lead_times.append(hours)
        except Exception:
            continue
    
    if skipped_commits > 0:
        print(f"Warning: Skipped {skipped_commits} deployments due to missing commit data for {owner}/{repo}")

    lead_median = round(statistics.median(lead_times), 2) if lead_times else None

    # Change failure rate
    cfr = round(len(failures) / total, 3) if total else None

    # Time to restore: for each failed run, time until next success
    ttrs: List[float] = []
    for i, fr in enumerate(prod_runs):
        concl = (fr.get("conclusion") or "").lower()
        if concl not in {"failure", "cancelled", "timed_out"}:
            continue
        fail_time_s = fr.get("updated_at") or fr.get("created_at") or fr.get("run_started_at")
        if not fail_time_s:
            continue
        fail_time = datetime.fromisoformat(fail_time_s.replace("Z", TZ_Z))
        # Find next success after this index
        for nr in prod_runs[i + 1 :]:
            if (nr.get("conclusion") or "").lower() == "success":
                succ_time_s = nr.get("updated_at") or nr.get("created_at") or nr.get("run_started_at")
                if succ_time_s:
                    succ_time = datetime.fromisoformat(succ_time_s.replace("Z", TZ_Z))
                    delta_h = (succ_time - fail_time).total_seconds() / 3600.0
                    if delta_h >= 0:
                        ttrs.append(delta_h)
                break

    ttr_avg = round(sum(ttrs) / len(ttrs), 2) if len(ttrs) > 0 else None

    return {
        "deployments": total,
        "deployment_frequency_per_day": dep_freq,
        "lead_time_hours_median": lead_median,
        "change_failure_rate": cfr,
        "time_to_restore_hours_avg": ttr_avg,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--window-days", type=int, default=30)
    parser.add_argument("--repos-file", type=str, default=None)
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

    # Default SustainNet repos if no file provided
    # All SustainNet repos except observability are private. GitHub Actions' default
    # GITHUB_TOKEN lacks cross-repo access. To include private repos, set up a
    # Personal Access Token (PAT) with 'repo' scope and pass via --repos-file.
    # Only the public repo is queried by default.
    default_repos = [
        "Honey-Badger-Labs/sustainnet-observability",  # Only public repo
    ]

    repos: List[str] = []
    if args.repos_file and os.path.exists(args.repos_file):
        with open(args.repos_file) as f:
            repos = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    else:
        repos = default_repos

    aggregate = {
        "window_days": args.window_days,
        "generated_at": iso(datetime.now(UTC)),
        "repos": {},
    }

    totals = {
        "deployments": 0,
        "deployment_frequency_per_day": 0.0,
        "lead_times": [],
        "failures": 0,
        "successes": 0,
        "ttrs": [],
    }

    for full in repos:
        try:
            owner, repo = full.split("/", 1)
        except ValueError:
            continue
        metrics = compute_repo_metrics(owner, repo, token, args.window_days)
        aggregate["repos"][full] = metrics

        totals["deployments"] += metrics.get("deployments", 0) or 0
        totals["deployment_frequency_per_day"] += metrics.get("deployment_frequency_per_day", 0.0) or 0.0
        if metrics.get("lead_time_hours_median") is not None:
            totals["lead_times"].append(metrics["lead_time_hours_median"])  # aggregate medians for simplicity
        # We cannot count failures/successes directly without raw runs; approximate CFR by weighting
        if metrics.get("change_failure_rate") is not None and metrics.get("deployments"):
            fail_count = int(round(metrics["change_failure_rate"] * metrics["deployments"]))
            succ_count = metrics["deployments"] - fail_count
            totals["failures"] += fail_count
            totals["successes"] += succ_count
        if metrics.get("time_to_restore_hours_avg") is not None:
            totals["ttrs"].append(metrics["time_to_restore_hours_avg"])

    overall = {
        "deployment_frequency_per_day": round(totals["deployment_frequency_per_day"], 3),
        "lead_time_hours_median": round(statistics.median(totals["lead_times"])) if totals["lead_times"] else None,
        "change_failure_rate": round(
            totals["failures"] / (totals["failures"] + totals["successes"]), 3
        ) if (totals["failures"] + totals["successes"]) else None,
        "time_to_restore_hours_avg": round(sum(totals["ttrs"]) / len(totals["ttrs"]), 2) if totals["ttrs"] else None,
    }

    aggregate["overall"] = overall

    out_path = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "data", "dora.json")
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(aggregate, f, indent=2)

    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
