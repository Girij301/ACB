import {
  WorkspaceContent,
  WorkspaceSidebar,
} from "@/components/workspace";

import { workspaceMainVariants } from "./workspaceMainVariants";

export function WorkspaceMain() {
  return (
    <div className={workspaceMainVariants()}>
      <WorkspaceSidebar />

      <WorkspaceContent />
    </div>
  );
}