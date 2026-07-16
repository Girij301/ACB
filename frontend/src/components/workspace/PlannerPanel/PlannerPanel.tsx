import {
  LoaderCircle,
  Play,
  Route,
  Sparkles,
} from "lucide-react";

import { useExecution } from "@/hooks";

import type { PlanStep } from "@/services/planner";

interface PlannerPanelProps {
  sessionId: string;
  task: string;
  plan: PlanStep[];
  loading: boolean;
}

export function PlannerPanel({
  sessionId,
  task,
  plan,
  loading,
}: PlannerPanelProps) {
  const {
    activeStep,
    steps,
    loading: executing,
    execute,
  } = useExecution();

  function getStepStatus(stepNumber: number) {
    const executionStep = steps.find(
      (step) => step.step_number === stepNumber
    );

    if (!executionStep) {
      return "pending";
    }

    return executionStep.status;
  }

  function getStatusBadge(status: string) {
    switch (status) {
      case "success":
        return {
          label: "Completed",
          className:
            "border-green-400/20 bg-green-500/10 text-green-300",
        };

      case "failed":
        return {
          label: "Failed",
          className:
            "border-red-400/20 bg-red-500/10 text-red-300",
        };

      case "running":
        return {
          label: "Running",
          className:
            "border-cyan-400/20 bg-cyan-500/10 text-cyan-300",
        };

      default:
        return {
          label: "Pending",
          className:
            "border-white/10 bg-white/5 text-white/60",
        };
    }
  }

  return (
    <section className="glass flex h-full min-h-0 flex-col rounded-2xl p-5">
      {/* Header */}

      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
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
            <Route className="h-5 w-5" />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-semibold text-white">
                Execution Plan
              </h2>

              <Sparkles className="h-4 w-4 text-cyan-400" />
            </div>

            <p className="mt-1 text-sm text-white/45">
              AI generated implementation roadmap
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {loading && (
            <span
              className="
                rounded-full
                border
                border-cyan-400/20
                bg-cyan-500/10
                px-3
                py-1
                text-xs
                text-cyan-300
              "
            >
              Planning...
            </span>
          )}

          {plan.length > 0 && (
            <button
              onClick={() =>
                execute(sessionId, task)
              }
              disabled={executing}
              className="
                inline-flex
                items-center
                gap-2
                rounded-xl
                border
                border-cyan-500/20
                bg-cyan-500/10
                px-5
                py-2.5
                text-sm
                font-medium
                text-cyan-300
                transition-all
                duration-300
                hover:scale-[1.02]
                hover:border-cyan-500/40
                hover:bg-cyan-500/20
                hover:shadow-[0_0_16px_rgba(34,211,238,0.12)]
                disabled:cursor-not-allowed
                disabled:opacity-50
              "
            >
              {executing ? (
                <>
                  <LoaderCircle className="h-4 w-4 animate-spin" />
                  Executing...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  Execute
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Content */}

      <div
        className="
          min-h-0
          flex-1
          overflow-y-auto
          rounded-xl
          border
          border-white/10
          bg-black/20
          p-4
        "
      >
        {plan.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="max-w-sm text-center">
              <h3 className="text-lg font-medium text-white">
                No execution plan
              </h3>

              <p className="mt-3 text-sm leading-6 text-white/50">
                Ask ACB AI to build, debug or improve a
                project. The generated execution plan
                will appear here before execution starts.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {plan.map((step) => {
              const status = getStepStatus(step.step);
              const badge =
                getStatusBadge(status);

              const isActive =
                activeStep === step.step;

              return (
                <div
                  key={step.step}
                  className={`
                    rounded-xl
                    border
                    p-4
                    transition-all
                    duration-300
                    ${
                      isActive
                        ? `
                          border-cyan-400/40
                          bg-cyan-500/10
                          shadow-[0_0_20px_rgba(34,211,238,0.08)]
                        `
                        : `
                          border-white/10
                          bg-white/5
                          hover:bg-white/10
                        `
                    }
                  `}
                >
                  <div className="flex items-start gap-4">
                    <div
                      className={`
                        flex
                        h-9
                        w-9
                        shrink-0
                        items-center
                        justify-center
                        rounded-full
                        text-sm
                        font-semibold
                        transition-all
                        duration-300
                        ${
                          status === "success"
                            ? `
                              bg-green-500/20
                              text-green-300
                            `
                            : status === "failed"
                            ? `
                              bg-red-500/20
                              text-red-300
                            `
                            : isActive
                            ? `
                              bg-cyan-500/20
                              text-cyan-300
                            `
                            : `
                              bg-white/10
                              text-white/60
                            `
                        }
                      `}
                    >
                      {step.step}
                    </div>

                    <div className="min-w-0 flex-1">
                      <div className="flex items-start justify-between gap-3">
                        <p className="text-sm font-medium text-white">
                          {step.description}
                        </p>

                        <span
                          className={`
                            rounded-full
                            border
                            px-2.5
                            py-1
                            text-[11px]
                            font-medium
                            whitespace-nowrap
                            ${badge.className}
                          `}
                        >
                          {badge.label}
                        </span>
                      </div>

                      <p
                        className="
                          mt-2
                          text-xs
                          uppercase
                          tracking-wider
                          text-white/40
                        "
                      >
                        {step.action}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}