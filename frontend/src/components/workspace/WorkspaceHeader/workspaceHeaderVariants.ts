import { cva } from "class-variance-authority";

export const workspaceHeaderVariants = cva(
  [
    "[grid-area:header]",

    "flex",
    "items-center",
    "justify-between",

    "h-14",
    "flex-shrink-0",

    "border-b",
    "border-white/10",

    "bg-white/[0.03]",
    "backdrop-blur-xl",

    "px-6",
  ].join(" ")
);