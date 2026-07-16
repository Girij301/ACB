import {
  Activity,
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
    <div
      className="
        rounded-2xl
        border
        border-white/10
        bg-gradient-to-b
        from-white/10
        to-white/5
        p-4
        transition-all
        duration-300
        hover:border-cyan-500/20
        hover:bg-white/10
      "
    >
      <p className="text-xs uppercase tracking-wide text-white/45">
        {label}
      </p>

      <p className="mt-3 text-3xl font-semibold text-white">
        {value}
      </p>
    </div>
  );
}

export function InspectorPanel({
  execution,
}: InspectorPanelProps) {
  return (
    <section className="glass flex h-full min-h-0 flex-col rounded-2xl p-5">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h2 className="flex items-center gap-2 text-lg font-semibold text-white">
            <div
              className="
                flex
                h-11
                w-11
                items-center
                justify-center
                rounded-xl
                bg-cyan-500/10
                text-cyan-300
              "
            >
              <Activity className="h-5 w-5" />
            </div>
            Inspector
          </h2>

          <p className="mt-1 text-sm text-white/50">
            Runtime execution details
          </p>
        </div>

        {execution && (
          <StatusBadge status={execution.status} />
        )}
      </div>

      {!execution ? (
        <div className="flex flex-1 items-center justify-center rounded-2xl border border-dashed border-white/10 bg-black/20">
          <div className="max-w-xs text-center">
            <div
              className="
                mx-auto
                flex
                h-16
                w-16
                items-center
                justify-center
                rounded-2xl
                bg-gradient-to-b
                from-white/10
                to-white/5
              "
            >
              <Activity className="h-8 w-8 text-cyan-400/70" />
            </div>

            <h3 className="mt-4 text-base font-semibold text-white">
              Execution Inspector
            </h3>

            <p className="mt-2 text-sm leading-6 text-white/45">
              Execution metrics, workspace information,
              runtime statistics and recovery data will
              appear here once execution begins.
            </p>
          </div>
        </div>
      ) : (
        <div className="min-h-0 flex-1 space-y-6 overflow-y-auto pr-1">
          <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-5">
            <h3 className="mb-4 text-sm font-semibold text-white">
              Execution Details
            </h3>

            <div className="space-y-4 text-sm">
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

                <span className="max-w-[170px] truncate font-mono text-xs text-cyan-300">
                  {execution.session_id}
                </span>
              </div>
            </div>
          </section>

          <section className="grid grid-cols-2 gap-3">
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
          </section>

          <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-5">
            <h3 className="mb-4 text-sm font-semibold text-white">
              Recovery Metrics
            </h3>

            <div className="space-y-4 text-sm">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/60">
                  <RotateCcw className="h-4 w-4" />
                  Retries
                </span>

                <span className="font-semibold text-white">
                  {execution.retry_count}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/60">
                  <Bug className="h-4 w-4" />
                  Debug Runs
                </span>

                <span className="font-semibold text-white">
                  {execution.debug_count}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-white/60">
                  <ClipboardCheck className="h-4 w-4" />
                  Validations
                </span>

                <span className="font-semibold text-white">
                  {execution.validation_count}
                </span>
              </div>
            </div>
          </section>

          <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-cyan-500/5 to-transparent p-5">
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-white">
              <FolderOpen className="h-4 w-4 text-cyan-400" />
              Workspace
            </div>

            <code className="block break-all rounded-xl bg-black/30 border border-white/10 p-3 font-mono text-xs text-cyan-300">
              {execution.workspace}
            </code>
          </section>

          <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-5">
            <div className="flex items-center gap-2 text-sm font-semibold text-white">
              <Clock3 className="h-4 w-4 text-cyan-400" />
              Started
            </div>

            <p className="mt-3 text-xs text-white/50">
              {new Date(
                execution.started_at,
              ).toLocaleString()}
            </p>
          </section>
        </div>
      )}
    </section>
  );
}