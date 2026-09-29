## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Constitution Alignment | CRITICAL | `.specify/memory/constitution.md:IV, Development Workflow`; `spec.md:70, 169-174`; `plan.md:13-19, 37-40`; `tasks.md:12-14` | The constitution requires Go tests runnable with `go test` for every implemented or preserved behaviour, table-driven coverage where alternatives exist, and a Go 1.22 implementation. This feature explicitly forbids Go code and plans a Java-only `javac`/`java` harness. The plan calls this a “justified feature exception,” but the constitution contains no such exception and says its rules govern all specifications, plans, and tasks. | Before implementation, either amend the constitution through its explicit governance workflow to allow this Java-only pre-migration characterization harness, or revise the governing requirements/artifacts so the conflict no longer exists. Do not rely on the plan’s unsupported exception. |
| I1 | Inconsistency | HIGH | `spec.md:161-164`; `tasks.md:45, 47, 90-93` | SC-001 requires results for all 54 IDs with only R07/R08/R26/R27 deferred, and T023 requires every other ID to be `PASS`. T008, however, permits R01-R06 to be reported `BLOCKED` if a configuration path is not safely reachable. This creates an additional status outcome that neither the success criterion nor final validation permits. | Decide and document one outcome: define a safe public route that makes R01-R06 executable and require `PASS`, or explicitly allow and define `BLOCKED` in the success criteria and final acceptance conditions. |
| G1 | Coverage Gap | HIGH | `spec.md:22, 82-84, 163`; `tasks.md:20, 34-35, 90-93` | FR-013 and SC-004 require every run to leave production source, configuration, schema, and stored records unchanged. The only explicit integrity task, T021, hashes scoped source input; it does not substantiate unchanged configuration, schema, or stored records. T006/T007 prevent known write targets, but do not provide a complete verification mechanism for the promised result. | Specify a non-mutating integrity strategy that covers every in-scope legacy input class, or narrow the requirement to guarantees the harness can establish without planning database work. Retain the prohibition on opening/mutating persistence paths. |
| A1 | Ambiguity | MEDIUM | `spec.md:70-73, 169-172`; `plan.md:13-21, 69`; `tasks.md:20, 34` | The specification delegates the existing Java execution mechanism to implementation, while the plan selects a JDK-only compilation model and an absolute `Project` directory argument. It does not state the supported JDK version, compilation classpath/source layout contract, or how the runner distinguishes a legitimate subject-build prerequisite failure from a rule failure. | Make the runner input/build contract explicit in the specification or plan, including the supported layout, JDK compatibility, allowed classpath inputs, and result status for environmental prerequisites. |
| D1 | Duplication | LOW | `spec.md:128, 133`; `tasks.md:77` | R37 (“Fine computes only while not paid”) and R42 (“A paid fine is not computed or charged”) use the same guard evidence and describe overlapping paid-fine behaviour. They must remain separately traceable because the matrix assigns both IDs, but separate independent implementations would duplicate the same assertion. | Implement one table-driven paid/unpaid case family that emits distinct R37 and R42 results and clearly records the differing observable assertions. |

### Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 | Yes | T001, T006, T007, T020, T023 | Single command and full-suite execution. |
| FR-002 | Yes | T004, T006, T009, T022 | Registry and all-rule traceability. |
| FR-003 | Yes | T005, T008, T011-T019 | Case families state public-entry-point use. |
| FR-004 | Yes | T008, T011, T012, T015-T017 | Permitted/rejected paths are assigned by rule family. |
| FR-005 | Yes | T008, T010 | `Main` baseline/configuration dispatch. |
| FR-006 | Yes | T012, T014, T019 | `Library` workflow and state cases. |
| FR-007 | Yes | T015, T019 | `Borrower` confirmation and associations. |
| FR-008 | Yes | T016, T019 | `Loan` fine and renewal cases. |
| FR-009 | Yes | T017, T019 | Identity, role numbering, and staff output. |
| FR-010 | Yes | T018, T019 | Hold queue and association cases. |
| FR-011 | Yes | T005, T006 | Fresh-JVM isolation and process orchestration. |
| FR-012 | Yes | T003, T005, T006, T009 | Structured diagnostic result contract. |
| FR-013 | Yes | T001, T002, T006, T007, T021, T023 | Coverage exists, but G1 identifies incomplete integrity verification. |
| FR-014 | Yes | T004, T006, T010, T022 | Four named persistence deferrals. |
| FR-015 | Yes | T004, T017, T019 | Evidence catalog and transcript limitation. |
| SC-001 | Yes | T006, T009, T010, T020, T022, T023 | Inconsistent with T008 `BLOCKED` allowance (I1). |
| SC-002 | Yes | T003, T004, T006, T009, T022 | Rule-to-evidence result fields. |
| SC-003 | Yes | T008, T011, T012, T015-T017 | Guard-path coverage is assigned. |
| SC-004 | Yes | T001, T006, T007, T021, T023 | Incomplete source/configuration/data integrity verification (G1). |
| SC-005 | Yes | T003, T006, T009, T020 | Diagnostic and maintainer guidance coverage. |

### Constitution Alignment Issues

- C1 is a blocking conflict: the Java-only, no-Go-code deliverable does not meet the constitution’s mandatory Go-test workflow. The constitution must be amended explicitly, or the artifacts must be reconciled, before `/speckit-implement`.

### Unmapped Tasks

None. Setup, runner, case-family, validation, and documentation tasks each map to at least one functional requirement, success criterion, or user story.

### Metrics

- Total Requirements: 20 (15 functional requirements and 5 buildable success criteria)
- Total Tasks: 23
- Coverage: 100% (20 of 20 requirements have at least one mapped task)
- Ambiguity Count: 1
- Duplication Count: 1
- Critical Issues Count: 1

### Next Actions

- Resolve C1 before `/speckit-implement`; the current plan cannot authorize an exception to the constitution.
- Reconcile the R01-R06 status contract (I1) and make the no-change verification supportable (G1).
- Run `/speckit-plan` after the constitution decision and contract refinements, then regenerate `/speckit-tasks` if task changes are needed.

Would you like me to suggest concrete remediation edits for the top 3 issues?
