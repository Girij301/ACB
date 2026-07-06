import { cva } from "class-variance-authority";

export const workspaceVariants = cva(
  [
    "flex",
    "h-screen",
    "w-full",
    "flex-col",
    "overflow-hidden",
    "bg-background",
    "text-white",
  ].join(" ")
);