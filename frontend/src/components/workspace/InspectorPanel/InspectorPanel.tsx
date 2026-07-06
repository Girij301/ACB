import type { ExecutionSummary } from "@/services/execution";

interface InspectorPanelProps {
  execution: ExecutionSummary | null;
}

export function InspectorPanel({
  execution,
}: InspectorPanelProps) {
  return (
    <section className="glass flex h-full flex-col rounded-2xl p-5">
      <h2 className="mb-4 text-lg font-semibold text-white">
        Inspector
      </h2>

      {!execution ? (
        <div className="flex flex-1 items-center justify-center rounded-xl border border-white/5 bg-black/20">
          <p className="text-center text-sm text-white/50">
            Execute a plan to view execution details.
          </p>
        </div>
      ) : (
        <div className="space-y-4 rounded-xl border border-white/5 bg-black/20 p-4">
          <div>
            <p className="text-xs text-white/50">
              Execution ID
            </p>

            <p className="text-white">
              {execution.execution_id}
            </p>
          </div>

          <div>
            <p className="text-xs text-white/50">
              Status
            </p>

            <p className="text-green-400">
              {execution.status}
            </p>
          </div>

          <div>
            <p className="text-xs text-white/50">
              Total Steps
            </p>

            <p className="text-white">
              {execution.total_steps}
            </p>
          </div>

          <div>
            <p className="text-xs text-white/50">
              Duration
            </p>

            <p className="text-white">
              {execution.duration_ms} ms
            </p>
          </div>
        </div>
      )}
    </section>
  );
}