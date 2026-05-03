"use client";

import {
  AlertTriangle,
  Beaker,
  CheckCircle2,
  Download,
  FileJson,
  GitBranch,
  Plus,
  RefreshCcw,
  Save,
  Settings,
  Trash2,
  Upload,
  Workflow
} from "lucide-react";
import { ChangeEvent, useMemo, useState } from "react";
import {
  AgentTrace,
  PromptSlot,
  RalphStatus,
  TestReport,
  ValidationReport,
  defaultSettings,
  fetchRalphStatus,
  fetchTestReport,
  renderLocal,
  resolveRenderValidate,
  runRalphCheck,
  runTestSuite,
  sampleTraces,
  slotTypes,
  sourceTypes
} from "../lib/api";

const initialSlots: PromptSlot[] = [
  {
    key: "audience",
    type: "role",
    value: "Write for backend engineers.",
    condition: null,
    priority: 100,
    source: "user",
    version: 1,
    required: true
  },
  {
    key: "task",
    type: "task",
    value: "Summarize the architecture decisions.",
    condition: null,
    priority: 90,
    source: "user",
    version: 1,
    required: true
  }
];

export default function PromptStudioPage() {
  const [activeView, setActiveView] = useState<"studio" | "tests" | "traces" | "ralph">("studio");
  const [slots, setSlots] = useState<PromptSlot[]>(initialSlots);
  const [selectedKey, setSelectedKey] = useState("audience");
  const [renderedText, setRenderedText] = useState("");
  const [validation, setValidation] = useState<ValidationReport | null>(null);
  const [settings, setSettings] = useState(defaultSettings);
  const [status, setStatus] = useState("Ready");
  const [suite, setSuite] = useState<TestReport["suite"]>("scenario");
  const [testReports, setTestReports] = useState<TestReport[]>([]);
  const [selectedReportId, setSelectedReportId] = useState("");
  const [selectedReport, setSelectedReport] = useState<TestReport | null>(null);
  const [traces] = useState<AgentTrace[]>(sampleTraces());
  const [selectedTraceId, setSelectedTraceId] = useState("trace_local_001");
  const [ralphStatus, setRalphStatus] = useState<RalphStatus | null>(null);
  const [selectedRalphTaskId, setSelectedRalphTaskId] = useState("M8.T10");
  const [ralphReport, setRalphReport] = useState<TestReport | null>(null);

  const rendered = useMemo(() => renderLocal(slots), [slots]);
  const selectedSlot = slots.find((slot) => slot.key === selectedKey) ?? slots[0];

  function updateSlot(index: number, patch: Partial<PromptSlot>) {
    setSlots((current) =>
      current.map((slot, slotIndex) => (slotIndex === index ? { ...slot, ...patch } : slot))
    );
  }

  function addSlot() {
    const nextIndex = slots.length + 1;
    const key = `slot_${nextIndex}`;
    setSlots((current) => [
      ...current,
      {
        key,
        type: "context",
        value: "New slot value.",
        condition: null,
        priority: 50,
        source: "user",
        version: 1,
        required: false
      }
    ]);
    setSelectedKey(key);
  }

  function deleteSlot(key: string) {
    setSlots((current) => current.filter((slot) => slot.key !== key));
    setSelectedKey(slots[0]?.key ?? "");
  }

  async function runPipeline() {
    setStatus("Running");
    const result = await resolveRenderValidate(slots, settings.apiBaseUrl);
    setRenderedText(result.rendered.text);
    setValidation(result.validation);
    setStatus(result.remote ? "API" : "Local");
  }

  async function runSuite() {
    setStatus("Testing");
    const result = await runTestSuite(suite, settings.apiBaseUrl);
    setTestReports((current) => [result.report, ...current.filter((item) => item.report_id !== result.report.report_id)]);
    setSelectedReport(result.report);
    setSelectedReportId(result.report.report_id);
    setStatus(result.remote ? "API" : "Local");
  }

  async function loadReport(reportId: string) {
    setSelectedReportId(reportId);
    const fallback = testReports.find((report) => report.report_id === reportId) ?? null;
    const result = await fetchTestReport(reportId, settings.apiBaseUrl, fallback);
    setSelectedReport(result.report);
    setStatus(result.remote ? "API" : "Local");
  }

  async function loadRalphStatus() {
    setStatus("Ralph");
    const result = await fetchRalphStatus(settings.apiBaseUrl);
    setRalphStatus(result.status);
    setSelectedRalphTaskId(result.status.tasks[0]?.id ?? "");
    setStatus(result.remote ? "API" : "Local");
  }

  async function checkRalphTask(taskId: string) {
    setSelectedRalphTaskId(taskId);
    const result = await runRalphCheck(taskId, settings.apiBaseUrl);
    setRalphReport(result.report);
    setStatus(result.remote ? "API" : "Local");
  }

  function exportJson() {
    const data = JSON.stringify(slots, null, 2);
    navigator.clipboard?.writeText(data).catch(() => undefined);
    setStatus("Exported");
  }

  function importJson(event: ChangeEvent<HTMLTextAreaElement>) {
    try {
      const parsed = JSON.parse(event.target.value) as PromptSlot[];
      if (Array.isArray(parsed)) {
        setSlots(parsed);
        setSelectedKey(parsed[0]?.key ?? "");
        setStatus("Imported");
      }
    } catch {
      setStatus("Invalid JSON");
    }
  }

  const visibleRenderedText = renderedText || rendered.text;

  return (
    <main className="studio-shell">
      <header className="topbar">
        <div>
          <h1>PromptSpec</h1>
          <p>Prompt Studio</p>
        </div>
        <nav className="tabs" aria-label="Main views">
          <button
            className={activeView === "studio" ? "tab active" : "tab"}
            type="button"
            onClick={() => setActiveView("studio")}
          >
            <FileJson size={16} />
            Studio
          </button>
          <button
            className={activeView === "tests" ? "tab active" : "tab"}
            type="button"
            onClick={() => setActiveView("tests")}
          >
            <Beaker size={16} />
            Test Lab
          </button>
          <button
            className={activeView === "traces" ? "tab active" : "tab"}
            type="button"
            onClick={() => setActiveView("traces")}
          >
            <Workflow size={16} />
            Trace
          </button>
          <button
            className={activeView === "ralph" ? "tab active" : "tab"}
            type="button"
            onClick={() => {
              setActiveView("ralph");
              void loadRalphStatus();
            }}
          >
            <GitBranch size={16} />
            Ralph
          </button>
        </nav>
        <div className="toolbar">
          <button type="button" onClick={addSlot} title="Add slot" aria-label="Add slot">
            <Plus size={18} />
          </button>
          <button type="button" onClick={runPipeline} title="Run pipeline" aria-label="Run pipeline">
            <RefreshCcw size={18} />
          </button>
          <button type="button" onClick={exportJson} title="Export JSON" aria-label="Export JSON">
            <Download size={18} />
          </button>
          <span className="status-pill">{status}</span>
        </div>
      </header>

      {activeView === "studio" ? (
        <StudioView
          deleteSlot={deleteSlot}
          importJson={importJson}
          selectedKey={selectedKey}
          selectedSlot={selectedSlot}
          setSelectedKey={setSelectedKey}
          setSettings={setSettings}
          settings={settings}
          slots={slots}
          updateSlot={updateSlot}
          validation={validation}
          visibleRenderedText={visibleRenderedText}
        />
      ) : null}

      {activeView === "tests" ? (
        <TestLabView
          loadReport={loadReport}
          runSuite={runSuite}
          selectedReport={selectedReport}
          selectedReportId={selectedReportId}
          setSuite={setSuite}
          suite={suite}
          testReports={testReports}
        />
      ) : null}

      {activeView === "traces" ? (
        <AgentTraceView
          selectedTraceId={selectedTraceId}
          setSelectedTraceId={setSelectedTraceId}
          traces={traces}
        />
      ) : null}

      {activeView === "ralph" ? (
        <RalphDashboardView
          checkRalphTask={checkRalphTask}
          ralphReport={ralphReport}
          ralphStatus={ralphStatus}
          selectedTaskId={selectedRalphTaskId}
        />
      ) : null}
    </main>
  );
}

