---
name: ios-to-android-feature-migration
description: Use when migrating a completed iOS feature from drama-ios to famo-android, based on feature-discovery final business and technical documents. Requires writing an Android migration plan first and waiting for user confirmation before modifying Android code.
---

# iOS to Android Feature Migration

Use this skill to migrate an already completed iOS feature from `drama-ios` to `famo-android`. This skill consumes the final documents produced by `feature-discovery`; it does not replace feature discovery.

## Scope

This skill owns:

- Reading the iOS feature-discovery final business and technical documents.
- Checking critical iOS code evidence only to validate migration-critical facts.
- Mapping iOS behavior and implementation facts to Android modules, interfaces, resources, storage, network, analytics, and verification.
- Writing an Android migration plan before any Android code change.
- Implementing Android changes only after the user confirms the written plan.
- Producing implementation and acceptance records after implementation.

This skill does not own:

- Full iOS feature exploration.
- Replacing or shortcutting `feature-discovery`.
- Modifying Android code before a written migration plan is confirmed.
- Running Android build, install, SDK, emulator, or adb commands when the Android project constraints prohibit them.

## Required Inputs

Before starting a real migration, locate and read both final feature-discovery documents:

```text
.huangdonghong/docs/<feature-slug>/<feature-name>业务梳理.md
.huangdonghong/docs/<feature-slug>/<feature-name>技术实现梳理.md
```

If either document is missing, stop the migration workflow and instruct the user to run `feature-discovery` for the iOS feature first. Do not infer the migration plan directly from iOS code when the final documents are absent.

The feature-discovery documents are the primary source of truth. iOS code inspection is mandatory only as targeted evidence checking for migration-critical facts, not as a full rediscovery pass.

## Repository Rules

Before writing a migration plan or editing Android code:

- Read and follow the current Android repository constraints, including `AGENTS.md`.
- Locate the iOS repository at `../drama-ios` relative to `famo-android`. If that path does not exist, stop and ask the user for the iOS repository path.
- If the iOS repository has its own local instructions, read and follow them for iOS evidence inspection.
- Keep Android changes limited to files directly required by the confirmed migration plan.

## Output Directory

For a real migration, write all migration artifacts under:

```text
.huangdonghong/feature-migration/<feature-slug>/
```

The required artifact files are:

```text
Android迁移方案.md
Android迁移实施记录.md
Android迁移验收报告.md
```

`Android迁移方案.md` is a required coding gate. If it has not been written, Android production code must not be modified.

## Workflow

1. Read Android repository constraints and relevant project documentation.
2. Locate the iOS repository and read its applicable local constraints.
3. Locate and read the two final feature-discovery documents.
4. Read `references/ios-evidence-checklist.md`, then inspect only the iOS evidence needed to validate migration-critical facts.
5. Read `references/android-analysis-checklist.md`, then inspect Android code to identify the correct module, entry points, interfaces, resources, data flow, storage, analytics, and existing patterns.
6. Read `references/migration-plan-template.md`, then write `.huangdonghong/feature-migration/<feature-slug>/Android迁移方案.md`.
7. Report the plan path and wait for explicit user confirmation.
8. After confirmation, read `references/implementation-checklist.md` and implement the Android changes exactly within the confirmed scope.
9. Run only validation commands allowed by the Android project constraints.
10. Read `references/delivery-report-template.md`, then write `Android迁移实施记录.md` and `Android迁移验收报告.md`.

## Hard Gates

- Missing final business document: stop and request `feature-discovery`.
- Missing final technical document: stop and request `feature-discovery`.
- Missing Android migration plan file: do not edit Android production code.
- No explicit user confirmation of the migration plan: do not edit Android production code.
- Blocking open questions in the migration plan: do not edit Android production code until resolved.
- Conflict between feature-discovery documents and checked iOS code: record the conflict in the migration plan and stop if it affects implementation decisions.

## Evidence Rules

Use this source priority:

1. Final feature-discovery documents.
2. Targeted iOS code evidence.
3. Existing Android implementation patterns.
4. User-provided clarification.

Do not present guesses as confirmed facts. When evidence is missing, write it as missing evidence or a pending question. Configuration, experiments, feature flags, resources, strings, analytics, persistence, and fallback behavior must be explicitly checked or explicitly marked as not found.

## Reference Loading

Load references only when their workflow step is reached:

- `references/ios-evidence-checklist.md`: before targeted iOS evidence inspection.
- `references/android-analysis-checklist.md`: before Android implementation analysis.
- `references/migration-plan-template.md`: before writing `Android迁移方案.md`.
- `references/implementation-checklist.md`: after plan confirmation and before code edits.
- `references/delivery-report-template.md`: after implementation and before writing delivery records.
