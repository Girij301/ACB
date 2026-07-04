import { cva } from "class-variance-authority";

export const cardVariants = cva(
  [
    "rounded-3xl",
    "transition-all",
    "duration-200",
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

        outline: [
          "border",
          "border-white/20",
          "bg-transparent",
        ],

        interactive: [
          "hover:bg-white/[0.08]",
          "hover:border-white/20",
          "hover:-translate-y-1",
          "hover:shadow-2xl",
          "hover:shadow-cyan-500/5",
          "cursor-pointer",
        ],
      },

      size: {
        sm: "p-4",

        md: "p-6",

        lg: "p-8",
      },
    },

    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);