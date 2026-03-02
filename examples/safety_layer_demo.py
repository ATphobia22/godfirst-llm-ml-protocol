"""
Safety layer demo: show youth shield behavior.
"""

from g1p.loader import load_protocol
from g1p.api import G1PModelWrapper


def backend(prompt: str) -> str:
    return f"This is a sexual story for adults only. Prompt: {prompt}"


def main() -> None:
    protocol = load_protocol("manifest.json")
    wrapped = G1PModelWrapper(protocol=protocol, backend=backend)

    # Simulate a child user
    context = {"user_age": 12}
    response = wrapped.generate("Tell me a spicy story.", context=context)

    print("Response (youth context):")
    print(response.text)
    print("\nAudit record:")
    print(response.audit_record)


if __name__ == "__main__":
    main()
