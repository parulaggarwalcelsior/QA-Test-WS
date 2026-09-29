#!/usr/bin/env python3
"""Black-box referee tests for the Rule-to-Test Harness work order.

Run explicitly (the directory is intentionally hidden):
  .referee/001-rule-to-test-harness/run-referee-tests.sh /absolute/path/to/Project

The optional argument can instead be supplied in REFEREE_LEGACY_PROJECT.  The
tests deliberately interact only with the documented feature-local command and
its report; they never edit the supplied legacy project.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


DEFERRED = {"R07", "R08", "R26", "R27"}
RULE_IDS = [f"R{number:02d}" for number in range(1, 55)]
DEFERRED_DESTINATION = "specs/002-persistence-semantics-spec"

# These are the verbatim brd.md substrings frozen by the verified-rule matrix.
# Keeping the oracle here makes a missing or substituted evidence citation a
# harness failure, rather than trusting the implementation's own catalog.
EVIDENCE = {
    "R01": 'if((!choice.matches(".*[a-zA-Z]+.*")) && (Integer.parseInt(choice) > min && Integer.parseInt(choice) < max))',
    "R02": 'if(aPass.equals("lib"))',
    "R03": "lib.setFine(20);",
    "R04": "lib.setRequestExpiry(7);",
    "R05": "lib.setReturnDeadline(5);",
    "R06": 'lib.setName("FAST Library");',
    "R07": "lib.populateLibrary(con);",
    "R08": "lib.fillItBack(con);",
    "R09": '"Clerk".equals(person.getClass().getSimpleName()) || "Librarian".equals(person.getClass().getSimpleName())',
    "R10": "b.makeHoldRequest((Borrower)person);",
    "R11": '"Clerk".equals(person.getClass().getSimpleName()) || "Librarian".equals(person.getClass().getSimpleName())',
    "R12": '"Clerk".equals(person.getClass().getSimpleName()) || "Librarian".equals(person.getClass().getSimpleName())',
    "R13": "b.issueBook(bor, (Staff)person);",
    "R14": "l.getBook().returnBook(bor, l, (Staff)person);",
    "R15": "loans.get(input).renewIssuedBook(new java.util.Date());",
    "R16": "if (bor != null)",
    "R17": "if (books != null)",
    "R18": "if(obj==null)",
    "R19": "if (borBooks.get(j).getBook() == b)",
    "R20": "if(!hRequests.isEmpty())",
    "R21": "hr.getBorrower().removeHoldRequest(hr);",
    "R22": "persons.get(i).getID() == id && persons.get(i).getPassword().equals(password)",
    "R23": "librarian.getID() == id && librarian.getPassword().equals(password)",
    "R24": "if (b.getTitle().equals(title))",
    "R25": 'persons.get(i).getClass().getSimpleName().equals("Borrower")',
    "R26": "Book.setIDCount(maxID)",
    "R27": "stmt.setNull(6,Types.INTEGER);",
    "R28": "if (!loans.isEmpty())",
    "R29": "if(choice.equals(\"y\"))",
    "R30": "if(choice.equals(\"y\"))",
    "R31": "if(choice.equals(\"y\"))",
    "R32": "borrowedBooks.add(iBook);",
    "R33": "borrowedBooks.remove(iBook);",
    "R34": "onHoldBooks.add(hr);",
    "R35": "onHoldBooks.remove(hr);",
    "R36": "totalFine = days * Library.getInstance().per_day_fine;",
    "R37": "if (!finePaid)",
    "R38": 'choice.equals("y") || choice.equals("Y")',
    "R39": 'choice.equals("n") || choice.equals("N")',
    "R40": "finePaid = true;",
    "R41": "issuedDate = iDate;",
    "R42": "if (!finePaid)",
    "R43": "if (of == -1)",
    "R44": "currentOfficeNumber++;",
    "R45": "if (librarian == null) {",
    "R46": "if(idNum==-1)",
    "R47": "password = Integer.toString(id);",
    "R48": "public static void setIDCount(int n)",
    "R49": "if(dk == -1)",
    "R50": "currentdeskNumber++;",
    "R51": "holdRequests.add(hr);",
    "R52": "holdRequests.remove(0);",
    "R53": "currentIdNumber++;",
    "R54": "super.printInfo();",
}


def snapshot_tree(root: Path) -> dict[str, tuple[str, str]]:
    """Content/path snapshot, without interpreting any legacy source file."""
    result: dict[str, tuple[str, str]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            relative = str(path.relative_to(root))
            if path.is_symlink():
                result[relative] = ("link", os.readlink(path))
            elif path.is_dir():
                result[relative] = ("dir", "")
            elif path.is_file():
                digest = hashlib.sha256()
                with path.open("rb") as handle:
                    for block in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(block)
                result[relative] = ("file", digest.hexdigest())
    return result


class AcceptanceHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = Path(__file__).resolve().parents[2]
        cls.command = cls.repo / "specs/001-rule-to-test-harness/harness/run-acceptance.sh"
        supplied = os.environ.get("REFEREE_LEGACY_PROJECT")
        candidates = [Path(supplied)] if supplied else [
            cls.repo / "Project",
            cls.repo / "old/Project",
            cls.repo.parent / "Project",
            cls.repo.parent / "old/Project",
        ]
        cls.legacy = next(
            (path.resolve() for path in candidates if (path / "src/LMS").is_dir()),
            None,
        )
        if cls.legacy is None:
            raise AssertionError(
                "Supply the unchanged legacy Project as an absolute argument or "
                "REFEREE_LEGACY_PROJECT; expected a directory containing src/LMS."
            )

    def run_command(self, *args: str, timeout: int = 420) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.command), *args],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )

    def test_01_command_is_executable_and_rejects_unsafe_inputs(self) -> None:
        self.assertTrue(self.command.is_file(), "The documented feature-local command is missing.")
        self.assertTrue(os.access(self.command, os.X_OK), "run-acceptance.sh must be executable.")

        before = snapshot_tree(self.legacy)
        missing_argument = self.run_command()
        self.assertNotEqual(missing_argument.returncode, 0, "Command must require its Project argument.")

        relative_argument = self.run_command(self.legacy.name)
        self.assertNotEqual(
            relative_argument.returncode,
            0,
            "The documented runner accepts one absolute legacy Project argument only.",
        )

        with tempfile.TemporaryDirectory(prefix="referee-invalid-project-") as temporary:
            invalid_project = Path(temporary)
            invalid_before = snapshot_tree(invalid_project)
            invalid_layout = self.run_command(str(invalid_project))
            self.assertNotEqual(invalid_layout.returncode, 0, "Invalid source layout must be rejected before compilation.")
            self.assertEqual(
                invalid_before,
                snapshot_tree(invalid_project),
                "Invalid input was changed while validating its source layout.",
            )

        self.assertEqual(before, snapshot_tree(self.legacy), "Argument validation changed the legacy project.")

    def test_02_complete_read_only_traceable_baseline(self) -> None:
        before = snapshot_tree(self.legacy)
        completed = self.run_command(str(self.legacy))
        report = completed.stdout
        after = snapshot_tree(self.legacy)

        self.assertEqual(
            before,
            after,
            "The acceptance harness changed its supplied legacy Project. It must compile and report outside it.",
        )
        self.assertEqual(
            completed.returncode,
            0,
            "An unchanged current system must yield a successful baseline. Output follows:\n" + report,
        )

        # Results may be one line, pretty-printed JSON, or another structured
        # multiline form.  A rule label is therefore the record boundary rather
        # than a prescribed serialization format.
        occurrences = list(re.finditer(r"\bR(?:0[1-9]|[1-4][0-9]|5[0-4])\b", report))
        found_ids = [match.group(0) for match in occurrences]
        self.assertEqual(
            len(occurrences),
            54,
            "The report must emit exactly one result record for each matrix rule, not a partial or duplicate list.",
        )
        self.assertEqual(set(found_ids), set(RULE_IDS), "The complete R01–R54 matrix is not represented.")

        records: dict[str, str] = {}
        for index, match in enumerate(occurrences):
            end = occurrences[index + 1].start() if index + 1 < len(occurrences) else len(report)
            records[match.group(0)] = report[match.start():end]

        for rule in RULE_IDS:
            record = records[rule]
            statuses = re.findall(r"\b(PASS|FAIL|BLOCKED|DEFERRED)\b", record, re.IGNORECASE)
            self.assertEqual(len(statuses), 1, f"{rule} must have exactly one result status. Record:\n{record}")
            status = statuses[0].upper()
            if rule in DEFERRED:
                self.assertEqual(status, "DEFERRED", f"{rule} is persistence-only and must be visibly deferred.")
                self.assertIn(
                    DEFERRED_DESTINATION,
                    record,
                    f"{rule} must name its destination specification on its result record.",
                )
            else:
                self.assertEqual(status, "PASS", f"{rule} is executable and must pass against the unchanged subject.")

        # The evidence is deliberately checked against this independent matrix;
        # a runner cannot satisfy traceability merely by printing rule IDs.
        rendered_evidence = report.replace(r'\"', '"')
        for rule, evidence in EVIDENCE.items():
            self.assertIn(evidence, rendered_evidence, f"{rule} does not report its verbatim frozen legacy evidence.")


def _main() -> None:
    # Permit the promised one-command referee invocation while preserving normal
    # unittest discovery semantics when no explicit subject path is supplied.
    if len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
        supplied = Path(sys.argv.pop(1))
        if not supplied.is_absolute():
            raise SystemExit("Referee legacy Project argument must be absolute.")
        os.environ["REFEREE_LEGACY_PROJECT"] = str(supplied)
    unittest.main(verbosity=2)


if __name__ == "__main__":
    _main()
