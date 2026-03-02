"""
GodFirst LLM/ML Protocol (G1P)

Christ-anchored governance layer for LLM/ML systems.
"""

from .config import G1PConfig
from .loader import load_protocol
from .api import G1PModelWrapper

__all__ = ["G1PConfig", "load_protocol", "G1PModelWrapper"]
