import { cn } from "@/lib";

interface HeroAuroraProps {
  className?: string;
}

export function HeroAurora({
  className,
}: HeroAuroraProps) {
  return (
    <div
      className={cn(
        "absolute inset-0 overflow-hidden pointer-events-none",
        className
      )}
    >
      <div
        className="
          absolute
          left-1/2
          top-0
          h-244
          w-4xl
          -translate-x-1/2
          rounded-full
          bg-linear-to-r
          from-cyan-400/20
          via-violet-500/18
          to-sky-400/20
          blur-[170px]
          animate-aurora
        "
      />
    </div>
  );
}