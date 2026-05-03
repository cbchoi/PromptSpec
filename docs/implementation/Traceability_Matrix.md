# Requirement Traceability Matrix

This matrix maps SRS requirements to implementation milestones, first task
coverage, and expected verification.

| Requirement | Milestone | Primary Tasks | Verification |
|---|---|---|---|
| F1.1 | M2 | M2.T2 | Unit tests for slot registry CRUD |
| F1.2 | M1 | M1.T2 | Model validation tests |
| F1.3 | M2 | M2.T3, M2.T4 | Import/export unit tests |
| F2.1 | M2 | M2.T5 | Resolver inheritance tests |
| F2.2 | M2 | M2.T6 | Resolver override tests |
| F2.3 | M2 | M2.T7 | Condition evaluator tests |
| F2.4 | M2 | M2.T8 | Conflict priority tests |
| F3.1 | M2 | M2.T9 | Renderer tests |
| F3.2 | M1, M2 | M1.T4, M2.T10 | Span model and renderer tests |
| F3.3 | M6 | M6.T8 | Playwright prompt studio test |
| F4.1 | M4, M5 | M4.T11, M5.T1 | Settings API and mocked LLM tests |
| F4.2 | M1, M5 | M1.T5, M5.T5 | MeaningReport model and inspector tests |
| F4.3 | M1, M5 | M1.T5, M5.T5 | Uncertainty mapping tests |
| F5.1 | M2 | M2.T11 | Missing-slot validator tests |
| F5.2 | M2 | M2.T12 | Semantic conflict validator tests |
| F5.3 | M2 | M2.T13 | Over-generation validator tests |
| F5.4 | M2 | M2.T14 | Ambiguity validator tests |
| F5.5 | M2, M5 | M2.T15, M5.T5 | Fidelity validation scenario tests |
| F6.1 | M3, M7 | M3.T1, M7.T2 | Test case schema and UI tests |
| F6.2 | M3 | M3.T4-M3.T7 | Harness suite runner tests |
| F6.3 | M3 | M3.T8 | Meaning comparator tests |
| F6.4 | M1, M3 | M1.T7, M3.T9 | TestReport model and writer tests |
| F7.1 | M7 | M7.T7 | Agent Trace UI tests |
| F7.2 | M1, M5 | M1.T9, M5.T4 | Schema export and inspector validation tests |
| F7.3 | M5, M7 | M5.T7, M7.T8-M7.T10 | Trace log and UI tests |
| F8.1 | M6, M9 | M6.T1, M9.T2 | Web and desktop smoke tests |
| F8.2 | M4 | M4.T1-M4.T3 | API integration tests |
| F8.3 | M4, M5, M9 | M4.T10, M4.T11, M5.T1, M9.T6 | Settings API and desktop settings tests |
| F9.1 | M8 | M8.T1, M8.T2 | Ralph task generator tests |
| F9.2 | M1, M8 | M1.T8, M8.T9 | RalphTask model and task validation tests |
| F9.3 | M8 | M8.T4, M8.T11 | Progress update tests |
| F9.4 | M8 | M8.T12 | Failure report writer tests |
| F9.5 | M8 | M8.T10, M8.T11 | Ralph check acceptance tests |
| F9.6 | M8 | M8.T10, M8.T11 | Completion gate tests |

## Coverage Rule

Every implementation PR must identify the affected SRS IDs and the tests that
verify them. Documentation-only work may use `docs-check` as its verification.

