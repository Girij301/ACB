import { cva } from "class-variance-authority";

export const workspaceMainVariants = cva(
  [
    "flex",
    "flex-1",
    "min-h-0",
    "overflow-hidden",
  ].join(" ")
);