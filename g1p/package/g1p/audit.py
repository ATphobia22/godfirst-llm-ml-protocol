"""
Audit logging and redemptive error handling.
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class AuditRecord:
    timestamp: float
    prompt: str
    response: Optional[str]
    filters: Dict[str, Any]
    safety: Dict[str, Any]
    governance: Dict[str, Any]
    error: Optional[str] = None


class AuditLogger:
    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        storage = self.config.get("storage", {})
        self.enabled = self.config.get("enabled", True)
        self.path = storage.get("path", "g1p_audit.log")

    def log(self, record: AuditRecord) -> None:
        if not self.enabled:
            return
        line = json.dumps(asdict(record), ensure_ascii=False)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def redemptive_error_record(self, prompt: str, error: Exception) -> AuditRecord:
        return AuditRecord(
            timestamp=time.time(),
            prompt=prompt,
            response=None,
            filters={},
            safety={},
            governance={},
            error=str(error),
        )
