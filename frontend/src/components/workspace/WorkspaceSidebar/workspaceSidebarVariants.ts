import { cva } from "class-variance-authority";

export const workspaceSidebarVariants = cva(
  [
    "flex",
    "w-[260px]",
    "flex-col",
    "shrink-0",

    "rounded-2xl",

    "border",
    "border-white/10",

    "bg-black/20",

    "backdrop-blur-2xl",

    "shadow-[0_10px_30px_rgba(0,0,0,0.18)]",

    "p-5",

    "transition-all",
    "duration-300",
  ].join(" ")
);