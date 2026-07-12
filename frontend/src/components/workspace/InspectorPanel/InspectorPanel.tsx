import {
  Activity,
  CheckCircle2,
  Clock3,
  FolderOpen,
  RotateCcw,
  Bug,
  ClipboardCheck,
  Hash,
} from "lucide-react";

import type { ExecutionSummary } from "@/services/execution";

interface InspectorPanelProps {
  execution: ExecutionSummary | null;
}

function StatusBadge({ status }: { status: string }) {
  const styles =
    status === "SUCCESS"
      ? "bg-green-500/15 text-green-300 border-green-500/20"
      : status === "FAILED"
        ? "bg-red-500/15 text-red-300 border-red-500/20"
        : "bg-amber-500/15 text-amber-300 border-amber-500/20";

  return (
    <span
      className={`rounded-full border px-3 py-1 text-xs font-semibold ${styles}`}
    >
      {status}
    </span>
  );
}

interface MetricCardProps {
  label: string;
  value: number | string;
}

function MetricCard({
  label,
  value,
}: MetricCardProps) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <p className="text-xs uppercase tracking-wide text-white/40">
        {label}
      </p>

      <p className="mt-2 text-2xl font-semibold text-white">
        {value}
      </p>
    </div>
  );
}

export function InspectorPanel({
  execution,
}: InspectorPanelProps) {
  return (
    <section className="glass flex h-full flex-col rounded-2xl p-5">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="flex items-center gap-2 text-lg font-semibold text-white">
          <Activity className="h-5 w-5 text-cyan-400" />
          Inspector
        </h2>

        {execution && (
          <StatusBadge status={execution.status} />
        )}
      </div>

      {!execution ? (
        <div className="flex flex-1 items-center justify-center rounded-xl border border-white/5 bg-black/20">
          <p className="max-w-xs text-center text-sm text-white/50">
            Execute a plan to inspect runtime information,
            execution metrics and workspace details.
          </p>
        </div>
      ) : (
        <div className="space-y-5 overflow-y-auto">

          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <div className="space-y-3 text-sm">

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/50">
                  <Hash className="h-4 w-4" />
                  Execution
                </span>

                <span className="font-medium text-white">
                  #{execution.execution_id}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-white/50">
                  Plan
                </span>

                <span className="font-medium text-white">
                  #{execution.plan_id}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-white/50">
                  Session
                </span>

                <span className="max-w-[160px] truncate font-mono text-xs text-cyan-300">
                  {execution.session_id}
                </span>
              </div>

            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">

            <MetricCard
              label="Steps"
              value={execution.total_steps}
            />

            <MetricCard
              label="Success"
              value={execution.successful_steps}
            />

            <MetricCard
              label="Failed"
              value={execution.failed_steps}
            />

            <MetricCard
              label="Duration"
              value={`${execution.duration_ms} ms`}
            />

          </div>

          <div className="rounded-xl border border-white/10 bg-white/5 p-4">

            <div className="space-y-4 text-sm">

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/60">
                  <RotateCcw className="h-4 w-4" />
                  Retries
                </span>

                <span className="font-medium text-white">
                  {execution.retry_count}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/60">
                  <Bug className="h-4 w-4" />
                  Debug Attempts
                </span>

                <span className="font-medium text-white">
                  {execution.debug_count}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/60">
                  <ClipboardCheck className="h-4 w-4" />
                  Validations
                </span>

                <span className="font-medium text-white">
                  {execution.validation_count}
                </span>
              </div>

            </div>

          </div>

          <div className="rounded-xl border border-white/10 bg-black/30 p-4">

            <div className="mb-3 flex items-center gap-2 text-sm font-medium text-white">
              <FolderOpen className="h-4 w-4 text-cyan-400" />
              Workspace
            </div>

            <code className="block break-all rounded-lg bg-black/40 p-3 font-mono text-xs text-cyan-300">
              {execution.workspace}
            </code>

          </div>

          <div className="rounded-xl border border-white/10 bg-white/5 p-4">

            <div className="flex items-center gap-2 text-sm text-white/70">
              <Clock3 className="h-4 w-4" />
              Started
            </div>

            <p className="mt-2 text-xs text-white/50">
              {new Date(execution.started_at).toLocaleString()}
            </p>

          </div>

        </div>
      )}
    </section>
  );
}