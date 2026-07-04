import { cva } from "class-variance-authority";

export const navbarVariants = cva(
  [
    "fixed",
    "top-6",
    "left-1/2",
    "-translate-x-1/2",

    "z-50",

    "flex",
    "items-center",
    "justify-between",

    "w-[min(1200px,calc(100%-2rem))]",

    "rounded-full",

    "border",
    "border-white/10",

    "bg-white/5",

    "backdrop-blur-2xl",

    "shadow-xl",

    "px-6",
    "py-3",

    "transition-all",
    "duration-300",
  ].join(" ")
);