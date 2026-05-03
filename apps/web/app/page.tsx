"use client";

import {
  AlertTriangle,
  CheckCircle2,
  Download,
  FileJson,
  Plus,
  RefreshCcw,
  Save,
  Settings,
  Trash2,
  Upload
} from "lucide-react";
import { ChangeEvent, useMemo, useState } from "react";
import {
  PromptSlot,
  ValidationReport,
  defaultSettings,
  renderLocal,
  resolveRenderValidate,
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
  const [slots, setSlots] = useState<PromptSlot[]>(initialSlots);
  const [selectedKey, setSelectedKey] = useState("audience");
  const [renderedText, setRenderedText] = useState("");
  const [validation, setValidation] = useState<ValidationReport | null>(null);
  const [settings, setSettings] = useState(defaultSettings);
  const [status, setStatus] = useState("Ready");

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
          <textarea
            aria-label="Import JSON"
            placeholder="Paste slot JSON"
            onChange={importJson}
          />
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
    </main>
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

