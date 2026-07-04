import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { gridVariants } from "./gridVariants";
import { cn } from "../../../lib";

export interface GridProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof gridVariants> {}

export function Grid({
  className,
  cols,
  gap,
  children,
  ...props
}: GridProps) {
  return (
    <div
      className={cn(
        gridVariants({
          cols,
          gap,
        }),
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}