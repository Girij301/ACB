import { Bot, Bug, Rocket, Workflow } from "lucide-react";

import { FadeUp } from "@/components/animations";
import { Heading } from "@/components/ui";

import {
  capabilitiesVariants,
  capabilityGridVariants,
} from "./capabilityVariants";
import { CapabilityCard } from "./CapabilityCard";

export function Capabilities() {
  return (
    <section id="capabilities" className={capabilitiesVariants()}>
      <div className="max-w-3xl text-center">
        <Heading level="h2">Everything Your AI Engineer Needs</Heading>

        <p className="mt-6 text-lg text-white/70">
          Build, debug, validate and deploy software with an autonomous AI
          development platform.
        </p>
      </div>

      <div className={capabilityGridVariants()}>
        <FadeUp delay={100}>
          <CapabilityCard
            icon={Workflow}
            title="AI Planning"
            description="Transforms complex goals into structured execution plans."
          />
        </FadeUp>

        <FadeUp delay={200}>
          <CapabilityCard
            icon={Bot}
            title="Code Generation"
            description="Writes production-quality code using modern engineering practices."
          />
        </FadeUp>

        <FadeUp delay={300}>
          <CapabilityCard
            icon={Bug}
            title="Self Debugging"
            description="Automatically detects failures, analyzes logs and fixes problems."
          />
        </FadeUp>

        <FadeUp delay={400}>
          <CapabilityCard
            icon={Rocket}
            title="Deployment Ready"
            description="Validates, tests and prepares projects for production deployment."
          />
        </FadeUp>
      </div>
    </section>
  );
}
