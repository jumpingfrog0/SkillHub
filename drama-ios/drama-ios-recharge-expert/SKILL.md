---
name: drama-ios-recharge-expert
description: Use for drama-ios work involving recharge, wallet, insufficient balance, coins, IAP, StoreKit, Turnover, payment results, receipt reporting, credited-currency arrival, coupons, currency exchange, packages, H5 or RN payment, payment notifications, payment context, traceId, transaction token, or orderId. Load the personal recharge knowledge kernel directly, gather categorized read-only evidence, classify R0-R3 risk, and produce a compact change contract before implementation.
---

# Drama iOS Recharge Expert

Use the personal semantic kernel to keep recharge changes inside existing responsibility and lifecycle boundaries. Treat source evidence as current implementation fact and the kernel as reviewed constraints with explicit status.

## Authority and boundaries

- Read recharge knowledge directly from `.huangdonghong/agent-knowledge/recharge/` at the repository root.
- Treat that directory as the only personal authority for recharge knowledge.
- Do not route through or depend on `.huangdonghong/.agents/context` for recharge knowledge. Continue obeying repository-level instructions that independently require general project context.
- Do not copy business claims into this skill. Keep orchestration here and business facts in the authority directory.
- Treat static indexing as investigation support, never as a complete call graph or proof that no dynamic caller exists.

## Workflow

1. Locate the repository root with `git rev-parse --show-toplevel`.
2. Read `.huangdonghong/agent-knowledge/recharge/README.md` and `.huangdonghong/agent-knowledge/recharge/semantics.yaml` directly.
3. Read `architecture.md` for any R2/R3 task, cross-layer task, or task involving routing, payment result, receipt, arrival, UI/Flow lifecycle, notifications, context, trace/token/orderId, login, or logout.
4. Select only semantics relevant to the task:
   - Apply `confirmed` entries as implementation constraints.
   - Use `provisional` entries only to request more evidence.
   - Stop and request the owner's decision when a `disputed` entry is hit.
   - Ignore `retired` entries by default while preserving their tombstones.
   - For historical replay at a revision different from an entry's `last_verified_baseline`, treat the entry as a forward-reference investigation lead until its claim and evidence are revalidated at the replay revision. Do not import a later class, state owner, or route into an older baseline merely because the current kernel confirms it.
5. Start with direct exact source reads (`rg`, `git grep <rev>`, or known paths) and the requirement coverage ledger below. Run the read-only index only when a still-uncovered clause needs cross-file caller, event producer/consumer, Bridge parity, or path discovery evidence; it is opt-in, not a per-task prerequisite. Prefer one to three exact identifiers over broad words and disable co-change on the first pass:

   ```bash
   python3 .agents/skills/drama-ios-recharge-expert/scripts/source_index.py \
     --repo . --history-limit 0 --query <symbol-or-key> --query <event-or-path-token>
   ```

   Add `--rev <commit>` for historical replay. Do not use an implementation or later commit when evaluating a task at its pre-implementation baseline. If exact output is still broad, rerun one query at a time and consume only evidence tied to an uncovered clause. Enable bounded co-change or inspect name similarity only as a separately justified lead; never inject their full output by default.
6. When the index is used, separate its output into these evidence categories:
   - `exact_matches`: exact symbol, constant, key, or literal matches.
   - `event_evidence`: producer, consumer, or declaration evidence.
   - `historical_cochange`: paths changed in the same historical commits; use as a lead, not a dependency proof.
   - `name_similarity`: low-confidence investigation appendix only.
7. Follow exact matches into relevant control flow, data flow, state ownership, error paths, and cleanup paths. Record code facts, historical facts, inference, conflict, and unknowns separately.
8. Assign the highest applicable risk:
   - R0: documentation, comments, or pure Debug support disconnected from production entry points.
   - R1: leaf UI, formatting, or pure models without routing or payment-state changes.
   - R2: entry points, routing, configuration, analytics, Bridge, or cross-file context propagation.
   - R3: ordering, IAP/Web results, receipt reporting, arrival, idempotency, notification payloads, context lifecycle, logout isolation, or payment state.
9. Before editing, output the compact change contract below. For R3, request confirmation from the personal owner or payment owner. Stop for a disputed semantic, a source/kernel conflict, or a high-risk unknown that could alter user-visible payment behavior.
10. After editing, inspect the actual diff. Report responsibility-boundary violations, missed paths, invariant risks, and confirmed entries whose evidence or invalidation condition may now be stale.

## Pre-patch completeness pass

Before finalizing the change contract or a first-patch specification:

