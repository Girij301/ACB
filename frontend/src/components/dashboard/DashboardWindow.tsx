import { Bot, CheckCircle2, Code2, Terminal } from "lucide-react";

import { Card } from "@/components/ui";
import { Loader2 } from "lucide-react";

export function DashboardWindow() {
  return (
    <Card
      variant="interactive"
      className="
        relative
        w-full
        max-w-6xl
        overflow-hidden
        transition-all
        duration-300
        hover:-translate-y-1
        rounded-3xl
        p-0
        shadow-2xl
        shadow-cyan-500/10
      "
    >
      {/* Window Header */}

      <div
        className="
          flex
          items-center
          gap-2
          border-b
          border-white/10
          px-6
          py-4
        "
      >
        <div className="h-3 w-3 rounded-full bg-red-400" />
        <div className="h-3 w-3 rounded-full bg-yellow-400" />
        <div className="h-3 w-3 rounded-full bg-green-400" />

        <span className="ml-4 text-sm text-white/50">
          Autonomous Coding Agent
        </span>
      </div>

      {/* Dashboard */}

      <div
        className="
          grid
          h-136
          grid-cols-[280px_1fr_280px]
        "
      >
        {/* Left */}

        <div className="border-r border-white/10 bg-white/2">
          <div className="border-b border-white/10 p-5">
            <div className="flex items-center gap-3">
              <Bot className="h-5 w-5 text-cyan-400" />

              <span className="font-medium text-white">AI Conversation</span>
            </div>
          </div>

          <div className="space-y-5 p-5">
            <div>
              <p className="text-xs uppercase text-white/40">Goal</p>

              <p className="mt-2 text-sm text-white/80">
                Build an ecommerce platform.
              </p>
            </div>

            <div>
              <p className="text-xs uppercase text-white/40">Planning</p>

              <div className="mt-2 flex items-center gap-2 text-sm text-cyan-300">
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating execution plan...
              </div>
            </div>

            <div>
              <p className="text-xs uppercase text-white/40">Thinking</p>

              <div className="mt-2 flex items-center gap-2">
                <span className="text-sm text-white/60">
                  Analyzing project structure
                </span>

                <span className="flex gap-1">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-cyan-400" />
                  <span
                    className="h-1.5 w-1.5 animate-pulse rounded-full bg-cyan-400"
                    style={{ animationDelay: "200ms" }}
                  />
                  <span
                    className="h-1.5 w-1.5 animate-pulse rounded-full bg-cyan-400"
                    style={{ animationDelay: "400ms" }}
                  />
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Center */}

        <div className="bg-neutral-950">
          <div className="border-b border-white/10 px-6 py-4">
            <div className="flex items-center gap-3">
              <Code2 className="h-5 w-5 text-violet-400" />

              <span className="font-medium text-white">app.py</span>
            </div>
          </div>

          <pre
            className="
                overflow-hidden
                p-6
                text-sm
                leading-7
                text-white/75
                "
          >
            {`class AutonomousAgent:

            def execute(self):
            plan = planner.create()

            executor.run(plan)

            validator.verify()

            return "Success"
            `}

            <span className="animate-pulse text-cyan-400">▋</span>
          </pre>
        </div>

        {/* Right */}

        <div className="border-l border-white/10 bg-white/[0.02]">
          <div className="border-b border-white/10 p-5">
            <div className="flex items-center gap-3">
              <Terminal className="h-5 w-5 text-green-400" />

              <span className="font-medium text-white">Execution</span>
            </div>
          </div>

          <div className="space-y-4 p-5">
            {[
              "Planning",
              "Generating Code",
              "Running Docker",
              "Validation",
              "Completed",
            ].map((step) => (
              <div key={step} className="flex items-center gap-3">
                <div className="relative">
                  <CheckCircle2 className="h-4 w-4 text-green-400" />

                  <span
                    className="
                        absolute
                        inset-0
                        rounded-full
                        bg-green-400/40
                        blur-sm
                        animate-ping
                        "
                  />
                </div>

                <span className="text-sm text-white/75">{step}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}
