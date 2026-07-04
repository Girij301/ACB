import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { containerVariants } from "./containerVariants";
import { cn } from "../../../lib";

export interface ContainerProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof containerVariants> {}

export function Container({
  className,
  size,
  padding,
  children,
  ...props
}: ContainerProps) {
  return (
    <div
      className={cn(
        containerVariants({
          size,
          padding,
        }),
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}