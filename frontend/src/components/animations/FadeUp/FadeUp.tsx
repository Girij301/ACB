import type { PropsWithChildren } from "react";

import { cn } from "@/lib";

interface FadeUpProps extends PropsWithChildren {
  delay?: number;
  className?: string;
}

export function FadeUp({
  children,
  delay = 0,
  className,
}: FadeUpProps) {
  return (
    <div
      className={cn(
        "w-full animate-blur-reveal opacity-0",
        className
      )}
      style={{
        animationDelay: `${delay}ms`,
        animationFillMode: "forwards",
      }}
    >
      {children}
    </div>
  );
}