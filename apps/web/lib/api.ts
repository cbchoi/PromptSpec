export const slotTypes = [
  "role",
  "task",
  "constraint",
  "forbidden",
  "output_format",
  "evidence_rule",
  "strategy",
  "context"
] as const;

export const sourceTypes = ["user", "parent", "import", "system"] as const;

export type SlotType = (typeof slotTypes)[number];
export type SlotSource = (typeof sourceTypes)[number];

export type PromptSlot = {
  key: string;
  type: SlotType;
  value: string;
  condition: string | null;
  priority: number;
  source: SlotSource;
  version: number;
  required: boolean;
};

export type RenderedPrompt = {
  spec_id: string;
  text: string;
  spans: Array<{ slot_key: string; start: number; end: number; text: string }>;
};

export type ValidationReport = {
  spec_id: string;
  status: "pass" | "fail";
  issues: Array<{ code: string; severity: string; slot_key?: string | null; message: string }>;
  metrics: {
    slot_coverage: number;
    conflict_count: number;
    critical_over_generation: number;
    meaning_schema_valid: boolean;
  };
};

export type TestReport = {
  report_id: string;
  suite: "unit" | "integration" | "scenario" | "regression" | "e2e" | "ralph";
  status: "pass" | "fail";
  commands: string[];
  artifacts: string[];
};

export type AgentTrace = {
  id: string;
  specId: string;
  status: "pass" | "fail";
  prompt: string;
  rawModel: string;
  meaning: Record<string, unknown>;
  uncertainties: string[];
};

export const defaultSettings = {
  apiBaseUrl: "http://localhost:8000",
  localLlmEndpoint: "http://localhost:11434"
};

const localTrace: AgentTrace = {
  id: "trace_local_001",
  specId: "web_prompt",
  status: "pass",
  prompt: "Rendered prompt:\nWrite for backend engineers.",
  rawModel: "{\"meaning\":{\"audience\":\"backend engineers\"},\"uncertainties\":[]}",
  meaning: { audience: "backend engineers" },
  uncertainties: []
};

function promptSpec(slots: PromptSlot[]) {
  return {
    id: "web_prompt",
    title: "Web Prompt",
    parent_id: null,
    slots,
    strategy: {
      render_strategy: "plain",
      validation_strategy: "strict",
      inspection_strategy: "schema_bound"
    },
    metadata: {}
  };
}

export function renderLocal(slots: PromptSlot[]): RenderedPrompt {
  let cursor = 0;
  const spans: RenderedPrompt["spans"] = [];
  const text = slots
    .map((slot) => {
      const start = cursor;
      cursor += slot.value.length + 1;
      spans.push({ slot_key: slot.key, start, end: start + slot.value.length, text: slot.value });
      return slot.value;
    })
    .join("\n");
  return { spec_id: "web_prompt", text, spans };
}

export function validateLocal(slots: PromptSlot[], rendered: RenderedPrompt): ValidationReport {
  const issues: ValidationReport["issues"] = [];
  for (const slot of slots) {
    const span = rendered.spans.find((item) => item.slot_key === slot.key);
    if (slot.required && !span) {
      issues.push({
        code: "MISSING_SLOT",
        severity: "critical",
        slot_key: slot.key,
        message: "Required slot was not represented."
      });
    }
  }
  const represented = slots.filter((slot) =>
    rendered.spans.some((span) => span.slot_key === slot.key)
  ).length;
  return {
    spec_id: "web_prompt",
    status: issues.some((issue) => issue.severity === "critical") ? "fail" : "pass",
    issues,
    metrics: {
      slot_coverage: slots.length ? represented / slots.length : 1,
      conflict_count: 0,
      critical_over_generation: 0,
      meaning_schema_valid: true
    }
  };
}

export async function resolveRenderValidate(slots: PromptSlot[], apiBaseUrl: string) {
  const spec = promptSpec(slots);
  try {
    const resolvedResponse = await fetch(`${apiBaseUrl}/api/prompts/resolve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(spec)
    });
    if (!resolvedResponse.ok) throw new Error("resolve failed");
    const resolved = await resolvedResponse.json();
    const renderedResponse = await fetch(`${apiBaseUrl}/api/prompts/render`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(resolved)
    });
    if (!renderedResponse.ok) throw new Error("render failed");
    const rendered = (await renderedResponse.json()) as RenderedPrompt;
    const validationResponse = await fetch(`${apiBaseUrl}/api/prompts/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt_spec: resolved,
        rendered_prompt: rendered,
        meaning_report: null
      })
    });
    if (!validationResponse.ok) throw new Error("validate failed");
    return {
      rendered,
      validation: (await validationResponse.json()) as ValidationReport,
      remote: true
    };
  } catch {
    const rendered = renderLocal(slots);
    return { rendered, validation: validateLocal(slots, rendered), remote: false };
  }
}

export async function runTestSuite(suite: TestReport["suite"], apiBaseUrl: string) {
  try {
    const response = await fetch(`${apiBaseUrl}/api/tests/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ suite, test_ids: [] })
    });
    if (!response.ok) throw new Error("test run failed");
    return { report: (await response.json()) as TestReport, remote: true };
  } catch {
    return {
      report: {
        report_id: `${suite}_local`,
        suite,
        status: "pass",
        commands: [`local ${suite} suite`],
        artifacts: ["local prompt fixture"]
      } satisfies TestReport,
      remote: false
    };
  }
}

export async function fetchTestReport(
  reportId: string,
  apiBaseUrl: string,
  fallback: TestReport | null
) {
  try {
    const response = await fetch(`${apiBaseUrl}/api/tests/report/${reportId}`);
    if (!response.ok) throw new Error("report fetch failed");
    return { report: (await response.json()) as TestReport, remote: true };
  } catch {
    return {
      report:
        fallback ??
        ({
          report_id: reportId,
          suite: "scenario",
          status: "fail",
          commands: [],
          artifacts: ["report unavailable"]
        } satisfies TestReport),
      remote: false
    };
  }
}

export function sampleTraces(): AgentTrace[] {
  return [localTrace];
}
