import {
  WorkspaceHeader,
  WorkspaceMain,
  WorkspaceStatusBar,
} from "@/components/workspace";

import { workspaceVariants } from "./workspaceVariants";

export function Workspace() {
  return (
    <main className="flex h-screen flex-col bg-background text-white">
      { <WorkspaceHeader /> }

      <div className="flex-1 min-h-0">
        <WorkspaceMain />
      </div>

      { <WorkspaceStatusBar /> }
    </main>
  );
}