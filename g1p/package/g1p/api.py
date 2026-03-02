"""
Public API: wrap any LLM/ML backend with G1P.
"""

from dataclasses import dataclass
from typing import Callable, Any, Dict

from .safety import SafetyEngine
from .filters import FilterPipeline
from .governance import GovernanceEngine
from .audit import AuditLogger, AuditRecord
from .config import G1PConfig


@dataclass
class G1PResponse:
    text: str
    audit_record: AuditRecord


class G1PModelWrapper:
    def __init__(self, protocol: Dict[str, Any], backend: Callable[[str], str]):
        self.protocol = protocol
        self.backend = backend

        safety_cfg = protocol.get("safety", {})
        filters_cfg = protocol.get("filters", {})
        governance_cfg = protocol.get("governance", {})
        audit_cfg = protocol.get("audit", {})

        self.config = G1PConfig(
            version=protocol.get("version", "unknown"),
            youth_shield_enabled=safety_cfg.get("youth_shield", {}).get("enabled", True),
            truth_guard_enabled=safety_cfg.get("truth_guard", {}).get("enabled", True),
            audit_enabled=audit_cfg.get("enabled", True),
            audit_log_path=audit_cfg.get("storage", {}).get("path", "g1p_audit.log"),
        )

        self.safety_engine = SafetyEngine(safety_cfg)
        self.filter_pipeline = FilterPipeline(filters_cfg)
        self.governance_engine = GovernanceEngine(governance_cfg)
        self.audit_logger = AuditLogger(audit_cfg)

    def generate(self, prompt: str, context: Dict[str, Any] | None = None) -> G1PResponse:
        context = context or {}
        try:
            # Session-level governance
            session_decision = self.governance_engine.evaluate_session(context)
            if session_decision.action == "enforce_strict_safety":
                context["youth_mode"] = "strict"

            # Call backend
            raw_output = self.backend(prompt)

            # Filters
            filter_result = self.filter_pipeline.run(raw_output)

            # Safety
            safety_decision = self.safety_engine.apply_all(filter_result.text, context)

            if not safety_decision.allowed:
                final_text = safety_decision.transformed_text
                governance_decision = self.governance_engine.evaluate_output(final_text, context)
            else:
                # Governance on output
                governance_decision = self.governance_engine.evaluate_output(
                    safety_decision.transformed_text, context
                )
                if not governance_decision.allowed and governance_decision.action == "block_and_warn":
                    final_text = (
                        "This response has been blocked by governance rules to prevent harm or exploitation."
                    )
                else:
                    final_text = safety_decision.transformed_text

            audit_record = AuditRecord(
                timestamp=__import__("time").time(),
                prompt=prompt,
                response=final_text,
                filters={"risk_level": filter_result.risk_level, "notes": filter_result.notes},
                safety={"decision": safety_decision.reason},
                governance={
                    "session": session_decision.reason,
                    "output": governance_decision.reason,
                },
            )
            self.audit_logger.log(audit_record)
            return G1PResponse(text=final_text, audit_record=audit_record)

        except Exception as e:  # noqa: BLE001
            error_record = self.audit_logger.redemptive_error_record(prompt, e)
            self.audit_logger.log(error_record)
            # Redemptive error message
            return G1PResponse(
                text=(
                    "An internal error occurred while applying the GodFirst Protocol. "
                    "The event has been logged for correction and learning."
                ),
                audit_record=error_record,
            )
