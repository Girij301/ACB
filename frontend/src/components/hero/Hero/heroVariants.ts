import { cva } from "class-variance-authority";

export const heroVariants = cva(
  [
    "relative",

    "flex",
    "min-h-screen",
    "items-center",
    "justify-center",

    "overflow-hidden",

    
    "py-36",
    "lg:py-44"
  ].join(" ")
);

export const heroContentVariants = cva(
  [
    "relative",

    "z-10",

    "mx-auto",

    "flex",
    "max-w-5xl",
    "flex-col",
    "items-center",

    "text-center",
  ].join(" ")
);