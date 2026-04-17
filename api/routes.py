from fastapi import APIRouter
from datetime import datetime

from models.schemas import (
    ThreatEvent,
    AgentResponse,
    ResponseExecutionResult,
)
from utils.threat_scoring import calculate_threat_score
from utils.decision_engine import decide_action
from utils.logger import log_agent_action

router = APIRouter()


def simulate_response_execution(source_ip: str, action: str, cooldown_minutes: int) -> ResponseExecutionResult:
    if action == "block":
        details = f"Simulated firewall block applied to {source_ip} for {cooldown_minutes} minutes."
    elif action == "rate_limit":
        details = f"Simulated rate limit applied to {source_ip} for {cooldown_minutes} minutes."
    else:
        details = f"Simulated enhanced monitoring enabled for {source_ip}."

    return ResponseExecutionResult(
        status="success",
        action_taken=action,
        source_ip=source_ip,
        details=details,
        executed_at=datetime.utcnow()
    )


@router.get("/")
def health_check():
    return {"status": "ok", "service": "AI Security Autonomous Agent"}


@router.post("/agent/respond", response_model=AgentResponse)
def autonomous_response(event: ThreatEvent):
    # 1. Score the threat
    threat_score = calculate_threat_score(event)

    # 2. Decide what to do
    decision = decide_action(event, threat_score)

    # 3. Execute (simulated for now)
    execution = simulate_response_execution(
        source_ip=event.source_ip,
        action=decision.action,
        cooldown_minutes=decision.cooldown_minutes
    )

    # 4. Log everything
    log_agent_action(event, threat_score, decision, execution)

    # 5. Return full agent response
    return AgentResponse(
        event=event,
        threat_score=threat_score,
        decision=decision,
        execution=execution
    )