function RalphDashboardView({
  checkRalphTask,
  ralphReport,
  ralphStatus,
  selectedTaskId
}: {
  checkRalphTask: (taskId: string) => void;
  ralphReport: TestReport | null;
  ralphStatus: RalphStatus | null;
  selectedTaskId: string;
}) {
  const tasks = ralphStatus?.tasks ?? [];
  const selectedTask = tasks.find((task) => task.id === selectedTaskId) ?? tasks[0];

  return (
    <section className="ralph-layout">
      <section className="panel" aria-label="Ralph progress">
        <div className="panel-heading">
          <h2>Progress</h2>
          <GitBranch size={18} />
        </div>
        {ralphStatus ? (
          <div className="progress-grid">
            <ProgressBlock title="Completed" values={ralphStatus.progress.completed} />
            <ProgressBlock title="In Progress" values={ralphStatus.progress.in_progress} />
            <ProgressBlock title="Blocked" values={ralphStatus.progress.blocked} />
          </div>
        ) : (
          <div className="empty-state">No Ralph status</div>
        )}
      </section>

      <section className="panel" aria-label="Ralph tasks">
        <div className="panel-heading">
          <h2>Tasks</h2>
          <Workflow size={18} />
        </div>
        <div className="report-list">
          {tasks.map((task) => (
            <button
              className={task.id === selectedTaskId ? "report-row active" : "report-row"}
              key={task.id}
              type="button"
              onClick={() => checkRalphTask(task.id)}
            >
              <span>{task.id}</span>
              <strong>{task.status}</strong>
            </button>
          ))}
        </div>
      </section>

      <section className="panel" aria-label="Ralph task detail">
        <div className="panel-heading">
          <h2>Task Detail</h2>
          <CheckCircle2 size={18} />
        </div>
        {selectedTask ? (
          <div className="report-detail">
            <div className={selectedTask.status === "completed" ? "result pass" : "result fail"}>
              {selectedTask.status}
            </div>
            <h3>{selectedTask.title}</h3>
            <dl>
              <div>
                <dt>Criteria</dt>
                <dd>{selectedTask.acceptance_criteria.length}</dd>
              </div>
              <div>
                <dt>Tests</dt>
                <dd>{selectedTask.test_commands.length}</dd>
              </div>
              <div>
                <dt>Deps</dt>
                <dd>{selectedTask.dependencies.length}</dd>
              </div>
            </dl>
            {ralphReport ? <pre>{JSON.stringify(ralphReport, null, 2)}</pre> : null}
          </div>
        ) : (
          <div className="empty-state">No task selected</div>
        )}
      </section>
    </section>
  );
}

