import { cn } from "@/lib";

import { HeroAurora } from "./HeroAurora";
import { HeroGrid } from "./HeroGrid";
import { HeroNoise } from "./HeroNoise";
import { HeroOrb } from "./HeroOrb";
import { heroBackgroundVariants } from "./heroBackgroundVariants";

interface HeroBackgroundProps {
  className?: string;
}

export function HeroBackground({
  className,
}: HeroBackgroundProps) {
  return (
    <div
  className={cn(
    heroBackgroundVariants(),
    "bottom-[-8rem]",
    className
  )}
>
      <HeroGrid />

      <HeroNoise />

      <HeroAurora />

      <HeroOrb
        className="
          left-12
          top-40
          h-60
          w-60
          bg-cyan-500/20
        "
      />

      <HeroOrb
        className="
          right-12
          top-64
          h-72
          w-72
          bg-violet-500/30
        "
      />

      <div
        className="
          absolute
          left-1/2
          top-40
          h-136
          w-136
          -translate-x-1/2
          rounded-full
          bg-cyan-500/7
          blur-[140px]
        "
      />

      <div
        className="
          absolute
          left-0
          top-1/3
          h-72
          w-72
          rounded-full
          bg-violet-500/6
          blur-[120px]
        "
      />

      <div
        className="
          absolute
          right-0
          top-1/4
          h-80
          w-80
          rounded-full
          bg-blue-500/10
          blur-[140px]
        "
      />

      {/* Bottom Fade */}
      <div
        className="
          absolute
          inset-x-0
          bottom-0
          h-48
          bg-linear-to-b
          from-transparent
          to-[#050505]
        "
      />
    </div>
  );
}