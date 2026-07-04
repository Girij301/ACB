import { cva } from "class-variance-authority";

export const spinnerVariants = cva(
  [
    "inline-block",
    "animate-spin",
    "rounded-full",
    "border-current",
    "border-t-transparent",
  ],
  {
    variants: {
      size: {
        xs: "h-3 w-3 border",
        sm: "h-4 w-4 border-2",
        md: "h-6 w-6 border-2",
        lg: "h-8 w-8 border-[3px]",
        xl: "h-10 w-10 border-4",
      },

      variant: {
        default: "text-white",

        muted: "text-white/50",

        primary: "text-white",

        danger: "text-red-400",
      },
    },

    defaultVariants: {
      size: "md",
      variant: "default",
    },
  }
);