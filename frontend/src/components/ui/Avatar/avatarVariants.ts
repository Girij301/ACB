import { cva } from "class-variance-authority";

export const avatarVariants = cva(
  [
    "inline-flex",
    "items-center",
    "justify-center",
    "overflow-hidden",
    "rounded-full",
    "bg-white/5",
    "border",
    "border-white/10",
    "select-none",
    "shrink-0",
  ],
  {
    variants: {
      size: {
        xs: "h-6 w-6 text-[10px]",
        sm: "h-8 w-8 text-xs",
        md: "h-10 w-10 text-sm",
        lg: "h-12 w-12 text-base",
        xl: "h-16 w-16 text-lg",
      },

      variant: {
        default: "",

        glass: "liquid-glass",
      },
    },

    defaultVariants: {
      size: "md",
      variant: "default",
    },
  }
);