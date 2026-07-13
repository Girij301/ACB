import { useMemo, useState } from "react";

import { ChatPanel } from "../ChatPanel";
import { PlannerPanel } from "../PlannerPanel";
import { ExecutionPanel } from "../ExecutionPanel";
import { InspectorPanel } from "../InspectorPanel";

import { useChat, usePlanner, useExecution } from "@/hooks";

import { workspaceContentVariants } from "./workspaceContentVariants";

export function WorkspaceContent() {
  const sessionId = useMemo(() => crypto.randomUUID(), []);

  const { messages, loading, sendMessage } = useChat(sessionId);

  const planner = usePlanner();

  const execution = useExecution();

  const [currentTask, setCurrentTask] = useState("");

  async function handleSend(message: string) {
    setCurrentTask(message);

    await sendMessage(message);

    await planner.createPlan(sessionId, message);
  }

  async function handleExecute() {
    if (!currentTask) return;

    await execution.execute(sessionId, currentTask);
  }

  return (
    <main className={workspaceContentVariants()}>
      <section className="grid gap-5 xl:grid-cols-[2fr_360px]">
        <div className="grid gap-5">
          <div className="h-[360px]">
            <ChatPanel
              messages={messages}
              loading={loading}
              onSend={handleSend}
            />
          </div>

          <div className="h-[220px]">
            <PlannerPanel
              plan={planner.plan}
              loading={planner.loading}
              executing={execution.loading}
              onExecute={handleExecute}
            />
          </div>

          <div className="h-[260px]">
            <ExecutionPanel
              steps={execution.steps}
              loading={execution.loading}
              error={execution.error}
              progress={execution.progress}
              completedSteps={execution.completedSteps}
              totalSteps={execution.totalSteps}
              activeStep={execution.activeStep}
            />
          </div>
        </div>

        <div className="h-full min-h-[860px]">
          <InspectorPanel execution={execution.execution} />
        </div>
      </section>
    </main>
  );
}
