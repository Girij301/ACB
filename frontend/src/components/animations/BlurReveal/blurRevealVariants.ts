import { cva } from "class-variance-authority";

export const blurRevealVariants = cva(
  [
    "animate-blur-reveal",
    "will-change-transform",
  ].join(" ")
);