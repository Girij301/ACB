import { cva } from "class-variance-authority";

export const inputVariants = cva(
  [
    "w-full",
    "rounded-full",
    "transition-all",
    "duration-200",
    "outline-none",
    "text-white",
    "placeholder:text-white/45",
    "disabled:pointer-events-none",
    "disabled:opacity-50",
    "focus:ring-2",
    "focus:ring-white/20",
  ],
  {
    variants: {
      variant: {
        default: [
          "bg-white/5",
          "border",
          "border-white/10",
        ],

        glass: [
          "liquid-glass",
          "bg-white/5",
        ],

        ghost: [
          "bg-transparent",
          "border",
          "border-transparent",
        ],
      },

      size: {
        sm: "h-10 px-4 text-sm",

        md: "h-12 px-5 text-base",

        lg: "h-14 px-6 text-lg",
      },

      error: {
        true: [
          "border-red-500",
          "focus:ring-red-400/30",
        ],

        false: "",
      },
    },

    defaultVariants: {
      variant: "default",
      size: "md",
      error: false,
    },
  }
);