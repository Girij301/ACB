import { cva } from "class-variance-authority";

export const badgeVariants = cva(
  [
    "inline-flex",
    "items-center",
    "justify-center",
    "rounded-full",
    "font-medium",
    "transition-colors",
    "whitespace-nowrap",
    "select-none",
  ],
  {
    variants: {
      variant: {
        default: [
          "bg-white/10",
          "text-white",
          "border",
          "border-white/10",
        ],

        glass: [
          "liquid-glass",
          "text-white",
        ],

        success: [
          "bg-emerald-500/20",
          "text-emerald-300",
          "border",
          "border-emerald-400/30",
        ],

        warning: [
          "bg-amber-500/20",
          "text-amber-300",
          "border",
          "border-amber-400/30",
        ],

        danger: [
          "bg-red-500/20",
          "text-red-300",
          "border",
          "border-red-400/30",
        ],

        outline: [
          "bg-transparent",
          "text-white",
          "border",
          "border-white/15",
        ],
      },

      size: {
        sm: "h-6 px-2.5 text-xs",

        md: "h-8 px-3 text-sm",

        lg: "h-10 px-4 text-base",
      },
    },

    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);