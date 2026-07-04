import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { type VariantProps } from "class-variance-authority";

import { cn } from "../../../lib";

import { buttonVariants } from "./buttonVariants";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;

  leftIcon?: React.ReactNode;

  rightIcon?: React.ReactNode;

  loading?: boolean;
}

export function Button({
  asChild = false,

  className,

  variant,

  size,

  leftIcon,

  rightIcon,

  loading,

  children,

  disabled,

  ...props
}: ButtonProps) {
  const Component = asChild ? Slot : "button";

  return (
    <Component
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      ) : (
        leftIcon
      )}

      {children}

      {!loading && rightIcon}
    </Component>
  );
}