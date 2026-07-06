import { workspaceHeaderVariants } from "./workspaceHeaderVariants";

export function WorkspaceHeader() {
  return (
    <header className={workspaceHeaderVariants()}>
      <h1 className="text-lg font-semibold">
        ACB AI Workspace
      </h1>

      <span className="text-sm text-white/50">
        Connected
      </span>
    </header>
  );
}