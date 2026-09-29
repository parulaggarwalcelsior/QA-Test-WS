# Research: Rule-to-Test Harness

## Decision: use a dependency-free Java harness

The subject is Java and the frozen documentation names no existing test framework or build tool. The harness will compile its own small runner with the JDK used for the subject and will not add JUnit, Maven, Gradle, Go, or an external service.

**Rationale**: This is the least-assumptive way to characterize the current system while respecting FR-001, FR-003, FR-013, and the no-new-dependency rule in the constitution.

**Alternatives considered**: JUnit is rejected because no version or dependency mechanism is recorded. A Go harness is rejected because the feature explicitly excludes Go code. Modifying the Java subject to expose test hooks is rejected by FR-003 and FR-013.

## Decision: receive the legacy Java project as a read-only command argument

The frozen evidence identifies legacy files as `Project/src/LMS/*.java`, but it records no repository location or execution command. The runner interface will take an absolute legacy-project directory supplied by the operator and verify that it contains those sources before compiling or running anything.

**Rationale**: It makes the source/build boundary explicit and prevents the harness from assuming that this documentation workspace is the legacy repository.

**Alternatives considered**: Hard-coding a relative legacy path is rejected because the AGENTS instructions permit work only in this workspace and the documents do not establish such a path. Copying or editing the subject is rejected because it would defeat unchanged-system characterization.

## Decision: isolate executable cases by JVM process

The acceptance runner will launch one fresh JVM per case and aggregate structured results. Its fixtures will construct only in-memory domain state through public constructors and methods, or script documented console input through existing public flows.

**Rationale**: `Library` is a singleton and `Person`, `Book`, `Clerk`, and `Librarian` have global counters. A fresh process prevents a case's singleton, static counter, `System.in`, or captured `System.out` state from changing another case's expected result (FR-011).

**Alternatives considered**: Resetting private/static state by reflection is rejected by FR-003. A shared JVM with ordered tests is rejected because it hides state coupling and makes results order-dependent.

## Decision: encode the rule matrix as a case registry with deferred outcomes

Each registry row will contain exactly one rule ID, a public entry point, setup/input label, expected observable result, and the verbatim evidence substring from `brd.md`. A guarded rule can have multiple table rows, but every emitted row retains the one rule ID it characterizes. R07, R08, R26, and R27 will be emitted as `DEFERRED: specs/002-persistence-semantics-spec`, not as a pass or a skipped executable assertion.

**Rationale**: The registry makes the 54-row matrix auditable and fulfils SC-001 and SC-002 without fabricating persistence behavior.

**Alternatives considered**: A prose-only mapping cannot execute or diagnose a failure. Treating deferred persistence rows as passing would misrepresent coverage. Executing them would violate FR-014 and the declared database exclusion.

## Decision: assert console text only when it is frozen evidence

The runner will capture standard output only for messages or line breaks actually recorded in frozen legacy evidence, such as staff salary augmentation and documented rejection messages. Other console cases will assert public return values, collection membership, state transitions, or the presence/absence of the guarded action.

**Rationale**: The constitution declares the console contract public but forbids inventing transcripts; FR-015 applies that limit directly to this feature.

**Alternatives considered**: Snapshotting undocumented whole-console sessions would establish new behavior not justified by the frozen corpus. Ignoring output entirely would lose the tested parts of the console contract.

## Decision: protect the no-persistence boundary at runner start

The runner will fail fast unless its invocation can compile and exercise only the in-memory/public paths needed for the 50 executable rules. It will not call startup/shutdown persistence paths or create a Derby fixture. The Main configuration rows R03–R06 are exercised only by the documented non-persistent initialization boundary; if that boundary cannot be entered without persistence in the supplied subject, the runner reports the case as blocked with its rule ID and evidence rather than writing state.

**Rationale**: FR-013 and FR-014 prohibit a test suite from trading persistence writes for coverage. A truthful blocked result is diagnosable and does not claim an unobserved pass.

**Alternatives considered**: Invoking full `Main.main` against a live Derby connection is rejected because the documents show startup population and shutdown write-back. Mocking a connection by production changes or database fixtures is out of scope.
