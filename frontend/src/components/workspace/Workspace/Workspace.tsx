import {
  WorkspaceHeader,
  WorkspaceContent,
  WorkspaceStatusBar,
} from "@/components/workspace";

import { workspaceVariants } from "./workspaceVariants";

export function Workspace() {
  return (
    <main className={workspaceVariants()}>
      <WorkspaceHeader />

      <WorkspaceContent />

      <WorkspaceStatusBar />
    </main>
  );
}