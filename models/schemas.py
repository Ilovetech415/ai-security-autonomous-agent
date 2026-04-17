from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class ThreatEvent(BaseModel):
    source_ip: str
    event_type: str = Field(..., description="e.g. brute_force, port_scan, suspicious_login, malware_activity")
    failed_attempts: int = 0
    request_count: int = 0
    endpoint: Optional[str] = None
    geo_anomaly: bool = False
    off_hours: bool = False
    known_bad_actor: bool = False
    payload_signature_match: bool = False
    notes: Optional[str] = None
    timestamp: datetime


class ThreatScoreResult(BaseModel):
    score: int
    severity: Literal["low", "medium", "high", "critical"]
    factors: List[str]


class DecisionResult(BaseModel):
    action: Literal["monitor", "rate_limit", "block"]
    reason: str
    cooldown_minutes: int


class ResponseExecutionResult(BaseModel):
    status: str
    action_taken: str
    source_ip: str
    details: str
    executed_at: datetime


class AgentResponse(BaseModel):
    event: ThreatEvent
    threat_score: ThreatScoreResult
    decision: DecisionResult
    execution: ResponseExecutionResult
