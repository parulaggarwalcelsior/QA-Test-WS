---

description: "Executable implementation tasks for the Java rule-to-test acceptance harness"
---

# Tasks: Rule-to-Test Harness

**Input**: Design documents from `/specs/001-rule-to-test-harness/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/acceptance-runner.md`, and `quickstart.md`

**Scope boundary**: Create only the dependency-free Java harness under this feature directory. The supplied legacy `Project` is read-only input; do not modify Java production sources, configuration, database/schema/records, infrastructure, or create Go code.

**Tests**: The acceptance cases below are the required test deliverable. They must use only public entry points of the eleven scoped components, isolate each case in a fresh JVM, and retain the exact `brd.md` evidence substring for every result.

## Phase 1: Setup (Harness Shell)

**Purpose**: Establish the checked-in, feature-local harness boundary and its one-command invocation.

- [x] T001 Create the executable command shell at `specs/001-rule-to-test-harness/harness/run-acceptance.sh` that accepts one absolute legacy `Project` argument and creates only temporary or feature-local output.
- [x] T002 Create the harness source and fixture directories at `specs/001-rule-to-test-harness/harness/src/lms/acceptance/`, `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/`, and `specs/001-rule-to-test-harness/harness/fixtures/` without adding files to the legacy project.

---

## Phase 2: Foundational (Runner, Isolation, and Traceability)

**Purpose**: Implement the blocking runner capabilities needed before any rule family can execute.

**⚠️ CRITICAL**: No acceptance case family may rely on private members, reflection, shared JVM state, persistence paths, or an altered legacy source tree.

- [ ] T003 Implement the immutable case definition and structured result records, including rule ID, component, public entry point, setup/input, expected/actual outcome, verbatim evidence, status, and deferred destination, in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/RuleCase.java` and `specs/001-rule-to-test-harness/harness/src/lms/acceptance/RuleResult.java`.
- [ ] T004 Implement the 54-row evidence registry in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/RuleCatalog.java`, preserving every R01–R54 ID and `brd.md` substring, assigning exactly R07, R08, R26, and R27 the `DEFERRED` destination `specs/002-persistence-semantics-spec`.
- [ ] T005 Implement the child-process case entry point in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/IsolatedCaseMain.java` to run one selected rule in a fresh JVM, script permitted console input/capture output, and turn assertion failures or unsafe prerequisites into complete `FAIL` or `BLOCKED` results.
- [ ] T006 Implement the parent aggregator in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/AcceptanceRunner.java` to validate all eleven `src/LMS/*.java` inputs, compile only to temporary/feature-local output, launch one JVM per rule, emit exactly one complete result per R01–R54, and exit nonzero only after reporting every safe-to-run result when any executable rule is `FAIL` or `BLOCKED`.
- [ ] T007 Complete `specs/001-rule-to-test-harness/harness/run-acceptance.sh` to invoke `AcceptanceRunner`, reject an invalid source layout before compilation, and ensure the supplied legacy project is neither a compiler output destination nor a write target.

**Checkpoint**: The harness can validate its read-only subject boundary and report the complete registry, including the four persistence deferrals, before behavior-family cases are added.

---

## Phase 3: User Story 1 - Run the behavioral baseline (Priority: P1) 🎯 MVP

**Goal**: Run one traceable suite command that identifies the expected state, actual state, and frozen evidence for every matrix rule without changing the legacy system.

**Independent Test**: Invoke `specs/001-rule-to-test-harness/harness/run-acceptance.sh /absolute/path/to/legacy/Project` and verify one result for each R01–R54, exactly four visible persistence deferrals, and a diagnostic result containing rule ID, scenario, expected/actual outcome, and evidence for a deliberately failing or blocked case.

