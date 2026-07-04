import { cva } from "class-variance-authority";

export const heroScrollIndicatorVariants = cva(
  [
    "absolute",

    "bottom-10",
    "left-1/2",

    "-translate-x-1/2",

    "flex",
    "flex-col",
    "items-center",
    "gap-2",

    "cursor-pointer",

    "select-none",

    "text-white/60",

    "transition-all",
    "duration-300",

    "hover:text-white",
  ].join(" ")
);