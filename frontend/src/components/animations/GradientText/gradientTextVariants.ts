import { cva } from "class-variance-authority";

export const gradientTextVariants = cva(
  [
    "inline-block",

    "bg-gradient-to-r",
    "from-cyan-400",
    "via-sky-300",
    "to-violet-400",

    "bg-[length:200%_200%]",
    "bg-clip-text",

    "text-transparent",

    "animate-gradient",
  ].join(" ")
);