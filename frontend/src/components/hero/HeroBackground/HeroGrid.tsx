import { cn } from "@/lib";

interface HeroGridProps {
  className?: string;
}

export function HeroGrid({
  className,
}: HeroGridProps) {
  return (
    <div
      className={cn(
        "absolute inset-0",
        "pointer-events-none",
        className
      )}
    >
      <div
        className="
          absolute
          inset-0
          opacity-[0.06]
          bg-[linear-gradient(rgba(255,255,255,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.08)_1px,transparent_1px)]
          bg-size-[48px_48px]
        "
      />
    </div>
  );
}