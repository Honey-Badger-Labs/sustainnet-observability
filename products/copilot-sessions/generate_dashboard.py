#!/usr/bin/env python3
"""
Generate Copilot Session Dashboard from session logs.

Reads from: sustainnet-observability/logs/copilot-sessions/
Outputs: Dashboard metrics and visualizations

Usage:
    python generate_dashboard.py [--days 7] [--output dashboard.json]
"""

import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, List
from collections import Counter

# South African Standard Time
SAST = timezone(timedelta(hours=2))

# Paths
SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR.parent.parent / "logs" / "copilot-sessions"


def load_sessions(days: int = 7) -> List[Dict[str, Any]]:
    """Load sessions from the last N days."""
    sessions = []
    cutoff = datetime.now(SAST) - timedelta(days=days)
    
    if not LOG_DIR.exists():
        print(f"Warning: Log directory not found at {LOG_DIR}")
        return []
    
    for log_file in LOG_DIR.glob("sessions-*.jsonl"):
        with open(log_file) as f:
            for line in f:
                try:
                    session = json.loads(line)
                    session_time = datetime.fromisoformat(session["start_time"])
                    if session_time >= cutoff:
                        sessions.append(session)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Warning: Skipping invalid log entry: {e}")
    
    return sessions


def calculate_metrics(sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate dashboard metrics from sessions."""
    if not sessions:
        return {"error": "No sessions found", "sessions_count": 0}
    
    # Basic counts
    total_sessions = len(sessions)
    total_duration = sum(s.get("duration_minutes", 0) for s in sessions)
    
    # Decision metrics
    total_decisions = sum(s["metrics"]["total_decisions"] for s in sessions)
    total_escalations = sum(s["metrics"]["total_escalations"] for s in sessions)
    total_overrides = sum(s["metrics"]["total_overrides"] for s in sessions)
    
    # Outcome distribution
    outcomes = Counter(s.get("outcome", "unknown") for s in sessions)
    
    # Agent distribution
    agents = Counter(s.get("agent", "unknown") for s in sessions)
    
    # Model distribution
    models = Counter(s.get("model", "unknown") for s in sessions)
    
    # Feedback scores
    feedback_scores = [s["feedback_score"] for s in sessions if s.get("feedback_score")]
    avg_feedback = sum(feedback_scores) / len(feedback_scores) if feedback_scores else None
    
    # Calculate rates
    escalation_rate = total_escalations / max(total_decisions, 1)
    override_rate = total_overrides / max(total_decisions, 1)
    accuracy_estimate = 1 - override_rate
    
    # Time saved estimate (assuming 30 min saved per successful session)
    successful_sessions = outcomes.get("success", 0)
    time_saved_hours = (successful_sessions * 30) / 60
    
    # Trust score calculation
    trust_components = {
        "accuracy": min(accuracy_estimate, 1.0) * 3,  # Max 3 points
        "low_escalation": max(0, 1 - escalation_rate * 10) * 2,  # Max 2 points
        "feedback": (avg_feedback / 5 * 2) if avg_feedback else 1,  # Max 2 points
        "completion": (outcomes.get("success", 0) / max(total_sessions, 1)) * 2,  # Max 2 points
        "predictability": 1  # Base point for having logging
    }
    trust_score = sum(trust_components.values())
    
    return {
        "generated_at": datetime.now(SAST).isoformat(),
        "period_days": 7,
        "summary": {
            "total_sessions": total_sessions,
            "total_duration_minutes": round(total_duration, 1),
            "avg_duration_minutes": round(total_duration / total_sessions, 1),
            "total_decisions": total_decisions,
            "decisions_per_session": round(total_decisions / total_sessions, 1),
            "time_saved_hours": round(time_saved_hours, 1)
        },
        "quality": {
            "accuracy_estimate": round(accuracy_estimate * 100, 1),
            "escalation_rate": round(escalation_rate * 100, 1),
            "override_rate": round(override_rate * 100, 1),
            "avg_feedback_score": round(avg_feedback, 2) if avg_feedback else None
        },
        "trust": {
            "score": round(trust_score, 1),
            "max_score": 10,
            "components": {k: round(v, 2) for k, v in trust_components.items()}
        },
        "distributions": {
            "outcomes": dict(outcomes),
            "agents": dict(agents),
            "models": dict(models)
        },
        "counts": {
            "escalations": total_escalations,
            "overrides": total_overrides,
            "feedback_responses": len(feedback_scores)
        }
    }


def format_dashboard(metrics: Dict[str, Any]) -> str:
    """Format metrics as a human-readable dashboard."""
    if "error" in metrics:
        return f"Dashboard Error: {metrics['error']}"
    
    s = metrics["summary"]
    q = metrics["quality"]
    t = metrics["trust"]
    
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI COPILOT DASHBOARD                                 Generated: {metrics['generated_at'][:16]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY (Last {metrics['period_days']} Days)
   Sessions:     {s['total_sessions']:>6}
   Duration:     {s['total_duration_minutes']:>6} min total ({s['avg_duration_minutes']} min avg)
   Decisions:    {s['total_decisions']:>6} ({s['decisions_per_session']}/session)
   Time Saved:   {s['time_saved_hours']:>6} hours (estimated)

📈 QUALITY METRICS
   Accuracy:     {q['accuracy_estimate']:>6}%
   Escalations:  {q['escalation_rate']:>6}%
   Overrides:    {q['override_rate']:>6}%
   Feedback:     {q['avg_feedback_score'] or 'N/A':>6}

🎯 TRUST SCORE: {t['score']}/{t['max_score']}
   Components:
   - Accuracy:      {t['components']['accuracy']:.1f}/3
   - Low Escalation:{t['components']['low_escalation']:.1f}/2
   - Feedback:      {t['components']['feedback']:.1f}/2
   - Completion:    {t['components']['completion']:.1f}/2
   - Predictability:{t['components']['predictability']:.1f}/1

📋 OUTCOME DISTRIBUTION
   {chr(10).join(f"   {k}: {v}" for k, v in metrics['distributions']['outcomes'].items())}

🤖 AGENT USAGE
   {chr(10).join(f"   {k}: {v}" for k, v in metrics['distributions']['agents'].items())}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def main():
    parser = argparse.ArgumentParser(description="Generate Copilot Session Dashboard")
    parser.add_argument("--days", type=int, default=7, help="Days of data to include")
    parser.add_argument("--output", type=str, help="Output file for JSON metrics")
    parser.add_argument("--format", choices=["json", "text", "both"], default="both")
    
    args = parser.parse_args()
    
    print(f"Loading sessions from last {args.days} days...")
    sessions = load_sessions(args.days)
    print(f"Found {len(sessions)} sessions")
    
    metrics = calculate_metrics(sessions)
    
    if args.format in ["text", "both"]:
        print(format_dashboard(metrics))
    
    if args.format in ["json", "both"]:
        if args.output:
            with open(args.output, "w") as f:
                json.dump(metrics, f, indent=2)
            print(f"Metrics written to {args.output}")
        elif args.format == "json":
            print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
