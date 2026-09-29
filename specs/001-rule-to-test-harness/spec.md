# Feature Specification: Rule-to-Test Harness

**Feature Branch**: `001-rule-to-test-harness`  
**Created**: 2026-09-29  
**Status**: Draft  
**Input**: User description: "Produce an executable acceptance test harness encoding the verified rules against the current Java system."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run the behavioral baseline (Priority: P1)

As a migration team member, I can run one acceptance suite against the current library system and see whether each verified front-end and back-end rule still holds, so that later work has a trustworthy behavioral baseline.

**Why this priority**: The baseline is the prerequisite for every later migration or extraction activity in the roadmap.

**Independent Test**: Run the documented suite against an unchanged current system and inspect a result that identifies every covered rule and any failing rule.

**Acceptance Scenarios**:

1. **Given** the current system and its existing test execution mechanism are available, **When** the documented suite is run, **Then** it completes with a distinct result for every rule in the verified-rule matrix in this specification.
2. **Given** a verified rule's observed outcome differs from its recorded outcome, **When** the suite is run, **Then** the result identifies the rule ID, scenario, and legacy evidence that failed.
3. **Given** the suite is run, **When** it finishes, **Then** no production source, configuration, database schema, or stored data has been changed by the harness.

---

### User Story 2 - Verify guarded library workflows (Priority: P1)

As a maintainer, I can verify console-facing authorization, validation, lookup, hold, issue, return, renewal, deletion, and fine decisions through the system's public entry points, so that both permitted and rejected paths are protected before migration.

**Why this priority**: The verified guards define who may act and when library state may change.

**Independent Test**: Supply representative roles, inputs, and library states through public entry points and verify each documented allowed and rejected outcome without modifying production code.

**Acceptance Scenarios**:

1. **Given** each supported role, **When** it attempts a role-gated hold, information, fine, issue, return, or renewal action, **Then** the allowed roles and borrower-only paths match the verified rules.
2. **Given** invalid menu input, a missing borrower, a null book-selection list, no loans, a borrowed book, or an unconfirmed deletion, **When** the related public flow is invoked, **Then** the guarded action does not proceed.
3. **Given** valid prerequisites for a hold, issue, return, renewal, deletion, or fine action, **When** the related public flow is invoked, **Then** the documented state transition and observable result occur.

---

### User Story 3 - Verify domain state and identity rules (Priority: P2)

As a maintainer, I can verify the identity, collection, queue, role-number, login, search, and fine rules that underpin the console flows, so that migration work does not silently change their semantics.

**Why this priority**: These rules make the higher-level flows repeatable and expose the state transitions that future implementation must preserve.

**Independent Test**: Construct the documented entities and invoke their public behavior to observe IDs, credentials, collections, queue order, role constraints, search results, login results, and fine outcomes.

**Acceptance Scenarios**:

1. **Given** automatic and explicit identity or role-number inputs, **When** Persons, Clerks, and Librarians are created, **Then** assignment and increment behavior matches the verified rules.
2. **Given** loans and hold requests, **When** they are added or removed through public behavior, **Then** borrower collections and the global hold queue reflect the documented order and membership.
3. **Given** supplied credentials, search terms, fine status, dates, and confirmation input, **When** the relevant public behavior is invoked, **Then** the documented login, exact-match search, fine, renewal, and output behavior occurs.

### Edge Cases

