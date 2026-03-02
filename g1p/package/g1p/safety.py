"""
Safety layer: youth shield and truth guard.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SafetyDecision:
    allowed: bool
    reason: str
    transformed_text: str


class SafetyEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.youth_shield_cfg = self.config.get("youth_shield", {})
        self.truth_guard_cfg = self.config.get("truth_guard", {})

    def apply_youth_shield(self, text: str, context: Dict[str, Any]) -> SafetyDecision:
        if not self.youth_shield_cfg.get("enabled", True):
            return SafetyDecision(True, "youth_shield_disabled", text)

        # Very simple heuristic placeholder
        blocked_keywords = ["sexual", "porn", "gore"]
        lowered = text.lower()
        if any(k in lowered for k in blocked_keywords):
            return SafetyDecision(
                allowed=False,
                reason="youth_shield_blocked_content",
                transformed_text="This content is not appropriate for children.",
            )

        return SafetyDecision(True, "youth_shield_pass", text)

    def apply_truth_guard(self, text: str, context: Dict[str, Any]) -> SafetyDecision:
        if not self.truth_guard_cfg.get("enabled", True):
            return SafetyDecision(True, "truth_guard_disabled", text)

        # Placeholder: in a real system, this would call classifiers / fact-checkers.
        disallowed_categories = set(
            self.truth_guard_cfg.get("disallowed_categories", [])
        )
        # We only simulate detection via simple keyword checks for now.
        lowered = text.lower()
        if "how to kill" in lowered or "suicide" in lowered:
            if "self-harm_instructions" in disallowed_categories:
                return SafetyDecision(
                    allowed=False,
                    reason="truth_guard_self_harm_block",
                    transformed_text=(
                        "I cannot provide guidance on self-harm or harm to others. "
                        "Please seek help from trusted people or professionals."
                    ),
                )

        return SafetyDecision(True, "truth_guard_pass", text)

    def apply_all(self, text: str, context: Dict[str, Any]) -> SafetyDecision:
        decision = self.apply_youth_shield(text, context)
        if not decision.allowed:
            return decision

        decision = self.apply_truth_guard(decision.transformed_text, context)
        return decision
