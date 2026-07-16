import {
  Activity,
  Terminal,
 AlertCircle,
  FileText,
} from "lucide-react";

import { useWorkspaceStore } from "@/store";

export function BottomPanel() {
  const { layout, setActivePanel } =
    useWorkspaceStore();

  function Tab({
    id,
    icon,
    label,
    disabled = false,
  }: {
    id:
      | "activity"
      | "chat"
      | "planner";
    icon: React.ReactNode;
    label: string;
    disabled?: boolean;
  }) {
    const active =
      layout.activePanel === id;

    return (
      <button
        disabled={disabled}
        title={
          disabled
            ? `${label} (Coming Soon)`
            : label
        }
        onClick={() =>
          !disabled &&
          setActivePanel(id)
        }
        className={`
          flex
          items-center
          gap-2
          rounded-lg
          border
          px-3
          py-2
          text-sm
          transition-all
          duration-200
          ${
            active
              ? "border-cyan-500/20 bg-cyan-500/10 text-cyan-300"
              : disabled
                ? "cursor-not-allowed border-transparent text-white/30 opacity-50"
                : "border-transparent text-white/60 hover:bg-white/5 hover:text-white"
          }
        `}
      >
        {icon}
        {label}
      </button>
    );
  }

  return (
    <section
      className="
        glass
        flex
        h-56
        flex-shrink-0
        flex-col
        overflow-hidden
        rounded-2xl
        border
        border-white/10
      "
    >
      {/* Header */}

      <div
        className="
          flex
          items-center
          gap-2
          border-b
          border-white/10
          px-4
          py-3
        "
      >
        <Tab
          id="activity"
          icon={
            <Activity className="h-4 w-4" />
          }
          label="Activity"
        />

        <Tab
          id="chat"
          disabled
          icon={
            <Terminal className="h-4 w-4" />
          }
          label="Terminal"
        />

        <Tab
          id="planner"
          disabled
          icon={
            <AlertCircle className="h-4 w-4" />
          }
          label="Problems"
        />

        <Tab
          id="planner"
          disabled
          icon={
            <FileText className="h-4 w-4" />
          }
          label="Output"
        />
      </div>

      {/* Content */}

      <div
        className="
          flex
          flex-1
          items-center
          justify-center
          bg-black/20
        "
      >
        <div className="text-center">
          <Activity className="mx-auto h-10 w-10 text-cyan-400/70" />

          <h3 className="mt-4 text-base font-semibold text-white">
            Activity Panel
          </h3>

          <p className="mt-2 max-w-lg text-sm leading-7 text-white/45">
            The live execution dashboard will appear
            here. Terminal, Problems and Output will
            become available in future milestones.
          </p>
        </div>
      </div>
    </section>
  );
}