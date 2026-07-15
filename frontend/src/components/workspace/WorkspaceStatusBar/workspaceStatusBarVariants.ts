import { cva } from "class-variance-authority";

export const workspaceStatusBarVariants = cva(
  [
    "[grid-area:status]",

    "flex",
    "items-center",

    "h-10",
    "flex-shrink-0",

    "border-t",
    "border-white/10",

    "bg-white/[0.03]",

    "px-6",
    "text-sm",
    "text-white/60",
  ].join(" ")
);