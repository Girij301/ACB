import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { inputVariants } from "./inputVariants";
import { cn } from "../../../lib";

type NativeInputProps = Omit<
  React.InputHTMLAttributes<HTMLInputElement>,
  "size"
>;

export interface InputProps
  extends NativeInputProps,
    VariantProps<typeof inputVariants> {
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      variant,
      size,
      error,
      leftIcon,
      rightIcon,
      ...props
    },
    ref
  ) => {
    return (
      <div className="relative w-full">
        {leftIcon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white/60">
            {leftIcon}
          </div>
        )}

        <input
          ref={ref}
          className={cn(
            inputVariants({
              variant,
              size,
              error,
            }),
            leftIcon && "pl-11",
            rightIcon && "pr-11",
            className
          )}
          {...props}
        />

        {rightIcon && (
          <div className="absolute right-4 top-1/2 -translate-y-1/2 text-white/60">
            {rightIcon}
          </div>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";