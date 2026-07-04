import { cva } from "class-variance-authority";

export const mainLayoutVariants = cva(
  [
    "relative",
    "min-h-screen",
    "overflow-x-hidden",
    "bg-background",
    "text-white",
  ]
);