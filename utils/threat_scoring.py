from models.schemas import ThreatEvent, ThreatScoreResult


def calculate_threat_score(event: ThreatEvent) -> ThreatScoreResult:
    score = 0
    factors = []

    # Base weights per event type
    event_type_weights = {
        "brute_force": 30,
        "port_scan": 20,
        "suspicious_login": 25,
        "malware_activity": 40,
        "data_exfiltration": 50,
        "privilege_escalation": 45,
    }

    base_weight = event_type_weights.get(event.event_type, 10)
    score += base_weight
    factors.append(f"event_type:{event.event_type} (+{base_weight})")

    # Failed attempts scoring
    if event.failed_attempts >= 20:
        score += 25
        factors.append("failed_attempts>=20 (+25)")
    elif event.failed_attempts >= 10:
        score += 15
        factors.append("failed_attempts>=10 (+15)")
    elif event.failed_attempts >= 5:
        score += 8
        factors.append("failed_attempts>=5 (+8)")

    # Request volume scoring
    if event.request_count >= 1000:
        score += 25
        factors.append("request_count>=1000 (+25)")
    elif event.request_count >= 500:
        score += 15
        factors.append("request_count>=500 (+15)")
    elif event.request_count >= 100:
        score += 8
        factors.append("request_count>=100 (+8)")

    # Behavioral indicators
    if event.geo_anomaly:
        score += 10
        factors.append("geo_anomaly (+10)")

    if event.off_hours:
        score += 10
        factors.append("off_hours (+10)")

    if event.known_bad_actor:
        score += 30
        factors.append("known_bad_actor (+30)")

    if event.payload_signature_match:
        score += 35
        factors.append("payload_signature_match (+35)")

    # Cap score at 100
    score = min(score, 100)

    # Severity classification
    if score >= 85:
        severity = "critical"
    elif score >= 65:
        severity = "high"
    elif score >= 35:
        severity = "medium"
    else:
        severity = "low"

    return ThreatScoreResult(
        score=score,
        severity=severity,
        factors=factors
    )
