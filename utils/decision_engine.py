from models.schemas import ThreatEvent, ThreatScoreResult, DecisionResult
from utils.memory_store import get_attacker_profile


def decide_action(event: ThreatEvent, score_result: ThreatScoreResult) -> DecisionResult:
    severity = score_result.severity
    profile = get_attacker_profile(event.source_ip)

    repeat_offender = profile["threat_count"] >= 3
    high_volume = profile["total_requests"] >= 10

    # 🔥 Escalation logic
    if repeat_offender:
        return DecisionResult(
            action="block",
            reason="Repeat offender detected. Escalating to permanent block.",
            cooldown_minutes=120
        )

    if high_volume and severity in ["medium", "high"]:
        return DecisionResult(
            action="block",
            reason="High-frequency attacker detected.",
            cooldown_minutes=60
        )

    # Original logic fallback
    if severity == "critical":
        return DecisionResult(
            action="block",
            reason="Critical threat detected.",
            cooldown_minutes=60
        )

    if severity == "high":
        return DecisionResult(
            action="rate_limit",
            reason="High-risk activity.",
            cooldown_minutes=30
        )

    if severity == "medium":
        return DecisionResult(
            action="monitor",
            reason="Medium-risk activity.",
            cooldown_minutes=10
        )

    return DecisionResult(
        action="monitor",
        reason="Low-risk activity.",
        cooldown_minutes=5
    )
