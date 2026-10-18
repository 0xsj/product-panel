# From a customer job to a working prototype

## Inspect and preserve the baseline

Locate the existing app, source assets, routes, fixture records and previous round
artifacts. Respect repository instructions and the user's stack. Record the observed
design foundations instead of recreating an approximate brand from memory. Avoid
bundling proprietary logos, screenshots or private business context into a reusable
skill distribution; project prototypes can use authorized project materials.

Use the smallest change that demonstrates the selected job. A new task may belong
inside an existing handover, request or client view rather than another global
navigation item or AI mode. Keep product-facing language about the user's task.

## Specify the transaction

Before building, identify:
- Trigger and actor; selected household/account/project and objects.
- Inputs and missing values; where each field originates.
- Output and intended recipient/audience.
- State transition and which human decides it.
- Actions the concept actually performs versus simulates.
- Undo/correction or retained history appropriate to the change.

Use separate records for concepts that carry different meaning. Examples:
- Request draft, external delivery and attributed reply.
- Reported answer, coordinator assessment and professional verification.
- Planned recipient, ownership assertion and physical collection.
- Inventory reference metadata and inspected document contents.
- Planning manifest, booking, provider report and receiving confirmation.

Do not interpret silence as agreement, an allocation as pickup, a filename as
verified evidence, or a reviewed discrepancy as a confirmed event.

## Make AI assistance believable and bounded

A deterministic local simulation is often enough. It should use actual fixture
inputs to produce specific, reproducible suggestions: missing-field questions,
record comparisons, categories, scoped briefs or discrepancy lists.

Expose source fields, uncertainty, exclusions and the decision needed from the
operator. An editable summary alone is not a complete workflow if the customer job
requires responses, corrections or follow-through. Avoid cosmetic confidence scores
and unnecessary theatrical processing. Label simulation at the point of use.

Keep fictional replies and reports explicitly attributed as samples. Do not claim
real participant identity, delivery/read receipts, file inspection, model inference
or external actions. Do not automatically write free-text assertions into sensitive
fields. A whitelisted per-field review can show current value, source, proposed
value and an explicit acceptance decision. Preserve “unknown” and conflicting
accounts without silently selecting the latest.

## Scope and freshness invariants

Validate object references against the intended account/project at generation and
again before mutation. If a reference links multiple objects, every linked object
must pass the disclosure scope before appearing in an audience packet.

Fingerprint the inputs each output actually depends on. Depending on the workflow,
include field values, scope membership, audience/disclosure, reference metadata,
comparison baseline, plan version, report revision and withdrawal state. An accepted
edit can invalidate another suggestion from the same run; advancing a run-level
fingerprint alone is insufficient.

Store immutable source snapshots/fingerprints with drafts. Mark stale output as
historical and require a fresh comparison before applying it. Editing old prose
must not silently revalidate changed sources. Older output lacking trustworthy
fingerprints should remain distinguishable as historical.

A comparison fingerprint should contain its inputs, not its own generated results
or review history; otherwise saving the output invalidates itself or recursively
grows storage. Reports retain their original plan/version association when a new
plan is captured. A source revision should not overwrite the older raw statement.

These are prototype behavior patterns, not proof of production security or compliance.

## Test the actual decisions

Use fictional fixtures with deliberate conflicts and missing values. Cover:
- Empty/unknown fields and an “I don't know” answer.
- Scope change, added/removed object and foreign-account references.
- Internal notes and restricted references excluded from outward drafts.
- A manual edit after a request; a dependent suggestion made obsolete by acceptance.
- Conflicting reports; partial/unidentified objects; withdrawn report or new plan.
- Persistence/reload, disabled stale controls and a guarded submit handler.

Verify that generation leaves sources unchanged and only an explicit permitted
transaction alters them. Derive counts from records. Test runtime behavior beyond
screenshots; visually inspect the actual rendered layout when supported. State
which checks were not possible, such as missing second-role access or broken
capture. Never claim a security, accessibility or compliance audit from a frontend
walkthrough alone.

Local HTML/CSS/JS output should work with a simple static server when requested,
with clear entry points, fictional seed data and an appropriate reset path. Preserve
existing user edits while testing; reset only disposable QA data within authorization.
