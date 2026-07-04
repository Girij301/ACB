import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { sectionVariants } from "./sectionVariants";
import { cn } from "../../../lib";

export interface SectionProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof sectionVariants> {}

export function Section({
  className,
  spacing,
  children,
  ...props
}: SectionProps) {
  return (
    <section
      className={cn(
        sectionVariants({
          spacing,
        }),
        className
      )}
      {...props}
    >
      {children}
    </section>
  );
}