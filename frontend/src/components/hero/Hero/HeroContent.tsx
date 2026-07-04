import { Heading, Text } from "@/components/ui";
import { cn } from "@/lib";

import { heroContentVariants } from "./heroVariants";

import { GradientText } from "@/components/animations/GradientText";

interface HeroContentProps {
  className?: string;
}

export function HeroContent({ className }: HeroContentProps) {
  return (
    <div className={cn(heroContentVariants(), className)}>
      <Heading
        level="h1"
        className="
          max-w-4xl
          text-balance
          text-5xl
          font-light
          italic
          leading-now
          tracking-tight
          text-white

          md:text-6xl
          lg:text-7xl
        "
      >
        Build, Debug & Deploy
        <br />
        with an Autonomous
        <br />
        <GradientText>AI Coding Agent</GradientText>
      </Heading>

      <Text
        variant="muted"
        className="
          mt-8
          max-w-xl
          text-lg
          leading-8
        "
      >
        AI software engineer that can understand goals, generate execution
        plans, write code, debug failures, execute tasks inside Docker, and
        continuously improve through intelligent self-healing.
      </Text>
    </div>
  );
}
