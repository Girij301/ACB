import { cn } from "@/lib";

interface NavbarBrandProps {
  className?: string;
}

export function NavbarBrand({
  className,
}: NavbarBrandProps) {
  return (
    <a
      href="/"
      className={cn(
        "flex items-center gap-3 select-none",
        className
      )}
    >
      <div
        className={cn(
          "flex h-10 w-10 items-center justify-center",
          "rounded-xl",
          "bg-white/10",
          "border border-white/10",
          "backdrop-blur-xl",
          "font-semibold text-white"
        )}
      >
        AI
      </div>

      <div className="flex flex-col leading-none">
        <span className="font-heading text-xl tracking-tight">
          Autonomous
        </span>

        <span className="text-xs uppercase tracking-[0.3em] text-white/60">
          Coding Agent
        </span>
      </div>
    </a>
  );
}