1. Build a requirement coverage ledger with one row per explicit task clause. Every row must contain: the exact condition or preservation rule, evidence query/path or justified external-contract unknown, current owner, candidate action, and a static validation. A candidate is incomplete while any row has only investigation notes but no action/validation. Cover eligibility (including positivity/range, not merely non-empty), excluded scope, configuration readiness, defaults and nil input, entry points, ordering, retry, cleanup, completion authority, and error states.
2. Fill the impact matrix even when a cell is unchanged: user type × legacy/new/black-user/wallet UI × Apple/Web/H5/RN channel × business type × result stage × retry/change-channel. Mark a cell `not applicable` or `unknown` with evidence instead of silently omitting it.
3. For a multi-entry feature, separately name every requested entry, every excluded entry, user-segment eligibility, configuration validity, completion signal, and whether counters/state are shared or per scene. Do not let an obvious UI host replace the eligibility or configuration-validity row.
4. Preserve the baseline's data carrier and owner unless an authoritative interface contract explicitly changes them. Product words such as “object” or “node” do not authorize inventing a generated SDK type, protobuf field, JSON key, or duplicate cache. When the baseline uses a serialized `expand`, prefer a guarded parser boundary until a new wire contract is evidenced.
5. For cleanup or handoff, prove this order: replacement input is valid → replacement context is saved → narrow obsolete state is cleared → external action starts. Enumerate every exact caller; an invalid URL/channel or rejected handoff must leave retry context intact.
6. Separate same-attempt retry from an explicit user change. A retry reuses the frozen attempt context; changing a channel, tier, or option revalidates only the fields whose applicability changed, while preserving trace and other transaction identity.
7. Inventory transaction identity field by field from the task, baseline carrier, and confirmed semantics. Explicitly preserve or intentionally replace every named field across start, retry, change-channel, result routing, and cleanup; never let “complete context” stand in for a missing identity field.
8. Complete the applicable result matrix explicitly: success, cancel, failure, timeout, unknown, risk-control, frozen/blocked, credited-currency arrival, and business-specific reward completion. For each nonterminal failure path, derive the primary user action from user capability, the original tier's available channels, and result semantics: retry, change payment, contact agent, or no safe action.
9. Cross-check task behavior against every relevant confirmed exception or branch/type matrix loaded from the authority. State why an exception applies or is out of scope.
10. When a disputed entry is hit, still provide the evidence and any safe local work, but do not generalize ownership or promise the disputed behavior. Mark the contract stopped and name the exact owner decision required.
11. For historical replay, if an exact protocol field or external schema is unavailable but target behavior is fixed, describe the safe owner/parser boundary and record the contract prerequisite. Do not stop or guess an identifier unless no safe candidate can be formed. A field or behavior explicitly named by the task is a requirement, not an unknown merely because its generated wire declaration is absent; only its unresolved wire identifier/shape may remain a prerequisite.
12. Audit every proposed stop before final output. `stopped=true` is valid only when (a) a disputed semantic or user-visible choice remains for the owner, or (b) no safe candidate action can be described before an external contract arrives. If `candidate_changes` already contains an adapter/parser seam, fail-closed wiring, UI extraction, or another reversible boundary action, missing field names, JSON keys, message values, limits, or defaults are prerequisites/unknowns with `stopped=false`, not blockers. Name the exact unresolved choice for every valid stop.
13. Give `disputed` precedence over the safe-local-work exception. When a task requirement intersects a relevant disputed entry at the replay baseline, the contract must remain `stopped=true` even if the candidate preserves current behavior, calls the policy “out of scope,” or provides useful local filtering/snapshot work. Record the semantic ID, evidence revalidation, safe local work, and exact owner decision; preserving current behavior prevents an unsafe patch but does not resolve the dispute.
14. Treat every selected benefit or option—coupon, package, product, reward, channel, promotion—as scoped data. Cross-check its applicability against every business type in the matrix, not only tier/channel. Freeze it only for the matching attempt; clear or reject it when entering an out-of-scope business type so an old selection cannot leak into another purchase.
15. Locate the authoritative domain owner before adding server-driven state. Extend the existing user-tag/domain-model chain that consumers already read; do not copy a new server label into `CoreData`, a login singleton, a view model, or another convenience cache unless that object is already the verified authority for the label. A parser/adapter seam belongs at the authoritative mapping boundary, and logout/account-switch semantics stay with that owner.
16. Separate lifecycle cardinalities explicitly. A user-scoped “first/only once” onboarding or auto-detail decision is not the same state as per-view exposure deduplication or per-scene display count. Re-entry/refresh behavior must use the existing policy owner or an external-contract prerequisite; a page-session boolean may deduplicate exposure but cannot silently redefine a user-scoped first-time rule.
17. Treat path-family words in the task as hard scope: legacy, new wallet, new popup, black-user, wallet, H5, and RN are not interchangeable examples. For every requested family, enumerate the exact baseline caller/handoff in the ledger and include it in `candidate_changes` and validation. A modern or similarly named path cannot substitute for an omitted legacy caller; extra families require separate evidence and must not displace the requested ones.
18. Close the baseline propagation graph for every value that must travel end to end. Enumerate all existing selection/producers for that value, every channel-specific start handoff, the attempt/context carrier, and every retry/change/result consumer. Do not declare a UI family “not applicable” merely because the first producer found belongs to another family; run a second exact search for the value's semantic model, selection state, and retry carrier, then either include each caller or cite concrete evidence that it cannot originate or be consumed there.
19. Resolve every product-role word such as “current popup,” “deprecated popup,” “wallet,” or “home entry” to an exact baseline runtime host before assigning inclusion or exclusion. Prove the mapping from live registration, construction, presentation, and ownership call sites; a class name, directory name, or superficial similarity is not evidence. Record a two-column requested-role → exact-class table and reject the contract if an included and excluded host may have been reversed.
20. A value producer may be a server model, preselected config, controller state, or an upstream handoff rather than a dedicated selection UI. For every task-requested family, trace reads as well as writes of the semantic value through its start method and carrier. The absence of the first producer shape found in another family cannot justify exclusion; only concrete control-flow evidence that the requested family cannot hold, receive, or forward the value may do so.
21. Run a final ledger-to-patch closure check after drafting the contract. Every requirement row and every requested path-family row must appear as an explicit `candidate_changes` action and an explicit validation, not merely as evidence, an impact-matrix cell, an invariant, or a review note. This includes each legacy or modern start entry and each business-type sink; one shared helper does not prove its callers were wired.
22. Model configuration-dependent behavior with at least three states when applicable: configuration absent/not ready, configuration present and allowing, and configuration present and forbidding. Derive the absent-state default from baseline behavior or an external contract; do not silently treat absence as denial, or denial as absence. Make the three-state rule visible in both the action and validation.
23. When the task names a server-designated event, reward, callback, field, or schema but the replay baseline does not expose its authoritative identifier, describe a contract-supplied matcher or adapter. Do not promote the closest existing message class, numeric type, JSON leaf, carrier, or handler into the unique contract merely because it is the best available integration lead.
24. For server-driven presentation models, make parser validity and lifecycle cardinality executable in the contract: validate runtime types, trim user-visible strings before non-empty checks, clear stale UI on invalid refresh, and place user-scoped suppression with the existing user policy so it survives page re-entry. Keep page-scoped exposure dedupe separate.

