# Implementation details

## Manifest

- Located at `manifest.json`.
- Validated by `g1p/manifest_schema.py`.
- Controls:
  - Safety configuration
  - Audit configuration
  - Filter pipeline
  - Governance rules
  - API expectations

## Safety

- Implemented in `g1p/safety.py`.
- Uses simple keyword heuristics as placeholders.
- Designed to be replaced or extended with:
  - Classifiers
  - Policy engines
  - External moderation APIs

## Governance

- Implemented in `g1p/governance.py`.
- Rules are defined in the manifest.
- Each rule has:
  - `id`
  - `description`
  - `applies_to` (e.g., `["output"]`, `["session"]`)
  - `action` (e.g., `allow`, `block_and_warn`, `enforce_strict_safety`)

## Audit

- Implemented in `g1p/audit.py`.
- Writes JSON lines to a file.
- Captures:
  - Prompt
  - Response
  - Filter notes
  - Safety decisions
  - Governance decisions
  - Errors (if any)
