import { cva } from "class-variance-authority";

export const footerVariants = cva(
  [
    "border-t",
    "border-white/10",
    "py-10",
    "px-6",
    "lg:px-8",
  ].join(" ")
);