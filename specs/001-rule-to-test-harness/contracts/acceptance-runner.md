# Acceptance Runner Contract

## Invocation

The implementation will provide this one complete-suite command:

```text
specs/001-rule-to-test-harness/harness/run-acceptance.sh /absolute/path/to/legacy/Project
```

The argument is read-only input. Before compilation, the runner verifies the documented source layout contains `src/LMS/Main.java`, `Library.java`, `Loan.java`, `Borrower.java`, `Book.java`, `Person.java`, `Staff.java`, `Librarian.java`, `Clerk.java`, `HoldRequest.java`, and `HoldRequestOperations.java`. It writes compiled classes, captured streams, and reports only to a temporary directory or the harness output directory under this feature root.

## Results

Each emitted result has this logical shape:

```text
[STATUS] Rnn case-label
component: Component
entry-point: public entry point
input/state: scenario summary
expected: expected observable outcome
actual: observed outcome
evidence: verbatim brd.md substring
```

`STATUS` is one of `PASS`, `FAIL`, `DEFERRED`, or `BLOCKED`. The complete run prints exactly one summary result for every R01–R54. R07, R08, R26, and R27 have the required form:

```text
[DEFERRED] Rnn persistence behavior — specs/002-persistence-semantics-spec
```

They are neither compiled as persistence tests nor counted as passes. Any failed or blocked case exits nonzero after the runner has reported all cases it can safely execute.

## Isolation and public-entry-point boundary

The parent runner starts a new JVM for each case. A case may use only documented public constructors, methods, accessors, or console flows of scoped components. It may redirect `System.in` and capture `System.out`; it may not use reflection or change production sources, configuration, schema, or records.

## Console assertion boundary

An assertion can compare exact text or line breaks only if corresponding text appears in frozen evidence. Otherwise the contract requires an observable return, state, membership, or evidenced transition assertion rather than an invented transcript.
