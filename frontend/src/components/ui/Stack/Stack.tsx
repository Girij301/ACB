import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { stackVariants } from "./stackVariants";
import { cn } from "../../../lib";

export interface StackProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof stackVariants> {}

export function Stack({
  className,
  direction,
  gap,
  align,
  justify,
  wrap,
  children,
  ...props
}: StackProps) {
  return (
    <div
      className={cn(
        stackVariants({
          direction,
          gap,
          align,
          justify,
          wrap,
        }),
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}