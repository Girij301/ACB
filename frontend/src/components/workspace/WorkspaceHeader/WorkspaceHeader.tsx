import {
  PanelLeft,
  PanelRight,
  PanelBottom,
  Wifi,
  Sparkles,
} from "lucide-react";

import { useExecution } from "@/hooks";
import { useWorkspaceStore } from "@/store";

import { workspaceHeaderVariants } from "./workspaceHeaderVariants";

function HeaderButton({
  title,
  active,
  onClick,
  children,
}: {
  title: string;
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      title={title}
      onClick={onClick}
      className={`
        group
        flex
        h-10
        w-10
        items-center
        justify-center
        rounded-xl
        border
        transition-all
        duration-200
        ${
          active
            ? "border-cyan-500/20 bg-cyan-500/10 text-cyan-300 shadow-[0_0_12px_rgba(34,211,238,0.08)]"
            : "border-white/10 bg-white/5 text-white/60 hover:border-white/20 hover:bg-white/10 hover:text-white"
        }
      `}
    >
      {children}
    </button>
  );
}

export function WorkspaceHeader() {
  const { connected } = useExecution();

  const {
    layout,
    toggleSidebar,
    toggleInspector,
    toggleBottomPanel,
  } = useWorkspaceStore();

  return (
    <header className={workspaceHeaderVariants()}>
      {/* Left */}

      <div className="flex items-center gap-6">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-cyan-400" />

            <h1 className="text-lg font-semibold text-white">
              ACB AI
            </h1>
          </div>

          <p className="text-xs text-white/45">
            Autonomous Development Workspace
          </p>
        </div>

        <div className="h-8 w-px bg-white/10" />

        <div className="flex items-center gap-2">
          <HeaderButton
            title={
              layout.sidebarCollapsed
                ? "Show Sidebar"
                : "Hide Sidebar"
            }
            active={!layout.sidebarCollapsed}
            onClick={toggleSidebar}
          >
            <PanelLeft className="h-4 w-4" />
          </HeaderButton>

          <HeaderButton
            title={
              layout.bottomPanelCollapsed
                ? "Show Bottom Panel"
                : "Hide Bottom Panel"
            }
            active={!layout.bottomPanelCollapsed}
            onClick={toggleBottomPanel}
          >
            <PanelBottom className="h-4 w-4" />
          </HeaderButton>

          <HeaderButton
            title={
              layout.inspectorCollapsed
                ? "Show Inspector"
                : "Hide Inspector"
            }
            active={!layout.inspectorCollapsed}
            onClick={toggleInspector}
          >
            <PanelRight className="h-4 w-4" />
          </HeaderButton>
        </div>
      </div>

      {/* Right */}

      <div className="flex items-center gap-4">
        <div
          className={`
            flex
            items-center
            gap-2
            rounded-full
            border
            px-4
            py-2
            text-xs
            font-medium
            transition-all
            ${
              connected
                ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300"
                : "border-amber-500/20 bg-amber-500/10 text-amber-300"
            }
          `}
        >
          <div
            className={`
              h-2
              w-2
              rounded-full
              ${
                connected
                  ? "bg-emerald-400"
                  : "bg-amber-400"
              }
            `}
          />

          <Wifi className="h-3.5 w-3.5" />

          {connected ? "Connected" : "Idle"}
        </div>
      </div>
    </header>
  );
}