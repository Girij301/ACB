import { cva } from "class-variance-authority";

export const heroBackgroundVariants = cva(
  [
    "absolute",
    "inset-0",
    "-z-10",
    "overflow-hidden",
    "pointer-events-none",
  ].join(" ")
);