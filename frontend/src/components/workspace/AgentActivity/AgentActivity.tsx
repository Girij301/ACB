import { LoaderCircle, ChevronDown, ChevronRight } from "lucide-react";

import { useState } from "react";

import { useExecution } from "@/hooks";

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
    loading,
  } = useExecution();

  const [agentStateCollapsed, setAgentStateCollapsed] =
    useState(false);

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

  const isCompleted =
    currentPhase === "Completed";

  const isFailed =
    currentPhase === "Failed";


  return (
    <section
      className="
        glass
        flex
        h-full
        min-h-0
        overflow-hidden
        flex-col
        rounded-2xl
        p-5
      "
    >
      <div className="mb-5">
        <h2
          className="
            text-lg
            font-semibold
            text-white
          "
        >
          Agent Activity
        </h2>

        <p
          className="
            mt-1
            text-sm
            text-white/50
          "
        >
          Live execution monitoring
        </p>
      </div>

      <div
        className="
        min-h-0
        flex-1
        overflow-y-auto
        rounded-2xl
        border
        border-white/10
        bg-black/20
        p-5
      "
      >

        {/* Progress */}

        <section
          className="
            shrink-0
            rounded-2xl
            border
            border-white/10
            bg-gradient-to-b
            from-white/10
            to-white/5
            p-5
            shadow-sm
            transition-all
            duration-300
            mb-6
          "
        >
          <div
            className="
              mb-4
              flex
              items-center
              justify-between
            "
          >
            <div>
              <h3
                className="
                  text-sm
                  font-semibold
                  text-white
                "
              >
                Progress
              </h3>

              <p
                className="
                  mt-1
                  text-xs
                  text-white/45
                "
              >
                Overall execution progress
              </p>
            </div>

            <span
              className="
                rounded-full
                bg-white/10
                px-3
                py-1
                text-xs
                text-white/70
              "
            >
              {completedSteps}/{totalSteps}
            </span>
          </div>

          <div
            className="
              h-2.5
              overflow-hidden
              rounded-full
              bg-white/10
            "
          >
            <div
              className="
                h-full
                rounded-full
                bg-cyan-400
                transition-all
                duration-700
              "
              style={{
                width: `${progress}%`,
              }}
            />
          </div>

          <div className="mt-3 flex items-center justify-between">
            <p
              className="
                text-xs
                text-white/50
              "
            >
              {progress}% complete
            </p>

            <p
              className="
                text-xs
                text-cyan-300
              "
            >
              Live
            </p>
          </div>
        </section>

        {/* Phase Timeline */}

        <section
          className="
          shrink-0
          rounded-2xl
          border
          border-white/10
          bg-white/5
          p-5
          mb-6
        "
        >
          <button
            type="button"
            onClick={() =>
              setAgentStateCollapsed(
                !agentStateCollapsed,
              )
            }
            className="
            mb-5
            flex
            w-full
            items-center
            justify-between
            text-left
          "
          >
            <div>
              <h3 className="text-sm font-semibold text-white">
                Agent State
              </h3>

              <p className="mt-1 text-xs text-white/45">
                Current execution lifecycle
              </p>
            </div>

            {agentStateCollapsed ? (
              <ChevronRight className="h-4 w-4 text-white/50" />
            ) : (
              <ChevronDown className="h-4 w-4 text-white/50" />
            )}
          </button>
          {!agentStateCollapsed && (
            <div
              className="
              space-y-4
            "
            >
              {phases.map((phase, index) => {
                let completed = false;
                let active = false;

                if (isCompleted) {
                  completed =
                    phase !== "Completed";
                } else if (isFailed) {
                  completed =
                    phase !== "Failed";

                  active =
                    phase === "Failed";
                } else {
                  completed =
                    index < activeIndex;

                  active =
                    phase === currentPhase;
                }

                return (
                  <div
                    key={phase}
                    className="
                    flex
                    items-center
                    gap-3
                    transition-all
                    duration-300
                  "
                  >
                    <div
                      className="
                      flex
                      h-6
                      w-6
                      items-center
                      justify-center
                      rounded-full
                      bg-black/20
                    "
                    >
                      {completed ? (
                        <span className="text-green-400">
                          ✓
                        </span>
                      ) : active ? (
                        <LoaderCircle
                          className="
                          h-4
                          w-4
                          animate-spin
                          text-cyan-400
                        "
                        />
                      ) : (
                        <span className="text-white/30">
                          ○
                        </span>
                      )}
                    </div>

                    <span
                      className={`
                      text-sm
                      transition-all
                      duration-300
                      ${completed
                          ? "font-medium text-green-300"
                          : active
                            ? "font-medium text-white"
                            : "text-white/50"
                        }
                    `}
                    >
                      {phase}
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        {/* Current Action */}

        <section
          className="
            shrink-0
            rounded-2xl
            border
            border-cyan-500/10
            bg-gradient-to-b
            from-cyan-500/5
            to-transparent
            p-5
            mb-6
          "
        >
          <div className="mb-4">
            <h3
              className="
                text-sm
                font-semibold
                text-white
              "
            >
              Current Action
            </h3>

            <p
              className="
                mt-1
                text-xs
                text-white/45
              "
            >
              Live agent activity
            </p>
          </div>

          <div
            className="
              rounded-xl
              border
              border-white/10
              bg-black/20
              px-4
              py-3
              transition-all
              duration-300
            "
          >
            {loading ? (
              <div
                className="
                  flex
                  items-center
                  gap-2
                  text-sm
                  text-white/70
                "
              >
                <LoaderCircle
                  className="
                    h-4
                    w-4
                    animate-spin
                    text-cyan-400
                  "
                />

                Agent working...
              </div>
            ) : (
              <p
                className="
                  text-sm
                  text-white/80
                "
              >
                {currentAction ||
                  "Waiting for execution..."}
              </p>
            )}
          </div>
        </section>

        {/* Timeline */}
        <section>
          <div
            className="
            shrink-0
            min-h-0
            pt-1
          "
          >
            <ExecutionTimeline />
          </div>
        </section>
      </div>
    </section>
  );
}