- [ ] T008 [US1] Implement non-persistent `Main` baseline cases for R01–R06 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/MainBaselineCases.java`, exercising public menu/admin/configuration entry points only and reporting `BLOCKED` rather than starting persistence when a configuration path cannot safely be reached.
- [ ] T009 [US1] Implement the baseline-runner contract checks in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/RunnerContractCases.java` to verify unique R01–R54 result coverage, one-result-per-rule output shape, required failure diagnostics, and the exact `DEFERRED` treatment of R07, R08, R26, and R27.
- [ ] T010 [US1] Wire the R01–R08 registry dispatch and all deferred results through `specs/001-rule-to-test-harness/harness/src/lms/acceptance/IsolatedCaseMain.java` so the complete command reports safe baseline outcomes without calling `Main` startup/shutdown persistence flows.

**Checkpoint**: The single documented command yields an auditable behavioral-baseline report and never represents a deferred persistence rule as a passed executable test.

---

## Phase 4: User Story 2 - Verify guarded library workflows (Priority: P1)

**Goal**: Characterize allowed and rejected public console/library workflows for roles, lookup/list prerequisites, hold, issue, return, renewal, and deletion.

**Independent Test**: Run the case IDs for R09–R17, R19–R21, and R28 against a legacy project with scripted actors and in-memory state; observe both the allowed transition and rejected/non-proceeding guard outcome whenever the evidence distinguishes them.

- [ ] T011 [P] [US2] Implement `Main.allFunctionalities` public-flow cases for R09–R17 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/MainWorkflowCases.java`, covering staff versus borrower hold/info/fine/issue/return/renew paths plus failed borrower lookup and null book-list non-progression.
- [ ] T012 [P] [US2] Implement public `Library.removeBookfromLibrary` and loan-list guard cases for R19–R21 and R28 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/LibraryWorkflowGuardCases.java`, covering borrowed-book rejection, hold-deletion confirmation decline/accept cascade, and empty/nonempty borrower-loan paths without database setup.
- [ ] T013 [US2] Register and dispatch R09–R17, R19–R21, and R28 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/IsolatedCaseMain.java`, ensuring each rule emits one summarized result that names both permitted and rejected scenario inputs where applicable.

**Checkpoint**: Guarded workflow cases demonstrate that only the documented role/state reaches each public transition, while rejected paths leave the guarded action unperformed.

---

## Phase 5: User Story 3 - Verify domain state and identity rules (Priority: P2)

**Goal**: Characterize public domain identity, collection, queue, lookup, search, fine, role-number, and printed-output behavior supporting the console workflows.

**Independent Test**: Run the case IDs for R18, R22–R25, and R29–R54 and verify observable public state/accessor results, queue order, captured evidence-backed output, and supplied versus automatic number behavior in isolated JVMs.

- [ ] T014 [P] [US3] Implement public `Library` singleton, login, librarian fallback, exact search, and typed lookup cases for R18 and R22–R25 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/LibraryStateCases.java`.
- [ ] T015 [P] [US3] Implement public `Borrower` confirmation and collection association cases for R29–R35 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/BorrowerStateCases.java`, covering `y` progression and rejected confirmation plus borrowed/on-hold add/remove membership.
- [ ] T016 [P] [US3] Implement public `Loan` fine and renewal cases for R36–R42 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/LoanCases.java`, covering positive/nonpositive overdue calculations, paid-fine non-recalculation, y/Y and n/N choices, no-fine payment state, and supplied renewal dates.
- [ ] T017 [P] [US3] Implement public `Person`, `Clerk`, `Librarian`, and `Staff` cases for R43–R50 and R54 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/IdentityAndStaffCases.java`, asserting automatic/supplied ID, desk, and office behavior, counter advancement, default password, one-librarian rejection, and only the frozen-evidence-supported staff output.
- [ ] T018 [P] [US3] Implement public `Book`, `HoldRequest`, and `HoldRequestOperations` queue/identity cases for R51–R53 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/HoldQueueAndBookCases.java`, asserting append-at-end, oldest-first removal, borrower association visibility, and book-ID counter advancement.
- [ ] T019 [US3] Register and dispatch R18, R22–R25, and R29–R54 in `specs/001-rule-to-test-harness/harness/src/lms/acceptance/IsolatedCaseMain.java`, preserving a separate structured result for every rule and capturing exact console text only where the catalog carries frozen transcript evidence.

