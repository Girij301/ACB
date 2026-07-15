import { cva } from "class-variance-authority";

export const cardVariants = cva(
  ["rounded-xl", "transition-all", "duration-200"],
  {
    variants: {
      variant: {
        default: ["bg-white/5", "border", "border-white/10"],

        glass: ["glass"],

        outline: ["border", "border-white/20", "bg-transparent"],

        interactive: [
          "cursor-pointer",

          "border",
          "border-white/10",

          "transition-all",
          "duration-200",

          "hover:bg-white/[0.04]",
          "hover:border-white/20",

          "hover:shadow-[0_10px_30px_rgba(0,0,0,0.35)]",
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
  },
);
