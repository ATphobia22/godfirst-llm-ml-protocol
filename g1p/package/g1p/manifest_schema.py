"""
Minimal schema validation helpers for the G1P manifest.
"""

from typing import Any, Dict


REQUIRED_TOP_LEVEL_KEYS = [
    "protocol_name",
    "protocol_short_name",
    "version",
    "safety",
    "audit",
    "filters",
    "governance",
    "api",
]


class ManifestValidationError(Exception):
    """Raised when the manifest is invalid."""


def validate_manifest(manifest: Dict[str, Any]) -> None:
    """Basic structural validation of the manifest."""
    missing = [k for k in REQUIRED_TOP_LEVEL_KEYS if k not in manifest]
    if missing:
        raise ManifestValidationError(f"Missing required manifest keys: {missing}")

    if not isinstance(manifest["safety"], dict):
        raise ManifestValidationError("safety must be an object")

    if not isinstance(manifest["audit"], dict):
        raise ManifestValidationError("audit must be an object")

    if not isinstance(manifest["filters"], dict):
        raise ManifestValidationError("filters must be an object")

    if not isinstance(manifest["governance"], dict):
        raise ManifestValidationError("governance must be an object")

    if not isinstance(manifest["api"], dict):
        raise ManifestValidationError("api must be an object")
