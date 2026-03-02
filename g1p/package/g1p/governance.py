"""
Governance rule engine.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class GovernanceDecision:
    allowed: bool
    action: str
    reason: str


class GovernanceEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.rules: List[Dict[str, Any]] = self.config.get("rules", [])

    def evaluate_output(self, text: str, context: Dict[str, Any]) -> GovernanceDecision:
        lowered = text.lower()
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            action = rule.get("action", "allow")
            applies_to = rule.get("applies_to", [])

            if "output" not in applies_to:
                continue

            if rid == "no_harm_instructions":
                if "how to kill" in lowered or "suicide" in lowered:
                    return GovernanceDecision(
                        allowed=False,
                        action=action,
                        reason=rid,
                    )

            if rid == "no_sexual_content_with_minors":
                if "child" in lowered and "sexual" in lowered:
                    return GovernanceDecision(
                        allowed=False,
                        action=action,
                        reason=rid,
                    )

        return GovernanceDecision(allowed=True, action="allow", reason="no_rule_triggered")

    def evaluate_session(self, context: Dict[str, Any]) -> GovernanceDecision:
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            action = rule.get("action", "allow")
            applies_to = rule.get("applies_to", [])

            if "session" not in applies_to:
                continue

            if rid == "youth_default_to_safe":
                user_age = context.get("user_age")
                if user_age is None or user_age < 18:
                    return GovernanceDecision(
                        allowed=True,
                        action=action,
                        reason=rid,
                    )

        return GovernanceDecision(allowed=True, action="allow", reason="no_session_rule_triggered")
