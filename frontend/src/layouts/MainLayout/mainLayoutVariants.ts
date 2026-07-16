import { cva } from "class-variance-authority";

export const mainLayoutVariants = cva([
  "relative",
  "flex",
  "h-screen",
  "w-full",
  "overflow-hidden",
  "bg-background",
  "text-white",
]);