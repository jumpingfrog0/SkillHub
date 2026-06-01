---
name: git-rebase-flow
description: "Use when Codex needs to guide or execute a standard Git rebase flow for a development branch: stash local work, update the base branch with pull --rebase, rebase the development branch, handle conflicts step by step, push with --force-with-lease, merge back with --no-ff, and return to the development branch. Also use for drama-ios branch flows such as drama-ios_2.19.0_donghong_maint based on drama-ios_2.19.0_maint."
---

# Git Rebase Flow

## Overview

Use this skill for a guided Git flow where a development branch is rebased onto its base branch, pushed safely, merged back into the base branch with `--no-ff`, then the workspace returns to the development branch.

This skill is intentionally guidance-first. Do not hide branch changes, conflict states, force-style pushes, or merges behind a script.

## Required Inputs

Confirm these values before mutating anything:

- Repository root.
- Development branch, for example `drama-ios_2.19.0_donghong_maint`.
- Base branch, for example `drama-ios_2.19.0_maint`.
- Remote name, default `origin`.

If the user gives only the current branch and base branch, treat the current branch as the development branch after verifying it with Git.

## Safety Rules

- Run `git status --short --branch` first and read the result before changing branches.
- If the current branch is not the expected development branch, stop and confirm before continuing.
- Treat "temporarily save local changes" as `git stash push -u`, not `git add`.
- Before any push, `--force-with-lease`, or merge into the base branch, state the current branch and the exact command to be run.
- Push a rebased development branch with `git push <remote> <dev-branch> --force-with-lease`; do not use a bare force push.
- Do not guess conflict resolutions. When `pull --rebase`, `rebase`, or `merge` conflicts occur, inspect the conflict state, report the files, and resolve only when the correct resolution is clear from context or the user provides direction.
- If local work was stashed, do not automatically apply it at the end. Remind the user to inspect `git stash list` and run `git stash pop` when they are ready.
- For drama-ios, follow project validation constraints: do not proactively run project build, compiler, or SDK discovery commands unless the user explicitly asks. Use static checks such as `rg`, `git diff --check`, or `plutil -lint` when appropriate.

## Workflow

1. Confirm the workspace and branches:

```bash
git status --short --branch
git branch --show-current
```

2. If there are local modifications, save them:

```bash
git stash push -u
```

Record that a stash was created so the final response can mention it.

3. Update the base branch:

```bash
git checkout <base-branch>
git pull --rebase
```

If this conflicts, stop in the rebase state, report the conflict files, and continue only after conflicts are resolved with `git rebase --continue` or the user chooses to abort.

4. Rebase the development branch:

```bash
git checkout <dev-branch>
git rebase <base-branch>
```

If conflicts occur, repeat this loop until the rebase is complete:

```bash
git status --short
# resolve conflicts
git add <resolved-files>
git rebase --continue
```

5. Push the rebased development branch safely:

```bash
git push <remote> <dev-branch> --force-with-lease
```

6. Merge the development branch back into the base branch:

```bash
git checkout <base-branch>
git merge <dev-branch> --no-ff
```

If the merge conflicts, stop, report conflict files, and resolve only with clear direction.

7. Validate according to the repository's rules. In drama-ios, do not run build commands unless explicitly asked; tell the user that the local build step still needs to be run or was intentionally skipped because of project constraints.

8. Push the base branch after validation:

```bash
git push <remote> <base-branch>
```

9. Return to the development branch:

```bash
git checkout <dev-branch>
```

10. If a stash was created, remind the user that it remains available and was not restored automatically.

## Final Response Checklist

Include:

- Final current branch.
- Whether the development branch was rebased and pushed with `--force-with-lease`.
- Whether the base branch was merged with `--no-ff` and pushed.
- Any conflict files that required manual handling.
- Whether validation/build was run, skipped, or still needed.
- Whether a stash was created and left unapplied.
