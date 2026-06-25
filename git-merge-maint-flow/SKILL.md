---
name: git-merge-maint-flow
description: "Standard Git workflow for merging a feature branch into a maintenance or release branch: update the target branch, rebase the feature branch, merge with --no-ff, push the target branch, then sync the feature branch back to the target. Use when the user asks to merge a feature branch into a maint/release branch, run a rebase + no-ff merge flow, sync a feature branch after maint merge, or continue after manually resolving rebase/merge conflicts."
---

# Git Merge Maint Flow

## Overview

Use this skill to perform a conservative maintenance-branch merge flow that preserves a merge commit while keeping the feature branch rebased on the latest target branch. Treat the workflow as stateful: always inspect Git state before acting, and resume safely when a rebase or merge was interrupted by conflicts.

## Required Inputs

- `target_branch`: the maintenance/release branch to receive the feature branch, such as `drama-ios_2.22.0_maint`.
- `feature_branch`: the feature branch to merge, such as `feat/1001752_family_sign`.
- `remote`: default to `origin`, but confirm from the repository before pushing.

If the user only says to continue an interrupted flow, first infer the current step from `git status` and branch state. Ask for missing branch names only when they cannot be inferred safely.

## Safety Rules

- Start with `git status --short --branch` and do not proceed if unrelated user changes are present until the user confirms how to handle them.
- Do not run destructive commands such as `git reset --hard`, `git checkout -- <file>`, recursive deletion, or bulk deletion unless the user explicitly requests that exact operation.
- Do not push while a rebase, merge, or conflict resolution is unfinished.
- Before pushing, confirm the current branch is the target branch, no unresolved conflicts remain, and the recent commit graph matches the intended merge.
- Prefer explicit branch names in commands. Do not rely on aliases such as `gco`, `gl`, or `gp` inside the skill.
- Respect repository-specific instructions. In repositories that forbid builds or SDK queries during validation, use only static Git/status/log checks.

## Main Workflow

1. Inspect state:
   - Run `git status --short --branch`.
   - Run `git remote -v` if the remote is not already certain.
   - Confirm `target_branch`, `feature_branch`, and `remote`.

2. Update the target branch:
   - Run `git switch <target_branch>`.
   - Run `git pull --rebase <remote> <target_branch>`.

3. Rebase the feature branch onto the updated target:
   - Run `git switch <feature_branch>`.
   - Run `git rebase <target_branch>`.
   - If conflicts occur, follow "Rebase Conflict Handling".

4. Merge the feature branch into the target branch:
   - Run `git switch <target_branch>`.
   - Run `git merge <feature_branch> --no-ff`.
   - If conflicts occur, follow "Merge Conflict Handling".

5. Verify and push the target branch:
   - Run `git status --short --branch`.
   - Run `git log --oneline --graph --decorate -n 20`.
   - If the graph is correct and the worktree is clean, run `git push <remote> <target_branch>`.

6. Sync the feature branch to the merged target:
   - Run `git switch <feature_branch>`.
   - Run `git rebase <target_branch>`.
   - If conflicts occur, follow "Rebase Conflict Handling".

7. Final verification:
   - Run `git status --short --branch`.
   - Run `git log --oneline --graph --decorate -n 20`.
   - Report the final target branch, feature branch, pushed remote, and whether the feature branch is now aligned with the target branch.

## Rebase Conflict Handling

When `git rebase <target_branch>` stops with conflicts:

- Run `git status` to confirm the rebase state and list conflicted files.
- Inspect conflicts with `git diff` and search for conflict markers with `rg "<<<<<<<|=======|>>>>>>>"`.
- Resolve only conflicts whose intent is clear from the surrounding code and project rules.
- If the conflict changes business behavior, API semantics, compatibility, state retention, or another product decision, stop and ask the user to choose.
- After conflicts are resolved by Codex or by the user, run `git add <resolved-files>` and then `git rebase --continue`.
- If more conflicts appear, repeat the same loop.
- If the user asks to abandon the rebase, run `git rebase --abort` only after confirming that this is their intent.

## Merge Conflict Handling

When `git merge <feature_branch> --no-ff` stops with conflicts:

- Run `git status` to confirm the merge state and list conflicted files.
- Inspect conflicts with `git diff` and `rg "<<<<<<<|=======|>>>>>>>"`.
- Resolve only conflicts whose intent is clear.
- If the conflict requires choosing between target-branch behavior and feature-branch behavior, ask the user before editing.
- After conflicts are resolved by Codex or by the user, run `git add <resolved-files>` and then `git commit` to finish the merge commit.
- If the user asks to abandon the merge, run `git merge --abort` only after confirming that this is their intent.

## Resume After User-Resolved Conflicts

Use this section when the user says any of:

- "I resolved the conflicts, continue."
- "I have manually resolved the rebase conflicts."
- "I have manually resolved the merge conflicts."
- "Check Git status and continue the interrupted merge flow."

Resume procedure:

- Run `git status` first.
- If Git reports `rebase in progress`, verify no unresolved conflict markers remain, run `git add <resolved-files>` for resolved files, then run `git rebase --continue`.
- If Git reports an active merge, verify no unresolved conflict markers remain, run `git add <resolved-files>` for resolved files, then run `git commit`.
- If no rebase or merge is active, inspect the branch and commit graph to determine the next unfinished main workflow step.
- If the next step cannot be inferred safely, state the current Git state and ask the user which step to continue from.

## Completion Criteria

The flow is complete only when:

- The target branch contains the feature branch through a `--no-ff` merge commit.
- The target branch has been pushed to the intended remote.
- The feature branch has been rebased onto the updated target branch after the merge.
- `git status --short --branch` shows no unfinished rebase, merge, or unresolved conflicts.
- The final response summarizes the commands completed, any conflicts handled, and the final branch state.
