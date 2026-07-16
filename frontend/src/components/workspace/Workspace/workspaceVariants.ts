import { cva } from "class-variance-authority";

export const workspaceVariants = cva([
  "relative",
  "flex",
  "h-screen",
  "w-full",
  "flex-col",
  "bg-background",
  "text-white",
].join(" "));