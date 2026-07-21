import {
  CheckCircle2,
  LoaderCircle,
} from "lucide-react";

import { useExecution } from "@/hooks";

import { workspaceStatusBarVariants } from "./workspaceStatusBarVariants";

export function WorkspaceStatusBar() {
  const {
    loading,
    currentPhase,
    progress,
  } = useExecution();

  return (
    <footer className={workspaceStatusBarVariants()}>
      <div className="flex flex-1 items-center justify-between">
        {/* Left */}

        <div className="flex items-center gap-6">

          <div className="h-4 w-px bg-white/10" />

          <div className="flex items-center gap-2 text-white/70">
            {loading ? (
              <>
                <LoaderCircle className="h-4 w-4 animate-spin text-cyan-400" />

                <span>{currentPhase}</span>
              </>
            ) : (
              <>
                <CheckCircle2 className="h-4 w-4 text-emerald-400" />

                <span>Workspace Ready</span>
              </>
            )}
          </div>
        </div>

        {/* Right */}

        <div className="flex items-center gap-6 text-white/60">
          <span>
            Phase:
            <span className="ml-2 text-white">
              {currentPhase}
            </span>
          </span>

          <div className="h-4 w-px bg-white/10" />

          <span>
            Progress:
            <span className="ml-2 text-cyan-300">
              {progress}%
            </span>
          </span>
        </div>
      </div>
    </footer>
  );
}