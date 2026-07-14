import { useExecution } from "@/hooks";
import { LoaderCircle } from "lucide-react";
import { ExecutionTimeline } from "./ExecutionTimeline";

const BASE_PHASES = [
  "Idle",
  "Thinking",
  "Planning",
  "Executing",
  "Retrying",
  "Debugging",
  "Validation",
  "Completed",
];

export function AgentActivity() {
  const {
    currentPhase,
    currentAction,
    progress,
    completedSteps,
    totalSteps,
    hasFailed,
  } = useExecution();

  // Show Failed only once execution actually enters the Failed phase
  const phases = hasFailed
    ? [
        "Idle",
        "Executing",
        "Failed",
        "Retrying",
        "Debugging",
        "Validation",
        "Completed",
      ]
    : BASE_PHASES;

  const activeIndex = phases.indexOf(currentPhase);

  const isCompleted = currentPhase === "Completed";
  const isFailed = currentPhase === "Failed";

  return (
    <section className="glass flex h-full flex-col rounded-2xl p-5">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-white">
          Agent Activity
        </h2>

        <p className="mt-1 text-sm text-white/50">
          Live execution progress will appear here.
        </p>
      </div>

      <div className="flex flex-1 flex-col gap-5 overflow-hidden">
        {/* Progress */}
        <section className="rounded-xl border border-white/10 bg-white/5 p-4">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-medium text-white">
              Progress
            </h3>

            <span className="text-xs text-white/60">
              {completedSteps}/{totalSteps}
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

          <p className="mt-2 text-xs text-white/50">
            {progress}% complete
          </p>
        </section>


        {/* Agent Activity */}
        <section className="rounded-xl border border-white/10 bg-white/5 p-4">
          <h3 className="mb-3 text-sm font-medium text-white">
            Agent Activity
          </h3>

          <div className="space-y-3">
            {phases.map((phase, index) => {
              let completed = false;
              let active = false;

              if (isCompleted) {
                completed = phase !== "Completed";
                active = false;
              } else if (isFailed) {
                completed = phase !== "Failed";
                active = phase === "Failed";
              } else {
                completed = index < activeIndex;
                active = phase === currentPhase;
              }

              return (
                <div
                  key={phase}
                  className="flex items-center gap-3"
                >
                  <div className="flex h-4 w-4 items-center justify-center">
                    {completed ? (
                      <span className="text-green-400">
                        ✓
                      </span>
                    ) : active ? (
                      <LoaderCircle
                        className="h-4 w-4 animate-spin text-cyan-400"
                        strokeWidth={2}
                      />
                    ) : (
                      <span className="text-white/40">
                        ○
                      </span>
                    )}
                  </div>

                  <span
                    className={`text-sm ${
                      completed
                        ? "text-green-300"
                        : active
                          ? "text-white"
                          : "text-white/50"
                    }`}
                  >
                    {phase}
                  </span>
                </div>
              );
            })}
          </div>
        </section>


        {/* Current Action */}
        <section className="rounded-xl border border-white/10 bg-white/5 p-4">
          <h3 className="mb-3 text-sm font-medium text-white">
            Current Action
          </h3>

          <div className="rounded-lg border border-white/10 bg-black/20 px-3 py-2">
            <p className="text-sm text-white/80">
              {currentAction || "Waiting for execution..."}
            </p>
          </div>
        </section>


        {/* Execution Timeline */}
        <div className="min-h-0 flex-1 overflow-hidden">
          <ExecutionTimeline />
        </div>
      </div>
    </section>
  );
}