import { cn } from "@/lib";

interface HeroOrbProps {
  className?: string;
}

export function HeroOrb({
  className,
}: HeroOrbProps) {
  return (
    <div
      className={cn(
        "absolute rounded-full blur-[180px] animate-float",
        className
      )}
    />
  );
}