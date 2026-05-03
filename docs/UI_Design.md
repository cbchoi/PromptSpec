# UI Design Document

## 1. Main Layout

```text
┌──────────────────────┬──────────────────────┐
│ Slot Table            │ Rendered Prompt       │
│ color-coded slots     │ color-coded spans     │
├──────────────────────┼──────────────────────┤
│ Meaning Report        │ Validation / Test     │
│ schema JSON + summary │ diff + pass/fail      │
└──────────────────────┴──────────────────────┘
```

## 2. Main Screens
- Prompt Studio
- Test Lab
- Agent Trace
- Ralph Loop Dashboard
- Settings

## 3. Ralph Loop Dashboard
- Current task
- Acceptance criteria
- Required tests
- Last iteration result
- Current progress
- Failing reports
- Completed task history
- Git commit status

## 4. Color Coding
- role: identity
- task: action
- constraint: rule
- forbidden: hard restriction
- output_format: output contract
- evidence_rule: factuality
- strategy: behavior

## 5. Interaction
- Click slot → highlight rendered prompt span
- Click rendered sentence → trace source slot
- Click validation issue → show offending slot/rendered span
- Click inheritance node → show inherited/overridden slots
- Click Ralph task → show source requirement, test, implementation note