function ProgressBlock({ title, values }: { title: string; values: string[] }) {
  return (
    <div className="progress-block">
      <h3>{title}</h3>
      {values.length === 0 ? <span className="empty-state">None</span> : null}
      {values.slice(0, 6).map((value) => (
        <span key={value}>{value}</span>
      ))}
    </div>
  );
}

function StudioView({
  deleteSlot,
  importJson,
  selectedKey,
  selectedSlot,
  setSelectedKey,
  setSettings,
  settings,
  slots,
  updateSlot,
  validation,
  visibleRenderedText
}: {
  deleteSlot: (key: string) => void;
  importJson: (event: ChangeEvent<HTMLTextAreaElement>) => void;
  selectedKey: string;
  selectedSlot: PromptSlot | undefined;
  setSelectedKey: (key: string) => void;
  setSettings: (settings: typeof defaultSettings) => void;
  settings: typeof defaultSettings;
  slots: PromptSlot[];
  updateSlot: (index: number, patch: Partial<PromptSlot>) => void;
  validation: ValidationReport | null;
  visibleRenderedText: string;
}) {
  return (
    <>
      <section className="workspace">
        <section className="panel slot-panel" aria-label="Slot table">
          <div className="panel-heading">
            <h2>Slots</h2>
            <FileJson size={18} />
          </div>
          <div className="slot-table">
            {slots.map((slot, index) => (
              <button
                className={slot.key === selectedKey ? "slot-row active" : "slot-row"}
                key={`${slot.key}-${index}`}
                type="button"
                onClick={() => setSelectedKey(slot.key)}
              >
                <span className={`swatch ${slot.type}`} />
                <span>{slot.key}</span>
                <strong>{slot.priority}</strong>
              </button>
            ))}
          </div>
        </section>

        <section className="panel editor-panel" aria-label="Slot editor">
          <div className="panel-heading">
            <h2>Edit</h2>
            <Save size={18} />
          </div>
          {selectedSlot ? (
            <SlotEditor
              slot={selectedSlot}
              index={slots.indexOf(selectedSlot)}
              updateSlot={updateSlot}
              deleteSlot={deleteSlot}
            />
          ) : null}
        </section>

        <section className="panel render-panel" aria-label="Rendered prompt">
          <div className="panel-heading">
            <h2>Rendered</h2>
            <CheckCircle2 size={18} />
          </div>
          <RenderedPrompt text={visibleRenderedText} slots={slots} selectedKey={selectedKey} />
        </section>

        <section className="panel validation-panel" aria-label="Validation report">
          <div className="panel-heading">
            <h2>Validation</h2>
            <AlertTriangle size={18} />
          </div>
          <ValidationView report={validation} />
        </section>
      </section>

      <section className="bottom-band">
        <div className="import-area">
          <div className="panel-heading compact">
            <h2>Import</h2>
            <Upload size={18} />
          </div>
          <textarea aria-label="Import JSON" placeholder="Paste slot JSON" onChange={importJson} />
        </div>
        <div className="settings-area">
          <div className="panel-heading compact">
            <h2>Settings</h2>
            <Settings size={18} />
          </div>
          <label>
            API
            <input
              value={settings.apiBaseUrl}
              onChange={(event) => setSettings({ ...settings, apiBaseUrl: event.target.value })}
            />
          </label>
          <label>
            LLM
            <input
              value={settings.localLlmEndpoint}
              onChange={(event) =>
                setSettings({ ...settings, localLlmEndpoint: event.target.value })
              }
            />
          </label>
        </div>
      </section>
    </>
  );
}

