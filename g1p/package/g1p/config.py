from dataclasses import dataclass
from typing import Optional


@dataclass
class G1PConfig:
    """In-memory representation of key protocol settings."""

    version: str
    youth_shield_enabled: bool = True
    truth_guard_enabled: bool = True
    audit_enabled: bool = True
    audit_log_path: str = "g1p_audit.log"
    default_youth_mode: str = "strict"
    manifest_path: Optional[str] = None
