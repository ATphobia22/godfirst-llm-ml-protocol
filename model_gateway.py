import os
from openai import OpenAI
from anthropic import Anthropic

from audit_logger import log_event
from youth_shield import run_youth_shield
from truth_guard import apply_truth_guard

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_model(prompt, model, user_id="anonymous", likely_minor=False):
    shield = run_youth_shield(prompt, likely_minor)
    if not shield.allowed:
        log_event("blocked_child_protection", prompt, "blocked", model, user_id, shield.flags)
        return shield.message_to_user

    safe_prompt = shield.safe_prompt

    try:
        if model == "gpt-4o-mini":
            resp = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": safe_prompt}],
            )
            raw = resp.choices[0].message.content
        else:
            msg = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                messages=[{"role": "user", "content": safe_prompt}],
            )
            raw = msg.content[0].text

        guarded = apply_truth_guard(raw)

        log_event("model_call", prompt, "success", model, user_id, shield.flags + guarded.flags)

        return guarded.output

    except Exception as e:
        log_event("model_call", prompt, "error", model, user_id, notes=str(e))
        return "An error occurred."
