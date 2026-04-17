from collections import defaultdict
from datetime import datetime

# In-memory store (later we can swap to Redis)
ATTACKER_DB = defaultdict(lambda: {
    "events": [],
    "total_requests": 0,
    "last_seen": None,
    "threat_count": 0
})


def update_attacker(ip: str, score: int):
    record = ATTACKER_DB[ip]

    record["events"].append({
        "score": score,
        "timestamp": datetime.utcnow().isoformat()
    })

    record["total_requests"] += 1
    record["last_seen"] = datetime.utcnow().isoformat()

    if score >= 65:
        record["threat_count"] += 1

    return record


def get_attacker_profile(ip: str):
    return ATTACKER_DB[ip]
