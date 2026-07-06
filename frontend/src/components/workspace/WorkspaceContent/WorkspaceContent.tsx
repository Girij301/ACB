import { useMemo } from "react";

import { ChatPanel } from "../ChatPanel";

import { PlannerPanel } from "../PlannerPanel";

import { ExecutionPanel } from "../ExecutionPanel";

import { InspectorPanel } from "../InspectorPanel";

import { useChat, usePlanner } from "@/hooks";

import { workspaceContentVariants } from "./workspaceContentVariants";

export function WorkspaceContent() {
  const sessionId = useMemo(() => crypto.randomUUID(), []);

  const { messages, loading, sendMessage } = useChat(sessionId);

  const planner = usePlanner();

  async function handleSend(message: string) {
    await sendMessage(message);

    await planner.createPlan(sessionId, message);
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
            <PlannerPanel plan={planner.plan} loading={planner.loading} />
          </div>

          <div className="h-[260px]">
            <ExecutionPanel />
          </div>
        </div>

        <div className="h-full min-h-[860px]">
          <InspectorPanel />
        </div>
      </section>
    </main>
  );
}
