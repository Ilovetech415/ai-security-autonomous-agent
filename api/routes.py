from agent_core import Agent

agent = Agent()
from fastapi import APIRouter
from datetime import datetime

from models.schemas import (
    ThreatEvent,
    ResponseExecutionResult,
)
from utils.threat_scoring import calculate_threat_score
from utils.decision_engine import decide_action
from utils.logger import log_agent_action
from utils.memory_store import update_attacker

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
    return {
        "status": "ok",
        "service": "AI Security Autonomous Agent"
    }


@router.post("/agent/respond")
def autonomous_response(event: ThreatEvent):
    # 1. Score the threat
    threat_score = calculate_threat_score(event)

    # 2. Update attacker memory (NEW 🔥)
    attacker_profile = update_attacker(
        ip=event.source_ip,
        score=threat_score.score
    )

    # 3. Decide action using BOTH score + memory
    decision = decide_action(event, threat_score)

    # 4. Execute simulated response
    execution = simulate_response_execution(
        source_ip=event.source_ip,
        action=decision.action,
        cooldown_minutes=decision.cooldown_minutes
    )

    # 5. Log everything
    log_agent_action(event, threat_score, decision, execution)

    # 6. Return full system state (VERY IMPORTANT FOR SENIOR LOOK)
    return {
        "event": event,
        "threat_score": threat_score,
        "decision": decision,
        "execution": execution,
        "attacker_profile": attacker_profile
    }
