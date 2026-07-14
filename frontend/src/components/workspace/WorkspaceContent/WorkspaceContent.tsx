import { useMemo, useState } from "react";

import { ChatPanel } from "../ChatPanel";
import { PlannerPanel } from "../PlannerPanel";
import { AgentActivity } from "../AgentActivity";
import { InspectorPanel } from "../InspectorPanel";

import { useChat, usePlanner, useExecution } from "@/hooks";

import { workspaceContentVariants } from "./workspaceContentVariants";

export function WorkspaceContent() {
  const sessionId = useMemo(() => crypto.randomUUID(), []);

  const { messages, loading, sendMessage } = useChat(sessionId);

  const planner = usePlanner();

  const execution = useExecution();

  const [currentTask, setCurrentTask] = useState("");

  const [plannerCollapsed, setPlannerCollapsed] = useState(false);

  async function handleSend(message: string) {
    setCurrentTask(message);

    setPlannerCollapsed(false);

    await sendMessage(message);

    await planner.createPlan(sessionId, message);
  }

  return (
    <main className={workspaceContentVariants()}>
      <section className="grid h-full min-h-0 gap-5 xl:grid-cols-[320px_minmax(0,1fr)_320px]">

        {/* Chat */}
        <div className="min-h-0">
          <ChatPanel
            messages={messages}
            loading={loading}
            onSend={handleSend}
          />
        </div>

        {/* Planner + Execution */}
        <div className="flex min-h-0 flex-col gap-4">

          {planner.plan.length > 0 && (
            <div
              className={`overflow-hidden transition-all duration-500 ${
                execution.loading
                  ? "h-28 flex-shrink-0"
                  : "h-[40%] min-h-[280px]"
              }`}
            >
              <PlannerPanel
                sessionId={sessionId}
                task={currentTask}
                plan={planner.plan}
                loading={planner.loading}
              />
            </div>
          )}

          <div className="min-h-0 flex-1">
            <AgentActivity />
          </div>

        </div>

        {/* Inspector */}
        <div className="min-h-0">
          <InspectorPanel
            execution={execution.execution}
          />
        </div>

      </section>
    </main>
  );
}