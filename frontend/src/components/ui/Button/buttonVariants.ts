import { cva } from "class-variance-authority";

export const buttonVariants = cva(
  [
    "inline-flex",
    "items-center",
    "justify-center",
    "gap-2",
    "rounded-full",
    "font-medium",
    "transition-all",
    "duration-300",
    "will-change-transform",
    "disabled:pointer-events-none",
    "disabled:opacity-50",
    "select-none",
    "cursor-pointer",
  ],
  {
    variants: {
      variant: {
        primary:
          "bg-blue-600 text-white hover:bg-blue-700",

        secondary:
          "bg-zinc-800 text-white hover:bg-zinc-700",

        ghost:
          "bg-transparent text-white hover:bg-white/10",

        ghostGlass:
          `
          bg-transparent
          text-white
          border
          border-transparent
          hover:glass
          hover:border-white/10
          hover:-translate-y-0.5
          hover:scale-[1.02]
          `,

        glass:
          "glass text-white",
      },

      size: {
        sm: "h-9 px-4 text-sm",

        md: "h-11 px-6 text-sm",

        lg: "h-14 px-8 text-base",
      },
    },

    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);