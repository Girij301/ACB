import type { HTMLAttributes } from "react";

import { cn } from "@/lib";

import { blurRevealVariants } from "./blurRevealVariants";

interface BlurRevealProps
  extends HTMLAttributes<HTMLDivElement> {}

export function BlurReveal({
  className,
  children,
  ...props
}: BlurRevealProps) {
  return (
    <div
      className={cn(
        blurRevealVariants(),
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}