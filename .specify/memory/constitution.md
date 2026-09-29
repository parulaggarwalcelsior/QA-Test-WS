<!--
Sync Impact Report
- Version change: none → 1.0.0
- Modified principles: none (initial adoption)
- Added sections: Core Principles; Scope and Technology Constraints; Development Workflow;
  Governance
- Removed sections: none
- Follow-up TODOs: Resolved: the console prompts and messages printed by Project/src/LMS/*.java at commit 798ee338 are the authoritative transcripts; exact text and line breaks must match.
-->
# Library Management System Go Migration Constitution

## Core Principles

### I. Evidence-Grounded Behavioural Parity
The Go 1.22 implementation MUST preserve behaviours evidenced in `../../old/docs/` and MUST
not invent behaviours merely because they would suit a library system or the migration goal.
Requirements, rules, symbols, and evidence MUST retain the legacy estate's terminology where
they are described. A change MUST be traceable to the frozen documentation or to an earlier
workspace artifact. This prevents the migration from silently changing the system it ports.

### II. Console Interface Is a Public Contract
All observable console menus, prompts, validation responses, and messages of the Library
Management System MUST be preserved by the front end. Input bounds, role-gated flows, and
confirmation semantics MUST match the documented legacy behaviour. Console I/O MUST remain
separable enough from back-end rules for automated verification. This protects users and
scripts that rely on the current interaction contract.

### III. Go 1.22 Front-End and Back-End Boundary
Production work MUST target Go 1.22 and remain within the front-end console layer and the
back-end application/domain layer. Database files, database schema, infrastructure, and
deployment work are out of scope and MUST NOT be created, modified, or planned as part of
this migration. No new external service or dependency on one may be introduced. This keeps
the work aligned with the declared `java to go` scope without expanding the estate.

### IV. Behavioural Tests Are Mandatory
Every implemented or preserved behaviour MUST have a Go test runnable with `go test`.
Tests MUST use table-driven cases where multiple inputs, roles, states, or outcomes express
the behaviour. Tests MUST cover both permitted and rejected paths when the documented rule
contains a guard, validation, confirmation, or authorization boundary. This makes parity
measurable instead of assumed.

### V. Small, Reviewable, Parity-Safe Changes
Each change MUST be narrow, independently reviewable, and accompanied by the tests needed to
demonstrate the affected legacy behaviour. Refactoring is permitted only when it preserves the
observable console contract and documented back-end results. Changes MUST avoid unrelated
cleanup, database alterations, and speculative enhancements. This limits translation risk and
makes discrepancies easy to isolate.

## Scope and Technology Constraints

The system being ported is the console-driven Library Management System described by the
frozen legacy documentation in `../../old/docs/`. The source estate is Java; the target is Go
1.22. Work begins from that documentation and from artifacts produced in this workspace, not
from unrelated repositories or assumptions about typical library software.

The allowed layers are front end and back end. Existing database files are read-only for this
work unit. Database and infrastructure behaviour may be described only when needed to state a
front-end or back-end boundary; it MUST NOT result in a database or infrastructure change.

Resolved: the console prompts and messages printed by Project/src/LMS/*.java at commit 798ee338 are the authoritative transcripts; exact text and line breaks must match.

## Development Workflow

Work MUST proceed spec-first: create or update a specification, then a plan, then ordered
tasks, and only then implementation. Each artifact MUST identify the legacy evidence and the
front-end/back-end boundary it relies on. Implementations MUST include table-driven Go tests
for every behaviour they add or preserve, and `go test` MUST pass before the work is presented
for review.

When documentation leaves a material behaviour ambiguous and no answer is available, the
relevant artifact MUST contain a `[NEEDS CLARIFICATION: question]` marker. Such a marker does
not authorize guessed behaviour or a database/infrastructure change.

## Governance

This constitution governs all migration specifications, plans, tasks, and implementations in
this workspace. Amendments MUST document the affected principles, rationale, and any required
updates to dependent artifacts. A backward-incompatible removal or redefinition of a principle
requires a MAJOR version bump; a new principle or material expansion requires a MINOR bump;
and a clarification or non-semantic refinement requires a PATCH bump.

Every review MUST verify the Go 1.22 target, front-end/back-end-only scope, preservation of
observable console behaviour, absence of database-file changes and new external services, and
table-driven `go test` coverage for each behaviour. A conflict with this constitution MUST be
resolved by amending the constitution before implementation proceeds.

**Version**: 1.0.0 | **Ratified**: 2026-09-29 | **Last Amended**: 2026-09-29
