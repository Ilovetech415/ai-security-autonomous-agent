from models.schemas import ThreatEvent, ThreatScoreResult, DecisionResult


def decide_action(event: ThreatEvent, score_result: ThreatScoreResult) -> DecisionResult:
    score = score_result.score
    severity = score_result.severity

    # CRITICAL → immediate block
    if severity == "critical":
        return DecisionResult(
            action="block",
            reason="Critical threat detected. Immediate block required.",
            cooldown_minutes=60
        )

    # HIGH → block or rate limit depending on indicators
    if severity == "high":
        if event.known_bad_actor or event.payload_signature_match:
            return DecisionResult(
                action="block",
                reason="High-risk threat with confirmed malicious indicators.",
                cooldown_minutes=45
            )
        return DecisionResult(
            action="rate_limit",
            reason="High-risk activity detected. Rate limiting to reduce exposure.",
            cooldown_minutes=30
        )

    # MEDIUM → rate limit or monitor
    if severity == "medium":
        if event.failed_attempts >= 10 or event.request_count >= 500:
            return DecisionResult(
                action="rate_limit",
                reason="Medium-risk pattern with elevated activity volume.",
                cooldown_minutes=15
            )
        return DecisionResult(
            action="monitor",
            reason="Medium-risk event requires observation.",
            cooldown_minutes=10
        )

    # LOW → monitor only
    return DecisionResult(
        action="monitor",
        reason="Low-risk event logged for observation only.",
        cooldown_minutes=5
    )
