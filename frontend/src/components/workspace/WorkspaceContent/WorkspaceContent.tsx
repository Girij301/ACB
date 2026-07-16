import { useMemo, useState } from "react";

import { useWorkspaceStore } from "@/store";

import { ChatPanel } from "../ChatPanel";
import { PlannerPanel } from "../PlannerPanel";
import { AgentActivity } from "../AgentActivity";

import {
  useChat,
  usePlanner,
  useExecution,
} from "@/hooks";

import { workspaceContentVariants } from "./workspaceContentVariants";

export function WorkspaceContent() {
  const sessionId = useMemo(
    () => crypto.randomUUID(),
    []
  );

  const {
    messages,
    loading,
    sendMessage,
  } = useChat(sessionId);

  const planner = usePlanner();

  const execution = useExecution();

  const { layout } = useWorkspaceStore();

  const [currentTask, setCurrentTask] =
    useState("");

  async function handleSend(message: string) {
    setCurrentTask(message);

    await sendMessage(message);

    await planner.createPlan(
      sessionId,
      message
    );
  }

  return (
    <main className={workspaceContentVariants()}>
      <div className="flex h-full min-h-0 flex-1 flex-col gap-4">
        {layout.selectedView === "chat" && (
          <ChatPanel
            messages={messages}
            loading={loading}
            onSend={handleSend}
          />
        )}

        {layout.selectedView === "planner" && (
          <PlannerPanel
            sessionId={sessionId}
            task={currentTask}
            plan={planner.plan}
            loading={planner.loading}
          />
        )}

        {layout.selectedView === "workspace" && (
          <div className="grid h-full min-h-0 gap-5 xl:grid-cols-[320px_minmax(0,1fr)]">
            {/* Chat */}
            <div className="h-full min-h-0 overflow-hidden">
              <ChatPanel
                messages={messages}
                loading={loading}
                onSend={handleSend}
              />
            </div>

            {/* Planner + Agent */}
            <div className="flex min-h-0 flex-col gap-4">

              {planner.plan.length > 0 && (
                <div
                  className={`flex-shrink-0 overflow-hidden transition-all duration-500 ${
                    execution.loading
                      ? "h-28"
                      : "h-80"
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

              {/* Agent Activity fills remaining height */}
              <div className="min-h-0 flex-1 overflow-hidden">
                <AgentActivity />
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}