"""
Discernment filters: classification and sanitisation pipeline.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FilterResult:
    text: str
    risk_level: str
    notes: Dict[str, Any]


class FilterPipeline:
    def __init__(self, pipeline_config: Dict[str, Any]):
        self.pipeline_config = pipeline_config or {}
        self.steps = self.pipeline_config.get("pipeline", [])

    def classify_risk(self, text: str) -> FilterResult:
        lowered = text.lower()
        if any(k in lowered for k in ["kill", "suicide", "bomb"]):
            risk = "high"
        elif any(k in lowered for k in ["angry", "hate"]):
            risk = "medium"
        else:
            risk = "low"
        return FilterResult(text=text, risk_level=risk, notes={"step": "classify_risk"})

    def sanitise_output(self, text: str) -> FilterResult:
        # Placeholder: could strip PII, profanity, etc.
        return FilterResult(text=text, risk_level="post_sanitise", notes={"step": "sanitise_output"})

    def run(self, text: str) -> FilterResult:
        current = FilterResult(text=text, risk_level="unknown", notes={})
        for step in self.steps:
            if step == "classify_risk":
                current = self.classify_risk(current.text)
            elif step == "sanitise_output":
                current = self.sanitise_output(current.text)
            # youth_shield and truth_guard are handled in SafetyEngine, not here.
        return current
