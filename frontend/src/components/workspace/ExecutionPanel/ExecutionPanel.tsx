import type { StepResult } from "@/services/execution";

interface ExecutionPanelProps {
  steps: StepResult[];
  loading: boolean;
  error: string | null;

  progress: number;

  completedSteps: number;

  totalSteps: number;

  activeStep: number | null;
}

export function ExecutionPanel({
  steps,
  loading,
  error,
  progress,
  completedSteps,
  totalSteps,
  activeStep,
}: ExecutionPanelProps) {
  if (error) {
    return (
      <section className="glass flex h-full flex-col rounded-2xl p-5">
        <h2 className="text-lg font-semibold text-white">Execution</h2>

        <div className="mt-4 flex flex-1 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5">
          <p className="text-sm text-red-400">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="glass flex h-full flex-col rounded-2xl p-5">
      <div className="mb-5 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Execution</h2>

        {loading && <span className="text-xs text-cyan-300">Executing...</span>}
      </div>

      {totalSteps > 0 && (
        <div className="mb-5">
          <div className="mb-2 flex justify-between text-xs text-white/60">
            <span>Progress</span>

            <span>
              {completedSteps} / {totalSteps}
            </span>
          </div>

          <div className="h-2 overflow-hidden rounded-full bg-white/10">
            <div
              className="h-full rounded-full bg-cyan-400 transition-all duration-300"
              style={{
                width: `${progress}%`,
              }}
            />
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto rounded-xl border border-white/5 bg-black/20 p-4">
        {steps.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <p className="text-center text-sm text-white/50">
              Execute the generated plan to see execution progress.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {steps.map((step) => {
              const isActive = activeStep === step.step_number;

              return (
                <div
                  key={step.step_number}
                  className={`rounded-xl border p-3 transition-all ${
                    isActive
                      ? "border-cyan-400 bg-cyan-500/10"
                      : "border-white/10 bg-white/5"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-white">
                      Step {step.step_number}
                    </span>

                    <span
                      className={`text-xs font-medium ${
                        step.status === "success"
                          ? "text-green-400"
                          : step.status === "failed"
                            ? "text-red-400"
                            : "text-yellow-400"
                      }`}
                    >
                      {step.status.toUpperCase()}
                    </span>
                  </div>

                  <p className="mt-2 text-sm text-white/80">
                    {step.description}
                  </p>

                  {step.message && (
                    <p className="mt-2 text-xs text-white/50">{step.message}</p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}
