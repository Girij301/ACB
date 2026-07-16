import {
  FolderOpen,
  FolderTree,
  History,
  ListTodo,
  MessageSquare,
  PanelLeftClose,
  Settings,
  Sparkles,
  Terminal,
} from "lucide-react";

import { useWorkspaceStore } from "@/store";

import { workspaceSidebarVariants } from "./workspaceSidebarVariants";

function SidebarButton({
  active,
  disabled = false,
  icon,
  label,
  onClick,
}: {
  active: boolean;
  disabled?: boolean;
  icon: React.ReactNode;
  label: string;
  onClick?: () => void;
}) {
  return (
    <button
      title={disabled ? `${label} (Coming Soon)` : label}
      disabled={disabled}
      onClick={onClick}
      className={`
        group
        flex
        w-full
        items-center
        gap-3
        rounded-xl
        border
        px-3
        py-3
        transition-all
        duration-200
        ${
          active
            ? "border-cyan-500/20 bg-cyan-500/10 text-cyan-300 shadow-[0_0_12px_rgba(34,211,238,0.08)]"
            : disabled
              ? "cursor-not-allowed border-transparent text-white/30 opacity-50"
              : "border-transparent text-white/60 hover:border-white/10 hover:bg-white/5 hover:text-white"
        }
      `}
    >
      <div
        className={`
          flex
          h-8
          w-8
          items-center
          justify-center
          rounded-lg
          ${
            active
              ? "bg-cyan-500/15"
              : "bg-white/5 group-hover:bg-white/10"
          }
        `}
      >
        {icon}
      </div>

      <span className="flex-1 text-left text-sm font-medium">
        {label}
      </span>

      {!disabled && active && (
        <div className="h-2 w-2 rounded-full bg-cyan-400" />
      )}
    </button>
  );
}

export function WorkspaceSidebar() {
  const {
    layout,
    setSelectedView,
    toggleSidebar,
  } = useWorkspaceStore();

  return (
    <aside className={workspaceSidebarVariants()}>
      {/* Header */}

      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">

              <h2 className="text-sm font-semibold uppercase tracking-wider text-white">
                Workspace Navigation
              </h2>
            </div>

          </div>

          <button
            title="Collapse Sidebar"
            onClick={toggleSidebar}
            className="
              rounded-xl
              border
              border-white/10
              bg-white/5
              p-2
              text-white/60
              transition-all
              duration-200
              hover:bg-white/10
              hover:text-white
            "
          >
            <PanelLeftClose className="h-4 w-4" />
          </button>
        </div>

        <div className="mt-5 border-b border-white/10" />
      </div>

      {/* Navigation */}

      <div className="space-y-3">
        <SidebarButton
          active={layout.selectedView === "chat"}
          icon={<MessageSquare className="h-4 w-4" />}
          label="Chat"
          onClick={() => setSelectedView("chat")}
        />

        <SidebarButton
          active={layout.selectedView === "workspace"}
          icon={<FolderOpen className="h-4 w-4" />}
          label="Workspace"
          onClick={() =>
            setSelectedView("workspace")
          }
        />

        <SidebarButton
          active={layout.selectedView === "planner"}
          icon={<ListTodo className="h-4 w-4" />}
          label="Planner"
          onClick={() =>
            setSelectedView("planner")
          }
        />

        <div className="my-4 border-t border-white/10" />

        <SidebarButton
          active={false}
          disabled
          icon={<FolderTree className="h-4 w-4" />}
          label="Explorer"
        />

        <SidebarButton
          active={false}
          disabled
          icon={<Terminal className="h-4 w-4" />}
          label="Terminal"
        />

        <SidebarButton
          active={false}
          disabled
          icon={<History className="h-4 w-4" />}
          label="History"
        />

        <SidebarButton
          active={false}
          disabled
          icon={<Settings className="h-4 w-4" />}
          label="Settings"
        />
      </div>

      {/* Footer */}

      <div className="mt-auto rounded-2xl border border-white/10 bg-black/20 p-4">
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-emerald-400" />

          <p className="text-xs font-medium text-white/70">
            Workspace Ready
          </p>
        </div>

        <p className="mt-3 text-xs leading-6 text-white/45">
          Explorer, Monaco Editor, Terminal and
          History will become available in upcoming
          milestones.
        </p>
      </div>
    </aside>
  );
}