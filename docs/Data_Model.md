# Data Model Specification

This document is the source of truth for machine-facing data contracts. API,
engine, harness, and agent documents must refer to these types instead of
redefining them.

## PromptSlot

```json
{
  "key": "audience",
  "type": "role|task|constraint|forbidden|output_format|evidence_rule|strategy|context",
  "value": "Write for senior backend engineers.",
  "condition": null,
  "priority": 100,
  "source": "user|parent|import|system",
  "version": 1,
  "required": true
}
```

Rules:
- `key` is unique within a `PromptSpec`.
- Higher `priority` wins when two active slots conflict.
- `condition` is either `null` or a deterministic expression evaluated by the resolver.
- `value` is treated as source meaning; renderers must not add unsupported meaning.

## PromptSpec

```json
{
  "id": "spec_001",
  "title": "Technical report prompt",
  "parent_id": null,
  "slots": [],
  "strategy": {
    "render_strategy": "technical_report",
    "validation_strategy": "strict_source_based",
    "inspection_strategy": "schema_bound_local_llm"
  },
  "metadata": {}
}
```

## RenderedPrompt

```json
{
  "spec_id": "spec_001",
  "text": "Write a technical report for senior backend engineers.",
  "spans": [
    {
      "slot_key": "audience",
      "start": 29,
      "end": 54,
      "text": "senior backend engineers"
    }
  ]
}
```

## MeaningReport

```json
{
  "spec_id": "spec_001",
  "schema_version": 1,
  "meaning": {},
  "uncertainties": [],
  "raw_model": null
}
```

Rules:
- Agent-facing reports must be valid JSON.
- `raw_model` may be omitted from UI responses, but must be available in trace logs when an LLM was used.
- Uncertain interpretations must be reported in `uncertainties` instead of free-form prose.

## ValidationReport

```json
{
  "spec_id": "spec_001",
  "status": "pass|fail",
  "issues": [
    {
      "code": "MISSING_SLOT",
      "severity": "info|warning|critical",
      "slot_key": "audience",
      "message": "Required slot was not represented in rendered prompt."
    }
  ],
  "metrics": {
    "slot_coverage": 1.0,
    "conflict_count": 0,
    "critical_over_generation": 0,
    "meaning_schema_valid": true
  }
}
```

## TestReport

```json
{
  "report_id": "report_001",
  "suite": "unit|integration|scenario|regression|e2e|ralph",
  "status": "pass|fail",
  "commands": [],
  "artifacts": []
}
```

## RalphTask

```json
{
  "id": "T001",
  "title": "Implement PromptSlot model",
  "status": "pending|in_progress|completed|blocked",
  "source_doc": "SRS.md",
  "acceptance_criteria": [],
  "test_commands": [],
  "dependencies": []
}
```

Completion rule:
- A task can move to `completed` only after all `test_commands` pass and the acceptance gate records evidence.
