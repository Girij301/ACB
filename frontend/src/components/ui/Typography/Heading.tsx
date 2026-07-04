import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { headingVariants } from "./typographyVariants";
import { cn } from "../../../lib";

type HeadingTag = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";

export interface HeadingProps
  extends React.HTMLAttributes<HTMLHeadingElement>,
    VariantProps<typeof headingVariants> {}

export function Heading({
  level = "h2",
  className,
  children,
  ...props
}: HeadingProps) {
  const Tag: HeadingTag = level ?? "h2";

  return (
    <Tag
      className={cn(
        headingVariants({
          level,
        }),
        className
      )}
      {...props}
    >
      {children}
    </Tag>
  );
}