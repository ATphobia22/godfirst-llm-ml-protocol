"""
Manifest loader and protocol bootstrap.
"""

import json
from typing import Dict, Any

from .manifest_schema import validate_manifest, ManifestValidationError


def load_protocol(path: str) -> Dict[str, Any]:
    """Load and validate a G1P manifest from disk."""
    with open(path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    validate_manifest(manifest)
    return manifest


__all__ = ["load_protocol", "ManifestValidationError"]
