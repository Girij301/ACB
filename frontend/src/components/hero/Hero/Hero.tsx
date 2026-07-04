import { BlurReveal } from "@/components/animations/BlurReveal";
import { cn } from "@/lib";

import { HeroBackground } from "../HeroBackground";
import { HeroScrollIndicator } from "../HeroScrollIndicator";
import { HeroActions } from "./HeroActions";
import { HeroContent } from "./HeroContent";
import { heroVariants } from "./heroVariants";

interface HeroProps {
  className?: string;
}

export function Hero({
  className,
}: HeroProps) {
  return (
    <section className={cn(heroVariants(), className)}>
      <HeroBackground />

      <BlurReveal>
        <div className="relative z-10 mx-auto flex w-full max-w-5xl flex-col items-center text-center">
          <HeroContent />

          <HeroActions className="mt-10" />
        </div>
      </BlurReveal>

      <HeroScrollIndicator />
    </section>
  );
}