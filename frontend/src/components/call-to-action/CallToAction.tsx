import { ArrowRight } from "lucide-react";

import { BlurReveal } from "@/components/animations";
import { Button, Heading } from "@/components/ui";

import { callToActionVariants } from "./callToActionVariants";

export function CallToAction() {
  return (
    <section className={callToActionVariants()}>
      <BlurReveal>
        <Heading level="h2">Ready to Build with Autonomous AI?</Heading>

        <p className="mt-6 max-w-2xl text-lg leading-8 text-white/70">
          Transform ideas into production-ready software with an autonomous AI
          engineer that plans, builds, debugs and validates every step.
        </p>

        <div className="mt-10 flex flex-wrap justify-center gap-5">
          <Button size="lg" variant="glass">
            Launch App
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>

          <Button size="lg" variant="ghost">
            View GitHub
          </Button>
        </div>
      </BlurReveal>
    </section>
  );
}
