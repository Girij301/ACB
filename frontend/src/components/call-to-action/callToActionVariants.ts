import { cva } from "class-variance-authority";

export const callToActionVariants = cva(
  [
    "relative",
    "mx-auto",
    "flex",
    "w-full",
    "max-w-7xl",
    "flex-col",
    "items-center",
    "justify-center",
    "gap-10",
    "px-6",
    "py-36",
    "text-center",
    "lg:px-8",
  ].join(" ")
);