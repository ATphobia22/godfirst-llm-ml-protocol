from dataclasses import dataclass

DISCLAIMER = (
    "\n\n[GodFirst Truth Guard] This answer may contain uncertainty."
)

@dataclass
class GuardResult:
    output: str
    flags: list

def apply_truth_guard(model_output: str, speculative=True) -> GuardResult:
    flags = []
    text = model_output

    if speculative:
        text += DISCLAIMER
        flags.append("speculation_disclaimer")

    return GuardResult(text, flags)
