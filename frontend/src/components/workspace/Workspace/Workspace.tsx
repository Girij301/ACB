import {
  WorkspaceHeader,
  WorkspaceMain,
  WorkspaceStatusBar,
} from "@/components/workspace";

import { workspaceVariants } from "./workspaceVariants";

export function Workspace() {
  return (
    <main className="flex h-screen min-h-0 flex-col overflow-hidden bg-background text-white">
      { <WorkspaceHeader /> }

      <div className="flex-1 min-h-0 overflow-hidden">
        <WorkspaceMain />
      </div>

      { <WorkspaceStatusBar /> }
    </main>
  );
}