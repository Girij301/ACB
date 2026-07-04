import { cn } from "@/lib";

interface HeroNoiseProps {
  className?: string;
}

export function HeroNoise({
  className,
}: HeroNoiseProps) {
  return (
    <div
      className={cn(
        "absolute inset-0",
        "pointer-events-none",
        "opacity-[0.025]",
        className
      )}
      style={{
        backgroundImage:
          "radial-gradient(circle at 1px 1px, rgba(255,255,255,0.6) 1px, transparent 0)",
        backgroundSize: "6px 6px",
      }}
    />
  );
}