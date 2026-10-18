---
name: panel-to-prototype
description: Turn product evidence and simulated customer-role reviews into prioritized workflow experiments, review canvases, and working frontend prototypes. Use for persona panels, product stress tests, professional-workspace exploration, or further panel-to-prototype rounds. Simulations generate hypotheses; they do not replace customer research.
metadata:
  version: "1.0.0"
---

# Panel to Prototype

Help the user connect **customer job → friction → proposed intervention → working behavior → next real-world test**. A larger panel or feature list is not itself progress.

## Establish the round

Inspect the provided product, prior findings and existing implementation before proposing additions. Preserve the user's chosen scope: panel only, prototype only using existing research, full round, or an iteration. Do not build when they ask only for findings; do not stop at recommendations when they authorize a prototype.

Identify the decision this round should help make, the relevant customer roles, available evidence and constraints. Infer routine choices from context; ask only for missing information that materially changes the work. With enough context, proceed with stated assumptions.

Keep a compact evidence ledger distinguishing:
- **Observed:** directly inspected behavior, with location and conditions.
- **Reported:** something the user or a supplied source says; preserve attribution.
- **Context:** sourced occupational/category practice; not demand for this product.
- **Hypothesis:** simulated role judgment, inferred need or proposed value.
- **Prototype result:** behavior demonstrated in the local model; not production capability.

Record unknowns explicitly. “Not inspected” does not mean “missing.” Avoid carrying old evidence forward as current without qualification. Read [references/panel-method.md](references/panel-method.md) for panel composition, critique prompts and source handling.

## Run a useful simulated panel

Select roles because they perform, buy, receive or constrain the work. Distinguish operators, economic buyers, recipients/referrers, affected participants and boundary reviewers. One person may occupy several relationships; these are not automatically separate market segments.

Give each role a concrete job, trigger, existing workaround, incentive, scope of responsibility, rejection condition and disconfirming question. Review the actual flows and fictional scenarios, not just feature names. Preserve disagreements and cases where an export, email, existing vendor or simpler view could suffice.

Label all simulated statements as hypotheses, not interviews, testimonials or measured buying intent. Shared-context agents are not independent corroboration. Describe the perspectives represented and the evaluation actually performed without inflating counts. Do not invent professional credentials or imply a real named person participated.

Parallel agents are optional. Use them only if available and authorized by the host or user; give bounded critique tasks, not implementation ownership over the same files. A single-agent pass may adopt multiple lenses but must not claim independent review.

## Choose interventions

Synthesize customer needs before naming screens. For each candidate, specify:
- Who benefits and what concrete work becomes easier.
- The trigger, input records, output and human decision.
- Necessary data/capability assumptions and material failure cases.
- How it differs from existing flows and what evidence could disconfirm its value.

Choose among **prototype, extend, defer, reject** and explain tradeoffs. These are recommended directions, not proof of implementation or authorization to build; record actual implementation separately. Favor distinct jobs with demonstrable behavior over reworded summaries. Do not invent a precise fit percentage or ROI score from simulated opinions.

If the user explicitly requests a number of additions, implement that scope when feasible. Prerequisites may be modeled transparently with fictional data. Do not repeatedly expand the panel or wait for real interviews as a condition of building an authorized theoretical prototype. Preserve blockers as test questions and state simulation boundaries.

For “a couple more,” inspect prior rounds first. Add perspectives only when they reveal a different job, handoff, responsibility or counterexample. Explain whether the increment is a new flow or an extension. Read [references/iteration.md](references/iteration.md).

## Build the chosen behavior

When implementation is authorized, read [references/prototype-method.md](references/prototype-method.md). Reuse the actual project and design foundations where available: tokens, typography, spacing, components and terminology. Match the requested fidelity without claiming copied production behavior that was not inspected.

Implement useful end-to-end state transitions, rather than attractive dead ends. Keep fixture records internally consistent. Derive counts and status from records. If AI is part of the concept, use a believable, explicitly labeled simulation with inspectable inputs, reasons, limitations and a human review path. The simulation must never claim to have inspected a file, verified identity or performed an external action that did not occur.

Source freshness is part of behavior: edits to the relevant records, membership, audience, reference metadata, baseline or plan/report version must invalidate dependent output. Keep historical output distinguishable from current output. Saving a draft is separate from sending, acceptance and real-world completion.

Default to a buildless local HTML/CSS/JS artifact for a new local-only concept when no existing stack dictates otherwise. Honor the user's hosting choice and the host's tools/skills. This skill alone authorizes no deployment, real contact, purchase, upload or production mutation.

## Record and verify

Scale artifacts to the task. Usually retain findings, selected/deferred decisions, implementation entry points and verification limits; preserve earlier rounds without silently rewriting their conclusions.

When a structured record or review canvas is useful, use [assets/round-record.example.json](assets/round-record.example.json) as a concrete starting shape. It is entirely fictional. `assets/round-record.schema.json` documents the format. Generate a standalone, offline canvas with:

```sh
python3 <skill-folder>/scripts/render_panel.py <round.json> --out <panel.html>
```

The helper checks structure and cross-references, not whether the claims are true. Its neutral canvas is a research artifact, not a replacement for the product's design system. Use an available equivalent if Python is unavailable.

Verify meaningful behavior: source linkage, unknown/conflicting data, scope isolation, controlled updates, dependent freshness, persistence and the main user journey. Run appropriate syntax/tests and browser checks using available supported tools. Report unavailable checks; do not fabricate a visual review. Do not install a browser/toolchain solely to satisfy this skill when the host does not support it.

Finish with working local paths/URLs or the requested research result, the central tradeoff, what was verified and the next real-customer question. Clearly separate simulated panel conclusions from observed evidence. Do not imply the skill ran interviews, proved demand or established product-market fit.
