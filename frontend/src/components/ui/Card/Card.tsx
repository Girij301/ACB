import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { cardVariants } from "./cardVariants";
import { cn } from "../../../lib";

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

export function Card({
  className,
  variant,
  size,
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={cn(
        cardVariants({
          variant,
          size,
        }),
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}