import { BrainCircuit, Code2, Rocket, Wrench } from "lucide-react";

import { FadeUp } from "@/components/animations";
import { Heading } from "@/components/ui";

import { howItWorksVariants, timelineVariants } from "./howItWorksVariants";
import { TimelineStep } from "./TimelineStep";

export function HowItWorks() {
  return (
    <section id="documentation" className={howItWorksVariants()}>
      <div className="max-w-3xl text-center">
        <Heading level="h2">How It Works</Heading>

        <p className="mt-6 text-lg text-white/70">
          From idea to production, your AI engineer manages the complete
          software development lifecycle.
        </p>
      </div>

      <div className={timelineVariants()}>
        <FadeUp delay={100}>
          <TimelineStep
            number="01"
            icon={BrainCircuit}
            title="Understand Your Goal"
            description="Describe what you want to build in plain English. The AI analyzes requirements and creates a structured execution strategy."
          />
        </FadeUp>

        <FadeUp delay={200}>
          <TimelineStep
            number="02"
            icon={Code2}
            title="Generate & Execute"
            description="The agent writes production-ready code, executes commands safely, and validates every implementation step."
          />
        </FadeUp>

        <FadeUp delay={300}>
          <TimelineStep
            number="03"
            icon={Wrench}
            title="Debug Automatically"
            description="When something fails, the AI analyzes logs, diagnoses root causes, and applies intelligent fixes without manual intervention."
          />
        </FadeUp>

        <FadeUp delay={400}>
          <TimelineStep
            number="04"
            icon={Rocket}
            title="Deliver Production Ready"
            description="The project is validated, tested, and prepared for deployment with confidence."
          />
        </FadeUp>
      </div>
    </section>
  );
}
