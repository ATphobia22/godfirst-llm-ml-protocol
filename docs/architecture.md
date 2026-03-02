# Architecture

## Layers

1. **Backend Model**
   - Any LLM/ML system (local, cloud, API).
   - Exposed as a simple function: `Callable[[str], str]`.

2. **G1P API Wrapper**
   - `G1PModelWrapper` orchestrates:
     - Filters
     - Safety
     - Governance
     - Audit

3. **Filters**
   - `FilterPipeline` classifies risk and sanitises output.

4. **Safety**
   - `SafetyEngine` applies:
     - Youth Shield
     - Truth Guard

5. **Governance**
   - `GovernanceEngine` enforces rules from the manifest.

6. **Audit**
   - `AuditLogger` writes structured JSON lines to a log file.
   - Errors are captured as **redemptive error records**.

## Data flow

1. User prompt → `G1PModelWrapper.generate(prompt, context)`
2. Session governance → may enforce strict safety.
3. Backend model → raw output.
4. Filters → risk classification and sanitisation.
5. Safety → youth shield and truth guard.
6. Governance → final allow/block decision.
7. Audit → full record written to log.
8. Response → safe text + audit record returned to caller.
