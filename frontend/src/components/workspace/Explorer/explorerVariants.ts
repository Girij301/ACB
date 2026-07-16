import { cva } from "class-variance-authority";

export const explorerVariants = cva(
  [
    "flex",
    "h-full",
    "min-h-0",
    "flex-col",

    "rounded-2xl",

    "border",
    "border-white/10",

    "bg-black/20",

    "backdrop-blur-xl",

    "overflow-hidden",
  ].join(" "),
);