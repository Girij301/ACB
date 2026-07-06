import { cva } from "class-variance-authority";

export const workspaceSidebarVariants = cva(
  [
    "flex",
    "w-72",
    "flex-col",
    "border-r",
    "border-white/10",
    "bg-white/[0.02]",
    "backdrop-blur-xl",
    "p-4",
    "shrink-0",
  ].join(" ")
);