# Acceptance Harness Data Model

This model describes harness-only, in-memory records. It does not introduce a database model, schema, fixture, or persistence representation.

## AcceptanceCase

| Field | Meaning | Validation |
| --- | --- | --- |
| `ruleId` | One matrix ID from R01–R54. | Required; unique per result. |
| `caseLabel` | Stable label for a permitted, rejected, or state-transition scenario. | Required; includes input/state. |
| `component` | One scoped component named by the matrix. | Must be one of the 11 components in `scope.json`. |
| `publicEntryPoint` | Constructor or documented public method/flow invoked by the case. | Required; no reflection, private member, or source modification. |
| `setup` | In-memory objects and scripted standard input required before the action. | Must not require a database, stored record, or altered production configuration. |
| `action` | The public call or console flow under test. | Required. |
| `expected` | Observable state, return, collection, or evidenced output expectation. | Required. |
| `evidence` | Verbatim substring from `../../old/docs/brd.md`. | Required and non-empty. |
| `status` | `PASS`, `FAIL`, `DEFERRED`, or `BLOCKED`. | R07, R08, R26, R27 are always `DEFERRED` in this feature. |

## RuleResult

| Field | Meaning |
| --- | --- |
| `ruleId` | The one rule ID represented by the result. |
| `caseLabel` | Scenario identity, including role/input/state. |
| `status` | Outcome from case execution. |
| `expected` | Expected observable result. |
| `actual` | Captured return, state summary, output summary, or thrown failure. |
| `evidenceReference` | `brd.md` component plus stored verbatim evidence substring. |
| `deferredTo` | Set only for the four persistence rows, to `specs/002-persistence-semantics-spec`. |

`FAIL` and `BLOCKED` results expose all fields above. `DEFERRED` results expose rule ID, legacy evidence, reason, and destination specification. A run succeeds only when all executable results are `PASS` and all four persistence rows are `DEFERRED`.

## FixtureState

Fixture state is created afresh per JVM process. It may contain public instances of `Library`, `Borrower`, `Book`, `Loan`, `Person`, `Staff`, `Librarian`, `Clerk`, `HoldRequest`, and `HoldRequestOperations`, plus scripted console input and captured standard output.

```text
Library ── persons/books/loans ──> Person, Book, Loan
Borrower ── borrowedBooks ──> Loan ── book ──> Book
Borrower ── onHoldBooks ──> HoldRequest ──> Book
HoldRequestOperations ── queue (oldest first) ──> HoldRequest
Staff (Clerk | Librarian) ── issues/returns ──> Loan
```

The harness observes these links only through documented public constructors, methods, accessors, and console flows.

## Case registry coverage

| Rule IDs | Case family and primary public entry point(s) |
| --- | --- |
| R01–R06 | `Main.takeInput`, administrative `Main` flow, and non-persistent initialization boundary |
| R07–R08 | Deferred persistence traceability only |
| R09–R17 | `Main.allFunctionalities` scripted role, lookup, list, issue, return, and renewal flows |
| R18–R28 | `Library.getInstance`, `login`, `findBorrower`, `findClerk`, removal/search and nonempty-loan flows |
| R26–R27 | Deferred persistence traceability only |
| R29–R35 | `Borrower` update and collection methods |
| R36–R42 | `Loan.computeFine1`, `payFine`, and `renewIssuedBook` |
| R43–R45 | `Librarian` construction and `addLibrarian` |
| R46–R48 | `Person` construction and `setIDCount` |
| R49–R50 | `Clerk` construction |
| R51–R52 | Public hold-placement/service flows and `HoldRequestOperations` queue observation |
| R53 | `Book` construction and public identity observation |
| R54 | Public `Staff.printInfo` output capture |

For R01, R02, R09–R17, R19–R25, R28–R31, and R36–R42, the registry contains explicit proceeding and rejected/non-proceeding rows wherever the evidence distinguishes both paths.