- Menu input containing letters or a numeric value equal to either exclusive bound is rejected; only a numeric value strictly between the supplied bounds is accepted.
- Login is rejected for a nonmatching ID/password pair, including when no person matches and the librarian credentials also do not match.
- A borrower with no loans cannot progress through return or renewal; a returned/paid fine is not recomputed or charged.
- A book being borrowed cannot be deleted. A book with hold requests is retained when deletion confirmation is declined; confirmed deletion removes the related borrower associations as well.
- A borrower cannot create a hold for another borrower; staff may do so only after the intended borrower is found.
- A second librarian is rejected; automatic identity, desk, and office numbering retain their documented sequential behavior.
- No database fixture, schema mutation, startup/shutdown persistence assertion, or persistence round trip is part of this feature; those are reserved for `specs/002-persistence-semantics-spec`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The deliverable MUST be an executable acceptance suite for the unchanged current system and MUST include one documented command or procedure that runs the complete suite.
- **FR-002**: The deliverable MUST trace all 54 verified rules in the matrix below, with a stable rule ID, test name or test-case label where executable, expected observable outcome, and the cited legacy evidence for each rule.
- **FR-003**: Each test MUST exercise the behavior through a public entry point of `Main`, `Library`, `Loan`, `Borrower`, `Book`, `Person`, `Staff`, `Librarian`, `Clerk`, `HoldRequest`, or `HoldRequestOperations`; it MUST not alter production code or use non-public behavior to force the asserted outcome.
- **FR-004**: For every verified validation, confirmation, authorization, lookup, or availability guard, the suite MUST cover both the path that proceeds and the path that is rejected or does not proceed when that distinction is evidenced.
- **FR-005**: The suite MUST characterize `Main` menu bounds, administrative password access, application configuration values, role-gated actions, borrower/list prerequisites, and observable console outcomes supported by the verified evidence.
- **FR-006**: The suite MUST characterize `Library` singleton, login, exact-match search, typed borrower/clerk lookup, book deletion, related hold cleanup, and loan-availability behavior supported by the verified evidence.
- **FR-007**: The suite MUST characterize `Borrower` confirmation-gated updates and borrowed/on-hold collection additions and removals.
- **FR-008**: The suite MUST characterize `Loan` overdue-fine calculation, paid/unpaid confirmation outcomes, no-fine behavior, and renewal-date replacement.
- **FR-009**: The suite MUST characterize `Person`, `Clerk`, and `Librarian` automatic-versus-supplied numbering, counter advancement, default credentials where verified, the single-librarian constraint, and `Staff`'s documented printed augmentation.
- **FR-010**: The suite MUST characterize `HoldRequestOperations` first-in/oldest-out queue behavior and the public `HoldRequest` associations needed to observe it.
- **FR-011**: The suite MUST use isolated test cases so one case's singleton, collection, counter, console input/output, or clock-dependent state cannot change the expected result of another case.
- **FR-012**: The suite MUST report failures with the rule ID, scenario input or state, expected result, actual result, and legacy evidence reference.
- **FR-013**: The suite MUST preserve the current system under test: it MUST NOT modify production source, introduce Go code, refactor behavior, create or change database structures, change stored records, or introduce infrastructure or external-service work.
- **FR-014**: The suite MUST keep persistence behavior out of its executable scope. Assertions about startup/shutdown state synchronization, identity continuation after loading persisted data, and nullable persisted loan fields belong only to `specs/002-persistence-semantics-spec`.
- **FR-015**: Exact console text and line breaks MUST be asserted only where the frozen legacy evidence provides the required transcript; the harness MUST not invent undocumented prompts or messages.

### Verified-rule coverage matrix

The matrix is the required one-to-one traceability basis. “Evidence” is a verbatim substring recorded in `../../old/docs/brd.md`; the cited file identifies the legacy component. The eventual suite may group compatible rows into table-driven cases, but it must retain each row's rule ID in its result.

