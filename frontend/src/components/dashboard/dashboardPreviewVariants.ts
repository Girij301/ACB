import { cva } from "class-variance-authority";

export const dashboardPreviewVariants = cva(
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