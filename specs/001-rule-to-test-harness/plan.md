# Implementation Plan: Rule-to-Test Harness

**Branch**: `001-rule-to-test-harness` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-rule-to-test-harness/spec.md`

## Summary

Deliver a dependency-free, executable Java acceptance harness for the unchanged legacy Library Management System. The harness will run isolated cases through documented public entry points, emit one traceable result per R01–R54, and label R07, R08, R26, and R27 as deferred to specification 002. All harness assets remain under this feature directory; the harness will not write to the legacy production tree, stored records, or database structures.

## Technical Context

**Language/Version**: Java, compiled and run with the JDK used by the current Java subject

**Primary Dependencies**: JDK `javac` and `java` only; no test framework or external service

**Storage**: N/A — temporary compilation and case output only; the harness neither opens nor mutates Derby, schema, or stored records

**Testing**: Dependency-free Java acceptance runner invoked by one checked-in shell command; each result includes a stable rule ID and evidence reference

**Target Platform**: Local environment capable of compiling and running the supplied current Java legacy project

**Project Type**: Console front-end and back-end characterization harness

**Performance Goals**: Complete the 50 executable rule results in one local invocation; runtime is not a product requirement

**Constraints**: Public entry points only; fresh JVM per case; captured console streams; no production edits, Go code, persistence execution, database fixture, configuration mutation, or external dependency. Exact text/line-break assertions only use frozen transcript evidence.

**Scale/Scope**: 54 rule IDs across 11 scoped components; 50 executable in this feature and four persistence IDs visibly deferred to specification 002

## Constitution Check

*GATE: Passed before Phase 0 research; re-checked after Phase 1 design.*

| Constitution gate | Pre-design result | Post-design result |
| --- | --- | --- |
| Evidence-grounded behavioral parity | Pass — every result is keyed to R01–R54 and verbatim `brd.md` evidence. | Pass — the result contract requires rule ID, input/state, expected/actual outcome, and evidence. |
| Console interface is public | Pass — console cases use documented `Main`, `Library`, `Borrower`, `Loan`, and `Book` public flows. | Pass — transcript checks are limited to frozen evidence; no prompt is inferred. |
| Go 1.22 front-end/back-end boundary | Justified feature exception — this roadmap item is an explicit Java characterization harness and excludes Go production work. | Pass — all planned content is test-only under this feature; no database or infrastructure path is planned. |
| Behavioral tests | Pass — the deliverable is the baseline acceptance suite. | Pass — isolated table-driven case registries cover permitted and rejected paths. |
| Small, reviewable changes | Pass — only harness assets and design artifacts are planned. | Pass — runner, cases, fixtures, and contracts are isolated from production. |

R07, R08, R26, and R27 are deferred traceability results, not database work.

## Project Structure

### Documentation and Harness

```text
specs/001-rule-to-test-harness/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── scope.json
├── contracts/
│   └── acceptance-runner.md
└── harness/
    ├── run-acceptance.sh
    ├── src/lms/acceptance/
    │   ├── AcceptanceRunner.java
    │   ├── RuleCase.java
    │   ├── RuleResult.java
    │   ├── IsolatedCaseMain.java
    │   └── cases/
    └── fixtures/
```

**Structure Decision**: The harness is an adjunct to, never a modification of, the legacy Java project. Its sole write root is `specs/001-rule-to-test-harness/`; it receives a legacy project directory as a read-only command argument and uses temporary directories for compiled classes and output.

## Complexity Tracking

No complexity violations require tracking. The documented Java-only harness exception is limited to this migration-baseline feature and does not permit production Java changes or production Go work.
