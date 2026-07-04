import type { HTMLAttributes } from "react";

import { cn } from "@/lib";

import { gradientTextVariants } from "./gradientTextVariants";

interface GradientTextProps
  extends HTMLAttributes<HTMLSpanElement> {}

export function GradientText({
  className,
  children,
  ...props
}: GradientTextProps) {
  return (
    <span
      className={cn(
        gradientTextVariants(),
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}