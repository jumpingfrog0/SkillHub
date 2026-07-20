---
name: discuss-design-decisions
description: Break a complex technical or architectural proposal into ordered, atomic decisions and discuss them with the user one at a time until each relevant tradeoff is confirmed, deferred, or rejected. Use when the user asks to discuss issues step by step or one by one, when a design review contains several coupled choices, when evaluating possible overengineering, or when implementation must wait for explicit decisions about behavior, ownership, dependencies, naming, lifecycle, or compatibility. Do not use for a single straightforward question, an already-approved implementation, or as a replacement for a stricter formal workflow.
---

# Discuss Design Decisions

Guide a focused design conversation that produces explicit decisions without overwhelming the user.

## Establish the decision map

1. Inspect the available proposal, code, constraints, and prior decisions before recommending changes.
2. Separate facts about the current system from design choices.
3. Split the unresolved design into atomic decision points. Do not turn routine implementation details into user decisions.
4. Order the decisions by dependency so that later discussions can rely on earlier conclusions.
5. Present only the short ordered list first. Do not include the full solution unless the user asks for it.
6. Track each item internally as `pending`, `confirmed`, `deferred`, or `rejected`.

## Discuss one decision at a time

For the current item:

1. State the exact question and its boundary.
2. Give only the context needed to decide it.
3. Compare the viable options and their concrete consequences.
4. Recommend one option and explain why. Do not offload technical judgment to the user.
5. Identify any behavior, compatibility, lifecycle, ownership, or API-semantic change that requires explicit confirmation.
6. Ask for confirmation before moving to the next dependent decision.

Keep each round compact. Do not preview detailed solutions for later items.

## Process user feedback

- Evaluate objections against current evidence; agree or disagree with reasons instead of conceding automatically.
- Record confirmed wording accurately and treat it as a constraint in later rounds.
- Add newly discovered decisions to the map and place them according to dependencies.
- Reopen a confirmed decision only when new evidence conflicts with it; explain the conflict first.
- Mark an item `deferred` when the user sets it aside, and avoid resolving or implementing it implicitly.
- When the user says to continue, advance to the next pending item without repeating the full history.

## Control implementation

- Do not modify code merely because a design is being discussed.
- Start implementation only when the user requests it and every decision required for that implementation scope is confirmed.
- If the user requests partial implementation, implement only confirmed items and preserve deferred behavior unchanged.
- Stop and surface any newly discovered choice that would alter visible behavior, state retention, API semantics, compatibility, or another confirmed boundary.
- After implementation, distinguish completed work from remaining deferred decisions.

## Summarize precisely

Summarize only when requested or when the decision phase is complete.

- Include confirmed conclusions and relevant constraints.
- List deferred or unresolved items separately.
- Exclude already implemented or previously summarized material when the user requests only the latest decision.
- Prefer a concise decision ledger over replaying the conversation.

## Avoid these failure modes

- Dumping every issue, recommendation, and code example into the first response.
- Discussing multiple independent decisions in one round.
- Treating a convenience abstraction as necessary without current evidence.
- Asking the user to choose between options without making a recommendation.
- Repeating all confirmed conclusions before every new question.
- Allowing a deferred decision to leak into implementation through an unstated assumption.
- Replacing an applicable project or formal workflow; use this skill only as its discussion protocol.
