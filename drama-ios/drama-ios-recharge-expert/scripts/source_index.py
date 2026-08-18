#!/usr/bin/env python3
"""Deterministic, read-only recharge source evidence index."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PRODUCER_PATTERNS = ("POST_NOTIFY", "postNotificationName", "ATHDispatchEvent")
CONSUMER_PATTERNS = ("ADD_NOTIFY", "HANDLER_NOTIFY", "addObserver", "subscribe_")
DECLARATION_PATTERNS = ("EXTERN_KEY", "DECLARE_KEY", "ATHDeclareEvent", "ATHDefineEvent")
SOURCE_SUFFIXES = {
    ".h", ".m", ".mm", ".swift", ".c", ".cc", ".cpp", ".py", ".rb",
    ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", ".yml", ".md",
    ".plist", ".proto",
}
EXCLUDED_PREFIXES = (
    "Cores/pbobjc/",
    "SDK/TurnoverSDK/Protocs/",
    "confuse/",
    "ir_mapping/",
)
SYMBOL_PATTERNS = (
    re.compile(r"^\s*[+-]\s*\([^)]*\)\s*([^\{;]+)"),
    re.compile(r"^\s*@(?:interface|implementation|protocol)\s+([A-Za-z_][A-Za-z0-9_]*)"),
    re.compile(r"^\s*(?:static\s+)?(?:const\s+)?[A-Za-z_][\w<>\s*]*\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)"),
    re.compile(r"^\s*(?:#define|DECLARE_[A-Z_]+|EXTERN_[A-Z_]+)\s*\(?\s*([A-Za-z_][A-Za-z0-9_]*)"),
)


class GitError(RuntimeError):
    pass


def run_git(repo: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise GitError(result.stderr.strip() or "git command failed")
    return result


def repository_root(path: Path) -> Path:
    result = run_git(path, ["rev-parse", "--show-toplevel"])
    return Path(result.stdout.strip()).resolve()


def validate_revision(repo: Path, revision: str | None) -> str | None:
    if not revision:
        return None
    result = run_git(repo, ["rev-parse", "--verify", f"{revision}^{{commit}}"])
    return result.stdout.strip()


def tracked_paths(repo: Path, revision: str | None) -> list[str]:
    if revision:
        output = run_git(repo, ["ls-tree", "-r", "--name-only", revision]).stdout
    else:
        output = run_git(repo, ["ls-files"]).stdout
    return sorted(
        path for path in output.splitlines()
        if Path(path).suffix.lower() in SOURCE_SUFFIXES
        and not path.startswith(EXCLUDED_PREFIXES)
    )


def file_text(repo: Path, path: str, revision: str | None, cache: dict[str, str]) -> str:
    cache_key = f"{revision or 'WORKTREE'}:{path}"
    if cache_key in cache:
        return cache[cache_key]
    if revision:
        result = run_git(repo, ["show", f"{revision}:{path}"], check=False)
        text = result.stdout if result.returncode == 0 else ""
    else:
        candidate = repo / path
        try:
            text = candidate.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeError):
            text = ""
    cache[cache_key] = text
    return text


def enclosing_symbol(lines: list[str], line_number: int) -> str:
    for index in range(min(line_number - 1, len(lines) - 1), -1, -1):
        line = lines[index]
        for pattern in SYMBOL_PATTERNS:
            match = pattern.match(line)
            if match:
                return " ".join(match.group(1).split())
    return "<file-scope>"


def exact_kind(query: str, content: str) -> str:
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", query):
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(query)}(?![A-Za-z0-9_])", content):
            return "symbol_or_key"
    return "literal"


def git_grep(repo: Path, query: str, revision: str | None) -> list[tuple[str, int, str]]:
    args = ["grep", "-n", "-I", "-F", "-e", query]
    if revision:
        args.append(revision)
    args.extend([
        "--",
        ".",
        ":(exclude)Cores/pbobjc/**",
        ":(exclude)SDK/TurnoverSDK/Protocs/**",
        ":(exclude)confuse/**",
        ":(exclude)ir_mapping/**",
    ])
    result = run_git(repo, args, check=False)
    if result.returncode not in (0, 1):
        raise GitError(result.stderr.strip() or "git grep failed")
    matches: list[tuple[str, int, str]] = []
    prefix = f"{revision}:" if revision else ""
    for raw_line in result.stdout.splitlines():
        line = raw_line[len(prefix):] if prefix and raw_line.startswith(prefix) else raw_line
        match = re.match(r"^(.+?):(\d+):(.*)$", line)
        if match:
            matches.append((match.group(1), int(match.group(2)), match.group(3).strip()))
    return matches


def classify_event_role(content: str) -> str | None:
    if content.lstrip().startswith(("//", "/*", "*")):
        return None
    if any(pattern in content for pattern in PRODUCER_PATTERNS):
        return "producer"
    if any(pattern in content for pattern in CONSUMER_PATTERNS):
        return "consumer"
    if any(pattern in content for pattern in DECLARATION_PATTERNS):
        return "declaration"
    return None


def collect_exact(repo: Path, queries: list[str], revision: str | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cache: dict[str, str] = {}
    exact: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int, str]] = set()
    for query in sorted(set(queries)):
        for path, line_number, content in git_grep(repo, query, revision):
            key = (query, path, line_number, content)
            if key in seen:
                continue
            seen.add(key)
            lines = file_text(repo, path, revision, cache).splitlines()
            item = {
                "query": query,
                "match_kind": exact_kind(query, content),
                "path": path,
                "line": line_number,
                "symbol": enclosing_symbol(lines, line_number),
                "content": content,
            }
            exact.append(item)
            role = classify_event_role(content)
            if role:
                events.append({**item, "role": role})
    sort_key = lambda item: (item["query"], item["path"], item["line"], item["content"])
    return sorted(exact, key=sort_key), sorted(events, key=lambda item: (item["query"], item["role"], item["path"], item["line"]))


def commit_paths(repo: Path, commit: str) -> list[str]:
    result = run_git(repo, ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit])
    return sorted(set(result.stdout.splitlines()))


def historical_cochange(repo: Path, seed_paths: list[str], revision: str | None, history_limit: int) -> list[dict[str, Any]]:
    if not seed_paths or history_limit <= 0:
        return []
    args = ["log", f"--max-count={history_limit}", "--format=%H"]
    if revision:
        args.append(revision)
    args.extend(["--", *sorted(seed_paths)[:8]])
    commits = [line for line in run_git(repo, args).stdout.splitlines() if line]
    counts: Counter[str] = Counter()
    witnesses: dict[str, list[str]] = defaultdict(list)
    seed_set = set(seed_paths)
    for commit in commits:
        for path in commit_paths(repo, commit):
            if path in seed_set:
                continue
            counts[path] += 1
            witnesses[path].append(commit)
    return [
        {
            "path": path,
            "shared_commit_count": count,
            "commits": sorted(witnesses[path]),
            "confidence": "investigation_lead_only",
        }
        for path, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:40]
    ]


def name_similarity(paths: list[str], queries: list[str], excluded_paths: set[str]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in paths:
        if path in excluded_paths:
            continue
        lower_path = path.lower()
        tokens = [token for token in re.split(r"[^a-z0-9]+", lower_path) if token]
        stem = Path(path).stem.lower()
        for query in sorted(set(queries)):
            query_lower = query.lower()
            scores = [difflib.SequenceMatcher(None, query_lower, stem).ratio()]
            scores.extend(difflib.SequenceMatcher(None, query_lower, token).ratio() for token in tokens)
            score = max(scores, default=0.0)
            if score < 0.58:
                continue
            candidates.append({
                "query": query,
                "path": path,
                "score": round(score, 3),
                "confidence": "low",
                "use": "investigation_appendix_only",
            })
    return sorted(candidates, key=lambda item: (item["query"], -item["score"], item["path"]))[:80]


def build_index(repo_arg: str, queries: list[str], revision_arg: str | None, history_limit: int) -> dict[str, Any]:
    if not queries or any(not query.strip() for query in queries):
        raise ValueError("at least one non-empty --query is required")
    repo = repository_root(Path(repo_arg).resolve())
    revision = validate_revision(repo, revision_arg)
    normalized_queries = sorted(set(query.strip() for query in queries))
    exact, events = collect_exact(repo, normalized_queries, revision)
    seed_paths = sorted(set(item["path"] for item in exact))
    paths = tracked_paths(repo, revision)
    return {
        "schema_version": 1,
        "repository": str(repo),
        "revision": revision or "WORKTREE",
        "queries": normalized_queries,
        "exact_matches": exact,
        "event_evidence": events,
        "historical_cochange": historical_cochange(repo, seed_paths, revision, history_limit),
        "name_similarity": name_similarity(paths, normalized_queries, set(seed_paths)),
        "limitations": [
            "Static search cannot prove that dynamic callers or subscribers do not exist.",
            "Historical co-change is an investigation lead, not proof of responsibility or dependency.",
            "Name similarity is low confidence and must not block a change or confirm a relationship.",
        ],
        "no_match_interpretation": "No exact match means only that the listed queries were not found by git grep at the listed revision.",
    }


def render_text(index: dict[str, Any]) -> str:
    lines = [f"revision: {index['revision']}", f"queries: {', '.join(index['queries'])}"]
    for category in ("exact_matches", "event_evidence", "historical_cochange", "name_similarity"):
        lines.append(f"\n[{category}]")
        for item in index[category]:
            lines.append(json.dumps(item, ensure_ascii=False, sort_keys=True))
    lines.append("\n[limitations]")
    lines.extend(f"- {item}" for item in index["limitations"])
    lines.append(f"- {index['no_match_interpretation']}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="path inside the Git repository")
    parser.add_argument("--rev", help="commit to index; defaults to the working tree")
    parser.add_argument("--query", action="append", required=True, help="exact symbol, key, event, or literal; repeatable")
    parser.add_argument("--history-limit", type=int, default=30, help="maximum relevant commits to inspect")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        index = build_index(args.repo, args.query, args.rev, args.history_limit)
    except (GitError, ValueError) as error:
        print(f"source_index: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(index))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
