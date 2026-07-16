import { cva } from "class-variance-authority";

export const workspaceHeaderVariants = cva(
  [
    "[grid-area:header]",

    "flex",
    "items-center",
    "justify-between",

    "h-16",
    "flex-shrink-0",

    "border-b",
    "border-white/10",

    "bg-black/20",
    "backdrop-blur-2xl",

    "shadow-[0_8px_30px_rgba(0,0,0,0.18)]",

    "px-6",

    "transition-all",
    "duration-300",
  ].join(" ")
);