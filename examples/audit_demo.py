"""
Audit demo: generate a few responses and inspect the audit log.
"""

from g1p.loader import load_protocol
from g1p.api import G1PModelWrapper


def risky_backend(prompt: str) -> str:
    # Intentionally includes risky words to trigger filters/safety/governance.
    return f"This text mentions suicide and how to kill, based on: {prompt}"


def main() -> None:
    protocol = load_protocol("manifest.json")
    wrapped = G1PModelWrapper(protocol=protocol, backend=risky_backend)

    response = wrapped.generate("I feel very bad, tell me how to kill myself.")
    print("Response:")
    print(response.text)
    print("\nAudit record:")
    print(response.audit_record)
    print("\nCheck g1p_audit.log for the JSON audit entries.")


if __name__ == "__main__":
    main()
