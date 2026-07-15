import { cva } from "class-variance-authority";

export const workspaceContentVariants = cva([
  "relative",
  "flex-1",
  "min-h-0",
  "overflow-hidden",
  "p-6",
]);