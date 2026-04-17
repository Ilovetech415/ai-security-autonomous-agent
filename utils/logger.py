import json
from pathlib import Path
from datetime import datetime
from models.schemas import ThreatEvent, ThreatScoreResult, DecisionResult, ResponseExecutionResult


LOG_FILE = Path("agent_actions.log")


def log_agent_action(
    event: ThreatEvent,
    score_result: ThreatScoreResult,
    decision: DecisionResult,
    execution: ResponseExecutionResult
) -> None:
    log_entry = {
        "logged_at": datetime.utcnow().isoformat(),
        "event": event.model_dump(mode="json"),
        "threat_score": score_result.model_dump(),
        "decision": decision.model_dump(),
        "execution": execution.model_dump(mode="json"),
    }

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
