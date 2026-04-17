from datetime import datetime


class Agent:

    def __init__(self):
        self.memory = []
        self.goals = []

    def add_goal(self, goal: str):
        self.goals.append(goal)

    def think(self):
        if not self.goals:
            return None

        current_goal = self.goals[0]

        thought = f"Analyzing goal: {current_goal}"

        return {
            "goal": current_goal,
            "thought": thought,
            "timestamp": datetime.utcnow().isoformat()
        }

    def decide(self, thought):
        goal = thought["goal"]

        if "scan" in goal:
            return {"action": "scan_system"}

        if "block" in goal:
            return {"action": "block_ip"}

        return {"action": "monitor"}

    def act(self, action):
        if action["action"] == "scan_system":
            result = "Scanning system for threats..."

        elif action["action"] == "block_ip":
            result = "Blocking suspicious IP..."

        else:
            result = "Monitoring system..."

        return {
            "action": action["action"],
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }

    def reflect(self, result):
        self.memory.append(result)

        return {
            "status": "reflection_saved",
            "memory_size": len(self.memory)
        }

    def run(self):
        thought = self.think()
        if not thought:
            return {"status": "no_goals"}

        action = self.decide(thought)
        result = self.act(action)
        reflection = self.reflect(result)

        return {
            "thought": thought,
            "action": action,
            "result": result,
            "reflection": reflection
        }

