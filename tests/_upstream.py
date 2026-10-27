"""Personalized repository detection helper."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def is_upstream_checkout() -> bool:
    """Whether this checkout is an unconfigured template."""
    return False
