import { cn } from "@/lib";

import { HeroCTA } from "./HeroCTA";

interface HeroActionsProps {
  className?: string;
}

export function HeroActions({
  className,
}: HeroActionsProps) {
  return (
    <div
      className={cn(
        "mt-10 flex flex-wrap items-center justify-center gap-5",
        className
      )}
    >
      <HeroCTA primary>
        Get Started
      </HeroCTA>

      <HeroCTA>
        Documentation
      </HeroCTA>
    </div>
  );
}