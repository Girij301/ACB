import { cva } from "class-variance-authority";

export const mainLayoutVariants = cva([
  "relative",
  "flex",
  "w-full",
  "bg-background",
  "text-white",
  "min-h-screen",
  "flex-col"
]);