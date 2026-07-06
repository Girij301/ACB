import type { PlanStep } from "@/services/planner";

interface PlannerPanelProps {
  plan: PlanStep[];
  loading: boolean;

  executing: boolean;

  onExecute: () => void | Promise<void>;
}

export function PlannerPanel({
  plan,
  loading,
  executing,
  onExecute,
}: PlannerPanelProps) {
  return (
    <section className="glass flex h-full flex-col rounded-2xl p-5">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">
          Planner
        </h2>

        <div className="flex items-center gap-3">
          {loading && (
            <span className="text-xs text-cyan-300">
              Planning...
            </span>
          )}

          {plan.length > 0 && (
            <button
              onClick={onExecute}
              disabled={executing}
              className="
                rounded-lg
                bg-cyan-500
                px-4
                py-2
                text-sm
                font-medium
                text-white
                transition-colors
                hover:bg-cyan-400
                disabled:cursor-not-allowed
                disabled:opacity-50
              "
            >
              {executing ? "Executing..." : "Execute"}
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto rounded-xl border border-white/5 bg-black/20 p-4">
        {plan.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <p className="text-center text-sm text-white/50">
              Ask the AI to build something and the execution plan will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {plan.map((step) => (
              <div
                key={step.step}
                className="rounded-xl border border-white/10 bg-white/5 p-3"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-7 w-7 items-center justify-center rounded-full bg-cyan-500/15 text-sm font-semibold text-cyan-300">
                    {step.step}
                  </div>

                  <div className="flex-1">
                    <p className="text-sm font-medium text-white">
                      {step.description}
                    </p>

                    <p className="mt-1 text-xs uppercase tracking-wide text-white/40">
                      {step.action}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}