| Rule ID | Component | Required observable rule | Legacy evidence |
| --- | --- | --- | --- |
| R01 | Main | Menu input is numeric and strictly between the bounds. | `if((!choice.matches(".*[a-zA-Z]+.*")) && (Integer.parseInt(choice) > min && Integer.parseInt(choice) < max))` |
| R02 | Main | Only Admin password `lib` grants administrative access. | `if(aPass.equals("lib"))` |
| R03 | Main | Fine per unit initializes to 20. | `lib.setFine(20);` |
| R04 | Main | Hold-request expiry initializes to 7 days. | `lib.setRequestExpiry(7);` |
| R05 | Main | Book return deadline initializes to 5 days. | `lib.setReturnDeadline(5);` |
| R06 | Main | Library name initializes to FAST Library. | `lib.setName("FAST Library");` |
| R07 | Main | Startup populates in-memory state from its connection. | `lib.populateLibrary(con);` — deferred by FR-014 |
| R08 | Main | Shutdown writes current records back. | `lib.fillItBack(con);` — deferred by FR-014 |
| R09 | Main | Clerk/Librarian may place a hold for a found borrower. | `"Clerk".equals(person.getClass().getSimpleName()) || "Librarian".equals(person.getClass().getSimpleName())` |
| R10 | Main | Borrower places a hold only for self. | `b.makeHoldRequest((Borrower)person);` |
| R11 | Main | Only Clerk/Librarian views another borrower's information. | `"Clerk".equals(person.getClass().getSimpleName()) || "Librarian".equals(person.getClass().getSimpleName())` |
| R12 | Main | Only Clerk/Librarian computes arbitrary borrowers' fines; a borrower sees own fine. | `"Clerk".equals(person.getClass().getSimpleName()) || "Librarian".equals(person.getClass().getSimpleName())` |
| R13 | Main | Only staff issues a book to a borrower. | `b.issueBook(bor, (Staff)person);` |
| R14 | Main | Only staff processes a return. | `l.getBook().returnBook(bor, l, (Staff)person);` |
| R15 | Main | Only staff renews a loan. | `loans.get(input).renewIssuedBook(new java.util.Date());` |
| R16 | Main | Borrower-dependent operations proceed only after a successful lookup. | `if (bor != null)` |
| R17 | Main | List selection proceeds only for a non-null book list. | `if (books != null)` |
| R18 | Library | `Library` is a lazily created singleton. | `if(obj==null)` |
| R19 | Library | A currently borrowed book is not deleted. | `if (borBooks.get(j).getBook() == b)` |
| R20 | Library | A deletion with holds needs confirmation; declining cancels it. | `if(!hRequests.isEmpty())` |
| R21 | Library | Confirmed deletion removes relevant book and borrower hold associations. | `hr.getBorrower().removeHoldRequest(hr);` |
| R22 | Library | Login accepts matching person credentials. | `persons.get(i).getID() == id && persons.get(i).getPassword().equals(password)` |
| R23 | Library | If no person matches, librarian credentials are checked separately. | `librarian.getID() == id && librarian.getPassword().equals(password)` |
| R24 | Library | Search uses equality for selected title, subject, or author. | `if (b.getTitle().equals(title))` |
| R25 | Library | Borrower/clerk lookup matches the requested runtime class. | `persons.get(i).getClass().getSimpleName().equals("Borrower")` |
| R26 | Library | Loading persisted state sets counters to continue after highest IDs. | `Book.setIDCount(maxID)` — deferred by FR-014 |
| R27 | Library | An unreturned persisted loan has null receiver and return date. | `stmt.setNull(6,Types.INTEGER);` — deferred by FR-014 |
| R28 | Library | Return/renew proceeds only when borrower loans are nonempty. | `if (!loans.isEmpty())` |
| R29 | Borrower | Name update requires `y`. | `if(choice.equals("y"))` |
| R30 | Borrower | Address update requires `y`. | `if(choice.equals("y"))` |
| R31 | Borrower | Phone update requires `y`. | `if(choice.equals("y"))` |
| R32 | Borrower | Adding a borrowed book adds its Loan. | `borrowedBooks.add(iBook);` |
| R33 | Borrower | Removing a borrowed book removes its Loan. | `borrowedBooks.remove(iBook);` |
| R34 | Borrower | Adding a hold request adds it to `onHoldBooks`. | `onHoldBooks.add(hr);` |
| R35 | Borrower | Removing a hold request removes it from `onHoldBooks`. | `onHoldBooks.remove(hr);` |
| R36 | Loan | Positive overdue days multiply by the per-day fine; nonpositive days produce zero. | `totalFine = days * Library.getInstance().per_day_fine;` |
| R37 | Loan | Fine computes only while not paid. | `if (!finePaid)` |
| R38 | Loan | `y` or `Y` marks fine paid. | `choice.equals("y") || choice.equals("Y")` |
| R39 | Loan | `n` or `N` leaves fine unpaid. | `choice.equals("n") || choice.equals("N")` |
| R40 | Loan | No generated fine marks the fine paid. | `finePaid = true;` |
| R41 | Loan | Renewal replaces issued date with the supplied date. | `issuedDate = iDate;` |
| R42 | Loan | A paid fine is not computed or charged. | `if (!finePaid)` |
| R43 | Librarian | `-1` selects the next office number; supplied number is used otherwise. | `if (of == -1)` |
| R44 | Librarian | Constructing a librarian advances office numbering. | `currentOfficeNumber++;` |
| R45 | Librarian | A second librarian is rejected. | `if (librarian == null) {` |
| R46 | Person | `-1` selects the next ID; supplied ID is used otherwise. | `if(idNum==-1)` |
| R47 | Person | Default password is the ID string. | `password = Integer.toString(id);` |
| R48 | Person | Current ID counter can be set explicitly. | `public static void setIDCount(int n)` |
| R49 | Clerk | `-1` selects the next desk number; supplied number is used otherwise. | `if(dk == -1)` |
| R50 | Clerk | Constructing a clerk advances desk numbering. | `currentdeskNumber++;` |
| R51 | HoldRequestOperations | New global hold requests append to the end. | `holdRequests.add(hr);` |
| R52 | HoldRequestOperations | Removing a global hold request removes the oldest. | `holdRequests.remove(0);` |
| R53 | Book | Construction advances the documented global ID counter. | `currentIdNumber++;` |
| R54 | Staff | Printed staff information includes inherited person output and salary. | `super.printInfo();` |

