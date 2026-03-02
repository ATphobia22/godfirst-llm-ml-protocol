"""
Simple inference example using G1P with a dummy backend.
"""

from g1p.loader import load_protocol
from g1p.api import G1PModelWrapper


def dummy_backend(prompt: str) -> str:
    return f"This is a friendly story about kindness. Prompt was: {prompt}"


def main() -> None:
    protocol = load_protocol("manifest.json")
    wrapped = G1PModelWrapper(protocol=protocol, backend=dummy_backend)

    response = wrapped.generate("Tell a story for a 9-year-old about forgiveness.")
    print("Response:")
    print(response.text)
    print("\nAudit record:")
    print(response.audit_record)


if __name__ == "__main__":
    main()
