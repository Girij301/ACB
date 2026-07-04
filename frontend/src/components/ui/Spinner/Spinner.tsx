import { type VariantProps } from "class-variance-authority";

import { spinnerVariants } from "./spinnerVariants";
import { cn } from "../../../lib";

export interface SpinnerProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof spinnerVariants> {}

export function Spinner({
  className,
  size,
  variant,
  ...props
}: SpinnerProps) {
  return (
    <span
      role="status"
      aria-label="Loading"
      className={cn(
        spinnerVariants({
          size,
          variant,
        }),
        className
      )}
      {...props}
    />
  );
}