**Legacy sources**: `../../old/docs/brd.md` is the rule-and-evidence source; `../../old/docs/lld.md` supplies the public symbols and observable state changes; `../../old/docs/roadmap.md` defines this feature's directory, components, and boundaries. R07, R08, R26, and R27 remain traceable in this harness matrix but are deliberately non-executable until specification 002, because their test requires persistence state and is outside this feature's stated boundary.

### Key Entities

- **Acceptance case**: One isolated, executable characterization of a verified rule, carrying its rule ID, setup, public action, observable expected result, and evidence reference.
- **Rule result**: The pass/fail outcome for an acceptance case, including enough input/state detail to diagnose a discrepancy.
- **Library state**: The observable in-memory people, librarian, books, loans, borrowed-book associations, and hold-request associations used by front-end and back-end rules.
- **Actor**: Admin, Borrower, Clerk, Librarian, or Staff context supplied to role-gated public flows.
- **Hold request and loan**: Existing domain relationships used to observe queue order, borrower associations, issue/return availability, renewal, and fines; no persistent representation is in scope.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A single documented invocation completes the acceptance suite and emits a result for all 54 matrix rule IDs; the four persistence-deferred IDs are visibly reported as deferred to specification 002, not passed without execution.
- **SC-002**: Every executable rule result identifies exactly one matrix rule ID and links to its legacy evidence; 0 executable results lack a rule-to-evidence mapping.
- **SC-003**: For every executable guarded rule, the suite contains at least one proceeding and one rejected/non-proceeding case where the verified evidence distinguishes them.
- **SC-004**: Running the suite leaves production source, production configuration, database schema, and stored records unchanged in 100% of runs.
- **SC-005**: A maintainer can locate the expected outcome and evidence for any reported failure from the suite output and matrix without inspecting undocumented behavior.

## Assumptions

- The current Java system remains the behavioral subject; this feature creates characterization tests only and does not begin the Go migration.
- The existing estate's supported test execution mechanism will be used or documented by the implementation plan; this specification does not select a test framework or add a dependency.
- Tests may provide console input and observe console output only through existing public flows. Exact prompt transcript assertions are restricted to text available from the frozen evidence.
- The frozen documents are the sole evidence base in this workspace. They identify 54 verified rules but no execution-grounded baseline; the harness is intended to establish that baseline.
- Database and infrastructure are excluded. Persisted-state behaviors are intentionally deferred to `specs/002-persistence-semantics-spec`, even though the four associated verified rules are retained for traceability.
- The specified front-end and back-end components are the complete component set for this feature. No additional component, external service, schema, migration, or refactoring is implied.

## Scope Boundaries

**In scope**: An executable acceptance harness and its rule-to-test evidence mapping for the current system's front-end and back-end behavior, limited to `Main`, `Library`, `Loan`, `Borrower`, `Book`, `Person`, `Staff`, `Librarian`, `Clerk`, `HoldRequest`, and `HoldRequestOperations`.

**Out of scope**: Go code; production-code modification; refactoring; Java behavior changes; persistence/schema analysis or rework; database fixtures or mutations; infrastructure; deployment; and the later roadmap specifications. Persistence assertions listed as R07, R08, R26, and R27 are explicitly deferred, rather than expanded into this feature.
