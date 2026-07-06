import { useAuth } from "@clerk/clerk-react";

import { cn } from "@/lib";

import { HeroCTA } from "./HeroCTA";

interface HeroActionsProps {
  className?: string;
}

export function HeroActions({
  className,
}: HeroActionsProps) {
  const { isSignedIn } = useAuth();

  return (
    <div
      className={cn(
        "mt-10 flex flex-wrap items-center justify-center gap-5",
        className
      )}
    >
      <HeroCTA
        primary
        href={isSignedIn ? "/workspace" : "/sign-in"}
      >
        {isSignedIn
          ? "Open Workspace"
          : "Get Started"}
      </HeroCTA>

      <HeroCTA href="#">
        Documentation
      </HeroCTA>
    </div>
  );
}