import {
  BottomPanel,
  InspectorPanel,
  WorkspaceContent,
  WorkspaceSidebar,
} from "@/components/workspace";

import { useExecution } from "@/hooks";

import { workspaceMainVariants } from "./workspaceMainVariants";
import { useWorkspaceStore } from "@/store";

export function WorkspaceMain() {
  const { execution } = useExecution();
  const { layout } = useWorkspaceStore();

  return (
    <main className={workspaceMainVariants()}>
      <div className="flex h-full min-h-0 flex-1 gap-5 overflow-hidden">

        {!layout.sidebarCollapsed && (
          <WorkspaceSidebar />
        )}

        <div className="flex h-full min-h-0 flex-1 flex-col gap-5">

          <div className="h-full min-h-0 flex-1">
            <WorkspaceContent />
          </div>

          {!layout.bottomPanelCollapsed && (
            <BottomPanel />
          )}

        </div>

        {!layout.inspectorCollapsed && (
          <div className="h-full w-[320px] min-h-0 shrink-0">
            <InspectorPanel execution={execution} />
          </div>
        )}

      </div>
    </main>
  );
}