function TestLabView({
  loadReport,
  runSuite,
  selectedReport,
  selectedReportId,
  setSuite,
  suite,
  testReports
}: {
  loadReport: (reportId: string) => void;
  runSuite: () => void;
  selectedReport: TestReport | null;
  selectedReportId: string;
  setSuite: (suite: TestReport["suite"]) => void;
  suite: TestReport["suite"];
  testReports: TestReport[];
}) {
  return (
    <section className="lab-layout">
      <section className="panel" aria-label="Test cases">
        <div className="panel-heading">
          <h2>Test Cases</h2>
          <Beaker size={18} />
        </div>
        <div className="suite-controls">
          <select value={suite} onChange={(event) => setSuite(event.target.value as TestReport["suite"])}>
            {["unit", "integration", "scenario", "regression", "e2e", "ralph"].map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
          <button type="button" onClick={runSuite}>
            Run
          </button>
        </div>
        <div className="case-list">
          <button className="case-row active" type="button">
            <span>scenario_pass_case</span>
            <strong>fixture</strong>
          </button>
          <button className="case-row" type="button">
            <span>expected_failure_probe</span>
            <strong>unit</strong>
          </button>
        </div>
      </section>

      <section className="panel" aria-label="Test reports">
        <div className="panel-heading">
          <h2>Reports</h2>
          <GitBranch size={18} />
        </div>
        <div className="report-list">
          {testReports.length === 0 ? <div className="empty-state">No reports</div> : null}
          {testReports.map((report) => (
            <button
              className={report.report_id === selectedReportId ? "report-row active" : "report-row"}
              key={report.report_id}
              type="button"
              onClick={() => loadReport(report.report_id)}
            >
              <span>{report.report_id}</span>
              <strong>{report.status}</strong>
            </button>
          ))}
        </div>
      </section>

      <section className="panel" aria-label="Report detail">
        <div className="panel-heading">
          <h2>Detail</h2>
          <AlertTriangle size={18} />
        </div>
        {selectedReport ? (
          <div className="report-detail">
            <div className={selectedReport.status === "pass" ? "result pass" : "result fail"}>
              {selectedReport.status}
            </div>
            <dl>
              <div>
                <dt>Suite</dt>
                <dd>{selectedReport.suite}</dd>
              </div>
              <div>
                <dt>Commands</dt>
                <dd>{selectedReport.commands.length}</dd>
              </div>
              <div>
                <dt>Artifacts</dt>
                <dd>{selectedReport.artifacts.length}</dd>
              </div>
            </dl>
            <pre>{JSON.stringify(selectedReport, null, 2)}</pre>
          </div>
        ) : (
          <div className="empty-state">No report selected</div>
        )}
      </section>
    </section>
  );
}

function AgentTraceView({
  selectedTraceId,
  setSelectedTraceId,
  traces
}: {
  selectedTraceId: string;
  setSelectedTraceId: (id: string) => void;
  traces: AgentTrace[];
}) {
  const selectedTrace = traces.find((trace) => trace.id === selectedTraceId) ?? traces[0];

  return (
    <section className="trace-layout">
      <section className="panel" aria-label="Trace list">
        <div className="panel-heading">
          <h2>Traces</h2>
          <Workflow size={18} />
        </div>
        <div className="report-list">
          {traces.map((trace) => (
            <button
              className={trace.id === selectedTraceId ? "report-row active" : "report-row"}
              key={trace.id}
              type="button"
              onClick={() => setSelectedTraceId(trace.id)}
            >
              <span>{trace.id}</span>
              <strong>{trace.status}</strong>
            </button>
          ))}
        </div>
      </section>

      <section className="panel" aria-label="Trace detail">
        <div className="panel-heading">
          <h2>Trace Detail</h2>
          <CheckCircle2 size={18} />
        </div>
        <div className="trace-detail">
          <dl>
            <div>
              <dt>Spec</dt>
              <dd>{selectedTrace.specId}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{selectedTrace.status}</dd>
            </div>
            <div>
              <dt>Uncertain</dt>
              <dd>{selectedTrace.uncertainties.length}</dd>
            </div>
          </dl>
          <h3>Prompt</h3>
          <pre>{selectedTrace.prompt}</pre>
          <h3>Raw Model</h3>
          <pre>{selectedTrace.rawModel}</pre>
          <h3>Meaning</h3>
          <pre>{JSON.stringify(selectedTrace.meaning, null, 2)}</pre>
        </div>
      </section>
    </section>
  );
}

function SlotEditor({
  slot,
  index,
  updateSlot,
  deleteSlot
}: {
  slot: PromptSlot;
  index: number;
  updateSlot: (index: number, patch: Partial<PromptSlot>) => void;
  deleteSlot: (key: string) => void;
}) {
  return (
    <div className="editor-grid">
      <label>
        Key
        <input value={slot.key} onChange={(event) => updateSlot(index, { key: event.target.value })} />
      </label>
      <label>
        Type
        <select
          value={slot.type}
          onChange={(event) => updateSlot(index, { type: event.target.value as PromptSlot["type"] })}
        >
          {slotTypes.map((type) => (
            <option key={type}>{type}</option>
          ))}
        </select>
      </label>
      <label>
        Source
        <select
          value={slot.source}
          onChange={(event) =>
            updateSlot(index, { source: event.target.value as PromptSlot["source"] })
          }
        >
          {sourceTypes.map((source) => (
            <option key={source}>{source}</option>
          ))}
        </select>
      </label>
      <label>
        Priority
        <input
          type="number"
          value={slot.priority}
          onChange={(event) => updateSlot(index, { priority: Number(event.target.value) })}
        />
      </label>
      <label className="wide">
        Value
        <textarea value={slot.value} onChange={(event) => updateSlot(index, { value: event.target.value })} />
      </label>
      <label className="check-line">
        <input
          type="checkbox"
          checked={slot.required}
          onChange={(event) => updateSlot(index, { required: event.target.checked })}
        />
        Required
      </label>
      <button
        className="delete-button"
        type="button"
        onClick={() => deleteSlot(slot.key)}
        title="Delete slot"
        aria-label="Delete slot"
      >
        <Trash2 size={18} />
      </button>
    </div>
  );
}

function RenderedPrompt({
  text,
  slots,
  selectedKey
}: {
  text: string;
  slots: PromptSlot[];
  selectedKey: string;
}) {
  const parts = slots.map((slot) => ({
    key: slot.key,
    value: slot.value,
    active: slot.key === selectedKey,
    type: slot.type
  }));

  return (
    <div className="rendered-text">
      {parts.length > 0
        ? parts.map((part) => (
            <mark className={part.active ? `span active ${part.type}` : `span ${part.type}`} key={part.key}>
              {part.value}
            </mark>
          ))
        : text}
    </div>
  );
}

function ValidationView({ report }: { report: ValidationReport | null }) {
  if (!report) {
    return <div className="empty-state">No report</div>;
  }

  return (
    <div className="validation-list">
      <div className={report.status === "pass" ? "result pass" : "result fail"}>{report.status}</div>
      <dl>
        <div>
          <dt>Coverage</dt>
          <dd>{Math.round(report.metrics.slot_coverage * 100)}%</dd>
        </div>
        <div>
          <dt>Conflicts</dt>
          <dd>{report.metrics.conflict_count}</dd>
        </div>
        <div>
          <dt>Over</dt>
          <dd>{report.metrics.critical_over_generation}</dd>
        </div>
      </dl>
      {report.issues.map((issue) => (
        <div className="issue" key={`${issue.code}-${issue.message}`}>
          <strong>{issue.code}</strong>
          <span>{issue.message}</span>
        </div>
      ))}
    </div>
  );
}