Keep index context bounded: use one to three exact symbols, constants, keys, or path tokens only for uncovered ledger rows. Follow exact/event evidence first. Run a second narrow query only when the first leaves a named clause uncovered; do not inject broad name-similarity or full co-change output into the working context.

## Compact change contract

```text
Goal:
Change scope:
Responsible layer to change:
Layers that must not change:
Affected legacy/new/black-user/wallet paths:
Affected Apple/Web/H5/RN paths:
Invariants to preserve:
Known risks:
Unknowns:
Conflicts:
Validation:
Risk: R0 | R1 | R2 | R3
Required confirmation:
```

Keep the contract in the task output or change description unless the user explicitly asks to persist it.

## Hard-fail checks

Reject or escalate a proposed change that could:

- duplicate ordering or credited-currency feedback;
- merge success, cancellation, failure, timeout, risk-control, or frozen-account outcomes;
- lose traceId, transaction token, orderId, or payment context;
- clear another transaction's context;
- bypass the established Component or Module boundary;
- break legacy/new/black-user/wallet routing;
- reverse the exact baseline hosts assigned to a requested current/deprecated or included/excluded product role;
- claim no caller or subscriber based on low-confidence or incomplete static search;
- silently prefer stale knowledge over current source evidence;
- choose a user-visible payment behavior without owner confirmation.

## Evidence output rules

- Cite a concrete path and symbol for important conclusions; include a commit for historical claims.
- Label inference and unknowns explicitly.
- Never promote `name_similarity` or historical co-change alone to confirmed fact or a blocking condition.
- When no evidence is found, state the searched revision, paths, and queries. Do not claim the object does not exist.
