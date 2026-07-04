import { cva } from "class-variance-authority";

export const containerVariants = cva(
  [
    "mx-auto",
    "w-full",
  ],
  {
    variants: {
      size: {
        sm: "max-w-3xl",
        md: "max-w-5xl",
        lg: "max-w-7xl",
        xl: "max-w-[1440px]",
        full: "max-w-none",
      },

      padding: {
        none: "",
        sm: "px-4",
        md: "px-6",
        lg: "px-8",
        xl: "px-12",
      },
    },

    defaultVariants: {
      size: "xl",
      padding: "lg",
    },
  }
);