**Checkpoint**: All in-scope domain rules are observable through the named public behavior, with no dependency on execution order, singleton reset, counter reset, or database state outside the fresh JVM process.

---

## Phase 6: Polish & Cross-Cutting Validation

**Purpose**: Complete the safe execution boundary, final traceability review, and maintainer-facing validation instructions.

- [ ] T020 Update execution and expected-result guidance in `specs/001-rule-to-test-harness/quickstart.md` to match the implemented command, 50 executable outcomes, four named deferrals, and nonzero failure/blocked exit behavior.
- [ ] T021 Add a pre/post-run legacy-input integrity check to `specs/001-rule-to-test-harness/harness/run-acceptance.sh` that reports a failure if any scoped source input changed, while retaining temporary/feature-local compilation output only.
- [ ] T022 Validate all 54 registry entries against the matrix and output contract in `specs/001-rule-to-test-harness/contracts/acceptance-runner.md`, correcting harness-only traceability gaps without expanding persistence, infrastructure, Go, or production-code scope.
- [ ] T023 Run the complete command documented in `specs/001-rule-to-test-harness/quickstart.md` against an unchanged supplied legacy project and resolve harness defects until R01–R06, R09–R25, and R28–R54 are `PASS`, R07/R08/R26/R27 are `DEFERRED`, and the command leaves the supplied project unchanged.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately.
- **Foundational (Phase 2)**: Depends on T001–T002 and blocks all rule-family work.
- **User Story 1 (Phase 3)**: Depends on the runner and registry in Phase 2.
- **User Story 2 (Phase 4)**: Depends on Phase 2; it may proceed alongside US1 once the runner interface is stable.
- **User Story 3 (Phase 5)**: Depends on Phase 2; it may proceed alongside US1 and US2 once the runner interface is stable.
- **Polish (Phase 6)**: Depends on all rule-family registration and execution.

### User Story Dependencies

- **US1 (P1)**: Starts after foundational runner work; establishes the complete reporting baseline and its Main/configuration cases.
- **US2 (P1)**: Starts after foundational runner work; has no domain-case dependency on US1, but relies on the shared result format.
- **US3 (P2)**: Starts after foundational runner work; has no case dependency on US1 or US2, but relies on the shared result format.

### Within Each User Story

- Implement case assertions through public entry points before adding their dispatch entry.
- Include proceeding and rejected/non-proceeding state in one rule result where the verified evidence distinguishes both paths.
- Do not add persistence fixtures, source modifications, reflection, or undocumented transcript assertions to make a case pass.

## Parallel Opportunities

- T011 and T012 can proceed in parallel because they write separate workflow case files.
- T014–T018 can proceed in parallel because each owns a separate domain case file.
- Once Phase 2 is stable, the US2 and US3 case-file tasks can proceed alongside the US1 baseline case file; only the `IsolatedCaseMain.java` registration tasks must be serialized.

## Parallel Example: User Story 3

```text
Task: "Implement Library singleton/login/search/lookup cases in specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/LibraryStateCases.java"
Task: "Implement Borrower confirmation and collection cases in specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/BorrowerStateCases.java"
Task: "Implement Loan fine and renewal cases in specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/LoanCases.java"
Task: "Implement identity and Staff cases in specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/IdentityAndStaffCases.java"
Task: "Implement hold queue and Book identity cases in specs/001-rule-to-test-harness/harness/src/lms/acceptance/cases/HoldQueueAndBookCases.java"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001–T007 to establish an isolated, read-only runner and complete evidence registry.
2. Complete T008–T010 to make the single command report all 54 IDs, the four deferrals, and usable failure diagnostics.
3. Validate the baseline command and its no-persistence boundary before adding workflow/domain families.

### Incremental Delivery

1. Add US2 workflow cases and validate permitted/rejected flow outcomes independently.
2. Add US3 domain case families in parallel, then serialize their dispatcher registration.
3. Finish the full-suite, source-integrity, and quickstart checks in Phase 6.

### Format Validation

All 23 tasks use the required checklist format: checkbox, sequential task ID, `[P]` only for independently editable files, `[US#]` for user-story tasks, and an exact target file or directory path.
