#!/usr/bin/env python3
"""Deterministic tests for source_index.py; no project build is invoked."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("source_index.py")


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout


class SourceIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        run(["git", "init", "-q"], self.repo)
        run(["git", "config", "user.name", "Index Test"], self.repo)
        run(["git", "config", "user.email", "index@example.invalid"], self.repo)
        (self.repo / "Producer.m").write_text(
            "#define POST_NOTIFY(x) x\n- (void)send { POST_NOTIFY(kPaymentDone); }\n",
            encoding="utf-8",
        )
        (self.repo / "Consumer.m").write_text(
            "#define ADD_NOTIFY(x) x\n- (void)listen { ADD_NOTIFY(kPaymentDone); }\n// ADD_NOTIFY(kPaymentDone)\n",
            encoding="utf-8",
        )
        (self.repo / "RechargeContext.m").write_text(
            "@implementation RechargeContext\n- (void)saveTraceId { NSString *traceId = @\"t\"; }\n@end\n",
            encoding="utf-8",
        )
        env = dict(os.environ, GIT_AUTHOR_DATE="2025-01-01T00:00:00Z", GIT_COMMITTER_DATE="2025-01-01T00:00:00Z")
        run(["git", "add", "."], self.repo, env)
        run(["git", "commit", "-q", "-m", "initial payment event"], self.repo, env)
        self.baseline = run(["git", "rev-parse", "HEAD"], self.repo).strip()
        (self.repo / "Future.m").write_text("void futureOrderId(void) {}\n", encoding="utf-8")
        env = dict(os.environ, GIT_AUTHOR_DATE="2025-01-02T00:00:00Z", GIT_COMMITTER_DATE="2025-01-02T00:00:00Z")
        run(["git", "add", "."], self.repo, env)
        run(["git", "commit", "-q", "-m", "future symbol"], self.repo, env)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def index(self, *queries: str, revision: str | None = None) -> tuple[str, dict]:
        command = ["python3", str(SCRIPT), "--repo", str(self.repo), "--history-limit", "10"]
        if revision:
            command.extend(["--rev", revision])
        for query in queries:
            command.extend(["--query", query])
        output = run(command, self.repo)
        return output, json.loads(output)

    def test_output_is_stable_and_roles_are_separate(self) -> None:
        first, parsed = self.index("kPaymentDone")
        second, _ = self.index("kPaymentDone")
        self.assertEqual(first, second)
        roles = {item["role"] for item in parsed["event_evidence"]}
        self.assertEqual(roles, {"consumer", "producer"})
        self.assertFalse(any(item["content"].startswith("//") for item in parsed["event_evidence"]))
        self.assertTrue(all(item["path"] for item in parsed["exact_matches"]))
        self.assertTrue(all(item["symbol"] for item in parsed["exact_matches"]))

    def test_revision_excludes_future_knowledge(self) -> None:
        _, parsed = self.index("futureOrderId", revision=self.baseline)
        self.assertEqual(parsed["exact_matches"], [])
        self.assertEqual(parsed["revision"], self.baseline)

    def test_low_confidence_and_limitations_cannot_block(self) -> None:
        _, parsed = self.index("RechargeContext")
        self.assertTrue(all(item["confidence"] == "low" for item in parsed["name_similarity"]))
        self.assertIn("Static search cannot prove", " ".join(parsed["limitations"]))
        self.assertTrue(all(item["confidence"] == "investigation_lead_only" for item in parsed["historical_cochange"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
