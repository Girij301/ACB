import type { LucideIcon } from "lucide-react";

interface SidebarItemProps {
  label: string;
  icon: LucideIcon;
  active: boolean;
  disabled?: boolean;
  onClick?: () => void;
}

export function SidebarItem({
  label,
  icon: Icon,
  active,
  disabled = false,
  onClick,
}: SidebarItemProps) {
  return (
    <button
      type="button"
      title={disabled ? `${label} (Coming Soon)` : label}
      disabled={disabled}
      onClick={onClick}
      className={`
        flex
        items-center
        gap-3
        rounded-xl
        px-4
        py-3
        text-sm
        transition-all
        duration-200
        outline-none

        ${
          active
            ? "border border-cyan-500/20 bg-cyan-500/10 text-cyan-300"
            : "border border-transparent text-white/70 hover:bg-white/5 hover:text-white"
        }

        ${
          disabled
            ? "cursor-not-allowed opacity-40"
            : "cursor-pointer focus:border-cyan-500/30 focus:bg-cyan-500/10"
        }
      `}
    >
      <Icon className="h-5 w-5 shrink-0" />

      <span className="flex-1 text-left">
        {label}
      </span>

      {disabled && (
        <span className="text-[10px] uppercase tracking-wide text-white/35">
          Soon
        </span>
      )}
    </button>
  );
}