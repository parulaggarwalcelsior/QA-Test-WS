# Quickstart: Validate the Rule-to-Test Harness

## Prerequisites

- A JDK capable of compiling the unchanged legacy Java project.
- A local, read-only path to the legacy `Project` directory whose `src/LMS` directory contains the 11 scoped Java files named in the [acceptance-runner contract](contracts/acceptance-runner.md).
- This feature's harness implementation, created under `specs/001-rule-to-test-harness/harness/`.

No Derby database, fixture, network service, Go toolchain, schema, or infrastructure setup is required or permitted for this validation.

## Run the complete suite

From the workspace root, run:

```text
specs/001-rule-to-test-harness/harness/run-acceptance.sh /absolute/path/to/legacy/Project
```

The runner validates the supplied source layout, compiles only into temporary/harness output, then runs each case in its own JVM. See the [runner contract](contracts/acceptance-runner.md) for result and exit-status semantics.

## Expected validation outcome

- R01–R06, R09–R25, R28–R54 produce a traceable `PASS`, `FAIL`, or safe `BLOCKED` result; every executable failure identifies its rule, scenario, expected/actual result, and legacy evidence.
- R07, R08, R26, and R27 produce `DEFERRED` results naming `specs/002-persistence-semantics-spec`.
- Legacy project files, database structures, and stored records remain unchanged before and after the command.

The [data model](data-model.md) defines registry and result fields; `spec.md` remains the authoritative 54-rule matrix.
