from dataclasses import dataclass

BLOCKED_KEYWORDS = [
    "suicide", "kill myself", "self harm",
    "porn", "sex with", "nude", "grooming",
]

@dataclass
class ShieldResult:
    allowed: bool
    flags: list
    safe_prompt: str
    message_to_user: str | None = None

def run_youth_shield(prompt: str, likely_minor=True) -> ShieldResult:
    flags = []
    lower = prompt.lower()

    for kw in BLOCKED_KEYWORDS:
        if kw in lower:
            flags.append(f"blocked_keyword:{kw}")

    if likely_minor and flags:
        return ShieldResult(
            allowed=False,
            flags=flags,
            safe_prompt="",
            message_to_user="This topic is unsafe for children. Please speak to a trusted adult.",
        )

    return ShieldResult(True, flags, prompt)
