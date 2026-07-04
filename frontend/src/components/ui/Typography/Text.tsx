import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { textVariants } from "./typographyVariants";
import { cn } from "../../../lib";

export interface TextProps
  extends React.HTMLAttributes<HTMLParagraphElement>,
    VariantProps<typeof textVariants> {}

export function Text({
  variant,
  className,
  children,
  ...props
}: TextProps) {
  return (
    <p
      className={cn(
        textVariants({
          variant,
        }),
        className
      )}
      {...props}
    >
      {children}
    </p>
  );
}