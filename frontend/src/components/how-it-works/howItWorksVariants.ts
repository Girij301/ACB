import { cva } from "class-variance-authority";

export const howItWorksVariants = cva(
  [
    "relative",
    "mx-auto",
    "flex",
    "w-full",
    "max-w-7xl",
    "flex-col",
    "items-center",
    "gap-20",
    "px-6",
    "py-36",
    "lg:px-8",
  ].join(" ")
);

export const timelineVariants = cva(
  [
    "relative",
    "mx-auto",
    "flex",
    "w-full",
    "max-w-5xl",
    "flex-col",
    "gap-12",
  ].join(" ")
);