# API Specification - FastAPI

All request and response bodies use the canonical schemas in `Data_Model.md`.
Errors return:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable summary",
    "details": {}
  }
}
```

## POST /api/prompts/resolve
Resolve active slots.

Request: `PromptSpec`

Response: resolved `PromptSpec`

## POST /api/prompts/render
Render PromptSpec into prompt text and span metadata.

Request: resolved `PromptSpec`

Response: `RenderedPrompt`

## POST /api/prompts/inspect
Inspect rendered prompt using local LLM.

Request: `RenderedPrompt`

Response: `MeaningReport`

## POST /api/prompts/validate
Validate PromptSpec, RenderedPrompt, and MeaningReport.

Request:

```json
{
  "prompt_spec": {},
  "rendered_prompt": {},
  "meaning_report": {}
}
```

Response: `ValidationReport`

## POST /api/tests/run
Run test suite.

Request:

```json
{
  "suite": "unit|integration|scenario|regression|e2e|ralph",
  "test_ids": []
}
```

Response: `TestReport`

## POST /api/ralph/check
Run Ralph-specific task acceptance check.

Request:

```json
{
  "task_id": "T001"
}
```

Response: `TestReport`

## GET /api/ralph/status
Return task/progress status.

Response:

```json
{
  "tasks": [],
  "progress": {
    "completed": [],
    "in_progress": [],
    "blocked": [],
    "last_failure": null
  }
}
```

## GET /api/tests/report/{report_id}
Return test report.

Response: `TestReport`

## GET /api/settings
Return app settings.

Response:

```json
{
  "local_llm_endpoint": "http://localhost:11434",
  "storage_path": ".promptspec/app.sqlite"
}
```

## PUT /api/settings
Update app settings.

Request: same shape as `GET /api/settings`

Response: updated settings

## Status Codes
- `200`: success
- `400`: invalid request body or unsupported option
- `404`: report or task not found
- `422`: schema validation failed
- `500`: unexpected server error
